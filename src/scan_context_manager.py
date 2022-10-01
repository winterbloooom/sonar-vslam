import numpy as np
import cv2
import matplotlib.pyplot as plt

def visualize_scan_context(scan_context, idx):
    cmap = plt.get_cmap('Greys')
    plt.matshow(scan_context, cmap=cmap)
    # plt.colorbar()
    plt.tight_layout()
    plt.savefig("./sc_"+str(idx)+".png")

class ScanContextManager:
    def __init__(self, 
                sequence_length: int, 
                max_range: float, 
                max_azimuth: float, 
                sector_res: int, 
                ring_res: int, 
                sonar_img_ext: str = "npy", ):
        """
        Args
            sequence_length (int): 시퀀스 내 스캔 개수 = 이미지 개수
            sonar_img_ext (str) : 이미지인지 npy인지
        """
        self.sequence_length = sequence_length
        self.scan_contexts = [[]] * sequence_length # 복제 식으로 들어가진 않는지 점검
        self.ring_keys = [0] * sequence_length # 복제 식으로 들어가진 않는지 점검
        self.sonar_img_ext = sonar_img_ext # default: "npy"

        self.max_range = max_range
        self.max_azimuth = max_azimuth
        self.sector_res = sector_res
        self.ring_res = ring_res
        self.sector_gap = (self.max_azimuth + 1) / self.sector_res # 0 혹은 맨 끝 값 포함하려 +1
        self.ring_gap = self.max_range / self.ring_res # min_range가 있기 때문에 맨 마지막은 넘치면 버리면 됨. 임시


    def add_node(self, sonar_data_path: str, node_idx: int):
        """
        Args
            sonar_data_path (str) : npy 또는 이미지 형태의 데이터의 파일명(경로)
            node_idx (int) : 노드의 인덱스
        """
        assert node_idx <= self.sequence_length, "Node index is out of Sequence Length"

        # data load
        if self.sonar_img_ext == "npy":
            scan = np.load(sonar_data_path)
        else: 
            scan = cv2.imread(sonar_data_path, cv2.COLOR_BGR2GRAY)
        
        # change to sc
        current_scan_context, current_ring_key = self.create_scan_context(scan)

        # make node
        self.scan_contexts[node_idx] = current_scan_context
        self.ring_keys[node_idx] = current_ring_key


    def create_scan_context(self, scan: np.ndarray):
        """
        Args
            scan (ndarray) : (이미지 세로, 가로)의 이미지 numpy 배열
        """
        assert scan.shape[0] == scan.shape[1], "Not a square sonar image" # 정사각 이미지라 가정

        img_size = scan.shape[0]
        meter_per_pixel = self.max_range / img_size # m / pixel
        degree_per_pixel = self.max_azimuth / img_size # deg / pixel

        # image -> point cloud
        points_in_sonar = []
        for row in range(img_size):
            range_ = self.max_range - row * meter_per_pixel
            for col in range(img_size):
                intensity = scan[row, col] / 255
                azimuth_ = (col + 1) * degree_per_pixel
                p = {"range": range_, "azimuth": azimuth_, "intensity": intensity}
                points_in_sonar.append(p)

        # point cloud -> sc
        scan_context = np.zeros((self.ring_res, self.sector_res))
        for point in points_in_sonar:
            sector_idx = int(np.divmod(point['azimuth'], self.sector_gap)[0]) # 0 (azimuth 0) ~ 39 (azimuth 130)
            ring_idx = int(np.divmod(point['range'], self.ring_gap)[0]) - 1
            if ring_idx < 0: # point['range'] < min_range
                continue
            if scan_context[ring_idx, sector_idx] < point['intensity']:
                scan_context[ring_idx, sector_idx] = point['intensity']

        # ring key
        ring_key = np.mean(scan_context, axis=1)

        return scan_context, ring_key
