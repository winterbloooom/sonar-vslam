"""
싱글턴 패턴으로 제작
- configuration(params)
- scancontexts
- pose graph
"""

# TODO
# 함수 아주 세세하게 조깨기. for test
# Test 붙이기
# formatter 붙이기

import natsort
import os

from scan_context_manager import *
from pose_graph import *
import yaml # pip install pyyaml

class System:
    def __init__(self, params_path: str) -> None:
        """
        Args
            params_path: config를 파일로 따로 저장해서 json이나 yml로 불러오자

        """
        # parameters
        self.params_path = params_path

        self.sonar_img_path = 0
        self.sonar_img_ext = 0
        self.min_range = 0
        self.max_range = 0
        self.max_azimuth = 0
        self.sector_res = 0
        self.ring_res = 0
        self.scan_paths = [path for path in natsort.natsorted(os.listdir(self.sonar_img_path))]
        self.sequence_length = len(self.scan_paths)

        # Node(Scan Contexts)
        self.sc_manager = None

        # Pose Graph
        self.pose_graph = PoseGraph()

    def load_params(self):
        with open(self.params_path) as f:
            params = yaml.load(f, Loader=yaml.FullLoader)
            self.sonar_img_path = params['sonar_img_path']
            self.sonar_img_ext = params['sonar_img_ext']
            self.min_range = params['min_range']
            self.max_range = params['max_range']
            self.max_azimuth = params['max_azimuth']
            self.sector_res = params['sector_res']
            self.ring_res = params['ring_res']

    def create_scan_context_manager(self):
        self.sc_manager = ScanContextManager(sequence_length=self.sequence_length, 
                                            max_range=self.max_range,
                                            max_azimuth=self.max_azimuth,
                                            sector_res=self.sector_res,
                                            ring_res=self.ring_res,
                                            sonar_img_ext=self.sonar_img_ext,)