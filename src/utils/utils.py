""""
This file contains different generic utility functions
"""
from PyQt5.QtWidgets import QMessageBox

from src.config.config import *
import numpy as np


def detect_camera():
    """ checks if camera is attached
    :return:  VidoeCaputer object and Ture - if successfull , else none and false
    """
    try:
        for cam in CAMERA:

            cap = cv2.VideoCapture(cam)
            if not (cap is None or not cap.isOpened()):
                return cap, True
            return None, False
    except Exception as ex:
        return None, False


def show_error_dialog(message):
    """
    Creates error pop up with ok button
    :param message: message sent to the dialog
    :return: QMessageBox
    """
    msg = QMessageBox()
    msg.setText(message)

    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle('Error Occoured')
    msg.exec_()

    def pixmapToArray(pixmap):
        """
        Converts PixelMap to numpy array
        :param pixmap:
        :return:  numpy array
        """
        # Get the size of the current pixmap
        size = pixmap.size()
        h = size.width()
        w = size.height()
        channels_count = 4

        # Get the QImage Item and convert it to a byte string
        qImg = pixmap.toImage()
        s = qImg.bits().asstring(w * h * channels_count)
        img = np.fromstring(s, dtype=np.uint8).reshape((w, h, channels_count))

        return img
