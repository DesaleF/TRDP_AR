import cv2
import imutils
import numpy as np


#  this class is important to preprocess the image before displaying on labels
# for example perspective transform of the image from the projector
class PreProcessImages:
    def __init__(self):
        self.pts = None

    # Name:getCorners()
    # works: No
    # TODO:
    #   - extract four corners of the projected image from the projector
    def getCorner(self, image):
        """This will extract four corners
            :param
                image: full image from the camera
            :return
                rect: extract four corners
        """

        # initialize necessary variables
        rect = None
        ratio = image.shape[0] / 500.0
        image = imutils.resize(image, height=500)

        # convert the image to grayscale, blur it,
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # find edges in the image
        edged = cv2.Canny(gray, 75, 200)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if contour has four points, then we can assume that we have found our screen
            if len(approx) == 4:
                rect = approx
                break

        # save the contour (outline) of the projector screen
        print("STEP 2: Find contours of paper")
        cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)
        cv2.imwrite("Outline.png", image)
        return rect.reshape(4, 2) * ratio

    # Name:fourPointTransform()
    # works: No
    # TODO:
    #   - obtain a consistent order of the points and unpack them individually
    def fourPointTransform(self, image):
        """It will transform the detected corner displayable image
        :param
            - image: the full sized image
        :return
            - warped - transformed displayable image
        """

        # obtain a consistent order of the points and unpack them individually
        if self.pts is None:
            firstPts = self.getCorner(image)
            self.pts = self.orderPoints(firstPts)
        (tl, tr, br, bl) = self.pts

        # compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left
        # x-coordinates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct the set of destination points to obtain a
        # "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right,
        # bottom-right, and bottom-left order
        dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], np.float32)

        # compute the perspective transform matrix, apply it and return the warped image
        M = cv2.getPerspectiveTransform(self.pts, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        return warped

    # Name:orderPoints()
    # works: No
    # TODO:
    #   - order the points in the way we want to transform the points
    def orderPoints(self, firstPts):
        """Put the detected corner points in meaningful order
        order = [top-left, top-right, bottom-right, bottom-left]
        :param
            - firstPts: detected corners form the image
        :return
            -rect: correctly ordered corner points
        """

        # compute sum between points top-left point-> smallest sum, bottom-right point->largest sum
        rect = np.zeros((4, 2), dtype="float32")
        s = firstPts.sum(axis=1)
        rect[0] = firstPts[np.argmin(s)]
        rect[2] = firstPts[np.argmax(s)]

        # compute difference between points, top-right->smallest difference, bottom-left->largest difference
        diff = np.diff(firstPts, axis=1)
        rect[1] = firstPts[np.argmin(diff)]
        rect[3] = firstPts[np.argmax(diff)]

        # return the ordered coordinates
        return rect
