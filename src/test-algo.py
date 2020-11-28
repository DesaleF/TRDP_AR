import cv2
import numpy as np
import importlib
from src import Algorithm

if __name__ == '__main__':

    filename = '../assets/models/with_bordeaux_background.png'
    dim = (600, 600)
    img = cv2.resize(cv2.imread(filename), dim)

    print(img.shape)

    # prepare main algorithm
    tool = Algorithm.mainAlgorithm(img, desc="Main algorithm")       # create this function

    blue_channel = tool.based_on_green_channel()
    # display results
    cv2.imshow('Original Image', img)
    cv2.imshow('From edge corner points', blue_channel)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
