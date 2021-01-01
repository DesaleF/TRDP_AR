import sys
import cv2
import numpy as np

# pyqt modules
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QPen, QCursor
from PyQt5.QtWidgets import QLabel, QMainWindow, QGridLayout, QApplication, QVBoxLayout, QGroupBox, QMessageBox

# our modules
from UI.projectorWindow import ProjectorWindow
from src.Preprocess import PreProcessImages
from src.ProcessImage import PreProcessImages as PreProcessImagesV2

from UI.Menus import AppMenu
from UI.SideBar import SideBar


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'PROJECTION AR'
        self.left = 300
        self.top = 100
        self.camera = 0

        # offsets
        self.pointerOffsetX = 123
        self.pointerOffsetY = 63

        self.imageOffsetX = 250
        self.imageOffsetY = 200

        self.sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)

        # Flags
        self.video_started = False
        self.pencil_started = False
        self.erase_flag = False
        self.is_secondWindow = True
        self.secondTransparency = True

        # Objects
        self.secondaryWindow = ProjectorWindow(None)
        self.secondaryWindow_final = ProjectorWindow(self.secondTransparency)
        self.preProcessingTool = PreProcessImages()
        self.PreProcessImagesV2Tool = PreProcessImagesV2()

        # extra parameters
        self.timer = QTimer()
        self.cap = None
        self.filePath = None
        self.cursor = None

        # variable for annotation
        self.draw_pixmap = QPixmap(self.sizeObject.width() - self.imageOffsetX,
                                   self.sizeObject.height() - self.imageOffsetY)
        self.draw_pixmap.fill(Qt.transparent)
        self.painter = QPainter(self.draw_pixmap)
        self.annotation_label = QLabel(self)
        self.videoLabel = QLabel("Start Video", self)

        # custom drawing variables
        self.drawing = False
        self.brushSize = 6
        self.clear_size = 20
        self.brushColor = Qt.green
        self.lastPoint = QPoint()

        # cursor setting
        self.editCursor = QCursor(QPixmap("./assets/icons/cursor/icons8-edit-24.png"))
        self.eraseCursor = QCursor(QPixmap("./assets/icons/cursor/icons8-erase-28.png"))

        # add components to the window and build
        self.menus = AppMenu(self)
        self.sideBar = SideBar(self)

        self.finalUi(self.sideBar.toolsButtonGroupBox)
        self.buildUI()

    def buildUI(self):
        """

        """
        # window location and title
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width(), self.height())
        self.setWindowIcon(QIcon("./assets/icons/icon-green.png"))
        self.showMaximized()

        # create projector window
        self.show()
        self.secondaryWindow.show()

    def finalUi(self, buttonGroup):
        """

        """
        # button group box
        colorVBox = QGroupBox("Colors")
        colorVBox.setFixedWidth(45)
        colorVBox.setMaximumHeight(1000)

        # vertical layout
        colorVLayout = QVBoxLayout()
        colorVLayout.setSpacing(0)
        colorVLayout.setContentsMargins(0, 0, 0, 0)
        self.add_palette_buttons(colorVLayout)

        # set the layout to the button group
        colorVBox.setLayout(colorVLayout)

        gridLayout = QGridLayout()

        # add widgets to the layout
        gridLayout.addWidget(buttonGroup, 0, 0)
        gridLayout.addWidget(self.videoLabel, 0, 1)
        gridLayout.addWidget(self.annotation_label, 0, 1)
        gridLayout.addWidget(colorVBox, 0, 2)

        # widget for the general layout
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(gridLayout)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda clr=c: self.set_pen_color(clr))
            layout.addWidget(b)

    def set_pen_color(self, c):
        self.brushColor = QtGui.QColor(c)

    def startVideo(self):
        """  This will start the camera feed """
        try:
            # if timer is stopped
            if not self.timer.isActive():
                self.cap = cv2.VideoCapture(self.camera)

                self.videoLabel.setText("Connecting to camera")
                self.video_started = True

                # set timer timeout callback function
                self.timer.timeout.connect(self.displayImage)
                self.timer.start(100)

        except Exception as expt:
            print('error in function startVideo')
            print(expt)

    def pauseDrawing(self):
        """ stop both plotting and erasing """
        if self.timer.isActive():
            self.drawing = False
            self.erase_flag = False
            QApplication.setOverrideCursor(Qt.UpArrowCursor)

        else:
            self.videoLabel.setText('Camera is not started')

    def displayImage(self):
        """ This function read the camera and display the image
        """
        try:
            # read form camera
            ret, image = self.cap.read()
            raw_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            wrapped = self.preProcessingTool.fourPointTransform(raw_image)

            #  recreate the second window
            if self.is_secondWindow:
                self.secondaryWindow.close()
                self.secondaryWindow_final.show()
                self.is_secondWindow = False

            wrapped = cv2.resize(wrapped,
                                 (self.sizeObject.width() - self.imageOffsetX,
                                  self.sizeObject.height() - self.imageOffsetY))
            # get image info
            height, width, channel = wrapped.shape
            step = channel * width

            # create QImage and show it onto the label
            qImg = QImage(wrapped.data, width, height, step, QImage.Format_RGB888)
            self.videoLabel.setPixmap(QPixmap.fromImage(qImg))

        except cv2.error as exc:
            print(exc)
            msg = QMessageBox()
            msg.setText('No camera is detected')

            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Error')
            msg.exec_()

            self.timer.stop()
            self.timer.disconnect()

            self.video_started = True
            self.videoLabel.setText('Camera is not connected')

    def drawUsingPencil(self):

        # change the cursor to pencil
        if self.video_started:
            self.menus.startVideoButton.setEnabled(False)
            QApplication.setOverrideCursor(self.editCursor)
            self.drawing = True

    def eraseDrawing(self):
        if self.video_started:
            self.erase_flag = True
            QApplication.setOverrideCursor(self.eraseCursor)
            self.drawing = False

    # pencil size
    def changePencilSize(self, penSize):
        self.brushSize = penSize

    # Eraser Size
    def changeEraserSize(self, brushSize):
        self.clear_size = brushSize

    # open file to load image
    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "QtWidgets.QFileDialog.getOpenFileNames()",
            "", "png Files (*.png)", options=options)
        if files:
            self.filePath = files[0]
            # go ahead and read the file if necessary

    def pixmapToArray(self, pixmap):
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

    # normal application exit
    def exitApp(self):
        if self.timer.isActive():
            self.cap.release()
        sys.exit(0)

    # add different events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.video_started:
            self.lastPoint = event.pos()
            self.lastPoint.setX(self.lastPoint.x() - self.pointerOffsetX)
            self.lastPoint.setY(self.lastPoint.y() - self.pointerOffsetY)

    # mouseMoveEvent(self, event)
    # Works: yes
    # TODO:
    def mouseMoveEvent(self, event):

        if (event.buttons() & Qt.LeftButton) and self.rect().contains(event.pos()):
            self.painter.setOpacity(0.9)
            currentPoint = event.pos()
            currentPoint.setX(currentPoint.x() - self.pointerOffsetX)
            currentPoint.setY(currentPoint.y() - self.pointerOffsetY)

            # drawing annotation
            if self.drawing:
                self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.painter.drawLine(self.lastPoint, currentPoint)

            # erasing the annotation
            elif self.erase_flag:
                r = QRect(QPoint(), self.clear_size * QSize())
                r.moveCenter(currentPoint)
                self.painter.save()

                self.painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
                self.painter.eraseRect(r)
                self.painter.restore()

            # set drawn annotation to the label and save last point
            self.annotation_label.setPixmap(self.draw_pixmap)
            self.lastPoint = currentPoint

            # update the paint in both screens
            scaled_pixmap = self.draw_pixmap.scaled(self.secondaryWindow_final.secWidth,
                                                    self.secondaryWindow_final.secHeight,
                                                    Qt.IgnoreAspectRatio, Qt.FastTransformation)

            self.secondaryWindow_final.label.setPixmap(scaled_pixmap)
            self.update()

    # highlight
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.video_started:
            # self.drawing = False
            self.save()

    def save(self):
        try:
            filePath = 'annotation.png'
            self.draw_pixmap.save(filePath)
        except Exception as ex:
            print(ex)


COLORS = [
    # 17 undertones https://lospec.com/palette-list/17undertones
    '#000000', '#00ff00', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
    '#458352', '#dcd37b', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super(QPaletteButton, self).__init__()
        self.setFixedSize(QtCore.QSize(40, 40))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)