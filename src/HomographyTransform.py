import cv2
import numpy as np


# compute homography
def getHomography():
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

    return H


# apply image transform
def getHomographyTransform(H, image):
    width = image.shape[0]
    height = image.shape[1]
    transformedImage = cv2.warpPerspective(image, H, (height, width))
    return transformedImage


# put the following code into the mouseMoveEvent
# apply homography transform
# numpyImage = self.pixmapToArray(QPixmap(scaled_pixmap))
# H = self.getHomography()
# hImage = self.getHomographyTransform(H, numpyImage)
#
# # display the image
# # secImage = QPixmap.fromImage(hTransformed)
# image = QtGui.QImage(hImage, hImage.shape[1], hImage.shape[0], hImage.shape[1] * 3,QtGui.QImage.Format_RGB888)
# pix = QtGui.QPixmap(image)
