import cv2
import numpy as np
import importlib
from skimage.metrics import structural_similarity

from src.LineDetector import LineDetector

if __name__ == '__main__':

    # read the image using opencv
    data_input = '../assets/models/projected.jpg'
    model = '../assets/models/blue-greed.png'

    dim = (600, 440)
    img_in = cv2.resize(cv2.imread(data_input), dim)
    img_in_gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)

    model_in = cv2.resize(cv2.imread(model), dim)

    # copy image and model
    input_image = img_in.copy()
    model_image = model_in.copy()

    # create line detector Instance
    detector = LineDetector("Line detector")

    # 1. Get only Green
    green_only = detector.get_only_one_color(input_image)
    green_only_copy = green_only.copy()
    green_only = cv2.cvtColor(green_only_copy, cv2.COLOR_BGR2GRAY)
    (thresh, green_only_binary) = cv2.threshold(green_only, 100, 255, cv2.THRESH_BINARY)

    # 2. get edge detection
    edges = detector.auto_canny(green_only_binary)
    edges_copy = edges.copy()

    # 3. detect lines
    line_detected, image_of_lines = detector.apply_line_detection(edges_copy)

    morphological = detector.erode_edges(image_of_lines)

    # 4. detect corners
    corners = detector.get_final_result(green_only)

    # 5. Morphological

    # Display results
    cv2.imshow('Original', img_in)
    cv2.imshow('Edge', edges)
    cv2.imshow('GREEN ONLY', green_only_copy)
    cv2.imshow('GREEN ONLY binary',     green_only_binary)
    cv2.imshow('GREEN ONLY morpholog',  morphological)
    cv2.imshow('corner',       corners)
    # cv2.imshow('Corner', corners)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
