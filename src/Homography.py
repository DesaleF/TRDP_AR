import cv2
from matplotlib import pyplot as plt
import numpy as np

MIN_MATCH_COUNT = 10
# import yaml


def main():
    img1 = cv2.imread('box.png', 0)  # queryImage
    img2 = cv2.imread('box_in_scene.png', 0)  # trainImage

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)


def opencv_matrix(loader, node):
    mapping = loader.construct_mapping(node)
    mat = np.array(mapping["data"])
    mat.resize(mapping["rows"], mapping["cols"])
    return mat



def loading_using_sci():
    import scipy.io
    mat = scipy.io.loadmat('../assets/tools/calibration.mat')
    print(mat['aplha_c_left'][0])


if __name__ == "__main__":

    try:
        K_cam = np.array([[1198.370216, 0.0000, 558.550289],
                          [0, 1217.432399, 303.112548],
                          [0, 0, 1]])

        K_proj = np.array([[1682.580944, 0.0000, 377.944090],
                           [0, 1592.522801, 259.182582],
                           [0, 0, 1]])

        T = np.array([-100.121874, -35.443266, 86.250559])

        R = np.array([[9.9753117267249736e-001, 2.4600138893772598e-002, 6.5775319938706903e-002],
                      [-2.5830952403295852e-002, 9.9950555626341375e-001, 1.7927768865717380e-002],
                      [-6.5301772139589140e-002, -1.9582547458668855e-002, 9.9767339464899940e-001]])
        H = K_proj * R * (np.linalg.inv(K_cam))

        print(H)
    except Exception as ex:
        print(ex)
