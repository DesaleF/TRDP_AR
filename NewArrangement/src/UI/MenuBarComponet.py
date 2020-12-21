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


class MenuBar(QtWidgets):

    def __init__(self):
        super('MenuCom')
    """

    """

    """
    """
    def createMenu(self):

        """  Create and add menu items into menu bar
        """
        # list of menu bars
        self.fileMenuBar = self.menuBar().addMenu("&File")
        self.editMenuBar = self.menuBar().addMenu("&Edit")
        self.brushSizeBar = self.menuBar().addMenu("&Pencil Size")
        self.eraserSizeBar = self.menuBar().addMenu("&Eraser Size")

        # file menu Bar components
        self.startVideoButton = self.fileMenuBar.addAction("Strat Video")
        self.actionExit = self.fileMenuBar.addAction("Exit")
        self.actionOpen = self.fileMenuBar.addAction("Open File")

        # edit menu bar components
        self.pencilButton = self.editMenuBar.addAction("Draw")
        self.stopVideoButton = self.editMenuBar.addAction("Pause")
        self.eraseButton = self.editMenuBar.addAction("Erase")
        self.lassoButton = self.editMenuBar.addAction("Lasso")
        self.rectangleButton = self.editMenuBar.addAction("Select")

        # Pencil tool
        self.pencilButton.setIcon(QIcon("./assets/icons/icons8-pencil-50.png"))
        self.pencilButton.triggered.connect(self.drawUsingPencil)

        # rectangle tool
        self.rectangleButton.setIcon(QIcon("./assets/icons/icons8-rectangle-50.png"))

        # Erase tool
        self.eraseButton.setShortcut("Ctrl+X")
        self.eraseButton.setIcon(QIcon("./assets/icons/icons8-eraser.png"))
        self.eraseButton.triggered.connect(self.eraseDrawing)

        # lasso tool
        self.lassoButton.setShortcut("Ctrl+L")
        self.lassoButton.setIcon(QIcon("./assets/icons/icons8-lasso-tool-48.png"))

        # Stop Video button
        self.stopVideoButton.setShortcut('Ctrl+P')
        self.stopVideoButton.setIcon(QIcon("./assets/icons/icons8-stop-squared-50.png"))
        self.stopVideoButton.triggered.connect(self.pauseDrawing)

        # start button
        self.startVideoButton.setShortcut('Ctrl+S')
        self.startVideoButton.setIcon(QIcon("./assets/icons/icons8-start-50.png"))
        self.startVideoButton.triggered.connect(self.startVideo)

        # create menu bar to put some menu Options
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setIcon(QIcon("./assets/icons/open_file_icon.png"))
        self.actionOpen.triggered.connect(self.openFileNamesDialog)

        # add exit option to exit the program(keyboard shortcut ctrl+q)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setIcon(QIcon("./assets/icons/icons8-exit-50.png"))
        self.actionExit.triggered.connect(self.exitApp)

        # Pencil size menu
        self.threepxActionSize = self.brushSizeBar.addAction("3px")
        self.threepxActionSize.triggered.connect(self.threePixel)
        self.threepxActionSize.setIcon(QIcon("./assets/icons/penSize/px3.png"))

        self.fivepxActionSize = self.brushSizeBar.addAction("5px")
        self.fivepxActionSize.triggered.connect(self.fivePixel)
        self.fivepxActionSize.setIcon(QIcon("./assets/icons/penSize/px5.png"))

        self.sevenpxActionSize = self.brushSizeBar.addAction("7px")
        self.sevenpxActionSize.triggered.connect(self.sevenPixel)
        self.sevenpxActionSize.setIcon(QIcon("./assets/icons/penSize/px7.png"))

        self.ninepxActionSize = self.brushSizeBar.addAction("9px")
        self.ninepxActionSize.triggered.connect(self.ninePixel)
        self.ninepxActionSize.setIcon(QIcon("./assets/icons/penSize/px9.png"))

        # Eraser size menu
        self.erase10ActionSize = self.eraserSizeBar.addAction("10px")
        self.erase10ActionSize.triggered.connect(self.eraserSize10)
        self.erase10ActionSize.setIcon(QIcon("./assets/icons/penSize/px3.png"))

        self.erase20ActionSize = self.eraserSizeBar.addAction("20px")
        self.erase20ActionSize.triggered.connect(self.eraserSize20)
        self.erase20ActionSize.setIcon(QIcon("./assets/icons/penSize/px5.png"))

        self.erase30ActionSize = self.eraserSizeBar.addAction("30px")
        self.erase30ActionSize.triggered.connect(self.eraserSize30)
        self.erase30ActionSize.setIcon(QIcon("./assets/icons/penSize/px7.png"))

        self.erase40ActionSize = self.eraserSizeBar.addAction("40px")
        self.erase40ActionSize.triggered.connect(self.eraserSize40())
        self.erase40ActionSize.setIcon(QIcon("./assets/icons/penSize/px9.png"))

