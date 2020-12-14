import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget


# this UI serve as image display window for projector
# TODO:
#   - Draw Colored Border on image label
class ProjectorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Secondary Window")
        self.label.setStyleSheet("background:white;")

        # create transparent layout
        layout.addWidget(self.label)
        self.setLayout(layout)
        # self.setStyleSheet("background:white;")
        self.setAttribute(Qt.WA_TranslucentBackground)

        # show the window on the second screen
        if QDesktopWidget.screenCount(QDesktopWidget()) > 1:
            monitor = QDesktopWidget().screenGeometry(1)
            self.move(monitor.left(), monitor.top())
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)

        # to get the screen size
        for displayNr in range(QDesktopWidget().screenCount()):
            self.screen = QDesktopWidget().screenGeometry(displayNr)
        self.secHeight = self.screen.height()-40
        self.secWidth = self.screen.width()-30
        self.setMinimumSize(self.secWidth, self.secHeight)

