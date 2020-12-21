import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QPen, QCursor
from PyQt5.QtWidgets import QLabel, QMainWindow, QGridLayout, QApplication, QVBoxLayout, QGroupBox

# our packages
from UI.projectorWindow import ProjectorWindow
from src.Preprocess import PreProcessImages


class App(QMainWindow):
    """
     This class composes all various components of the application
     Compoents : Menu bar , right side tool box
     Application :


    """
    def __init__(self):
        super(App).__init__()

        # The compoenents
        self.MenuCompoenet = None
        self.SideBarCompoenet = None
        self.VideoComponent = None

        # Procedures