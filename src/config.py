import os
import natsort
import numpy as np
import cv2

class Config:
    def __init__(self, img_dir: str, img_ext: str, min_range: float, max_range: float, max_azimuth: float, sector_res: int, ring_res: int) -> None:
        """
        Args:
            img_dir (str) : directory path including sonar images
            img_ext (str) : extension of sonar image. "npy" or image format(e.g. "png", "jpg")
            min_range (float) : minimum range of sonar [m]
            max_range (float) : maximum range of sonar [m]
            min_azimuth (float) : maximum azimuth of sonar [deg]
            sector_res (int) : resolution of sectors (= how many sectors you want to make?)
            ring_res (int) : resolution of rings (= how many rings you want to make?)
        """
        self.img_paths = [path for path in natsort.natsorted(os.listdir(img_dir))] # paths of all sonar imgaes
        self.img_ext = img_ext
        self.imgs = []
        self.img_size = 0 # square 이라 가정

        self.min_range = min_range
        self.max_range = max_range
        self.max_azimuth = max_azimuth

        self.meter_per_pixel = self.max_range / self.img_size # m / pixel
        self.degree_per_pixel = self.max_azimuth / self.img_size # deg / pixel
        
        self.sector_res = sector_res
        self.sector_gap = (self.max_azimuth + 1) / self.sector_res # 0 혹은 맨 끝 값 포함하려 +1

        self.ring_res = ring_res # res가 max_range 보다 작아지면 1m가 포함이 안됨
        self.ring_gap = self.max_range / self.ring_res # min_range가 있기 때문에 맨 마지막은 넘치면 버리면 됨. 임시
        
        self.SCs = [] # scan_context 들의 모음
        # self.scan_context = np.zeros((self.ring_res, self.sector_res))

    def load_images(self):
        if self.img_ext == "npy":
            self.imgs = [np.load(path) for path in self.img_paths]
        else:
            self.imgs = [cv2.imread(path, cv2.COLOR_BGR2GRAY) for path in self.img_paths]
        self.img_size = (self.imgs[0]).shape[0]