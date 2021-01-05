import cv2
import numpy as np
import importlib
from ProcessImage import PreProcessImages

if __name__ == '__main__':

    filename = '../assets/models/Rectangle.png'
    dim = (600, 600)
    img = cv2.resize(cv2.imread(filename), dim)

    # prepare main algorithm
    algo = PreProcessImages()

    # wrapped image
    wrapped, image_i = algo.fourPointTransform(img)

    # rect, wrapped = algo.getCorner(img)
    cv2.imshow('Original Image', img)
    cv2.imshow('wrapped', wrapped)
    cv2.imshow('Image Drawn', wrapped)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
