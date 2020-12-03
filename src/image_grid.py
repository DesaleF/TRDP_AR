import cv2 as cv
from matplotlib import pyplot as plt
image1 = cv.imread('result_samples/Lines Input_screenshot_17.11.2020.png')
image2 = cv.imread('result_samples/Lines Model_screenshot_17.11.2020.png')
plt.subplot(1, 2, 1)
plt.imshow(image1)
plt.subplot(1, 2, 2)
plt.imshow(image2)
plt.axis('off')
plt.show()