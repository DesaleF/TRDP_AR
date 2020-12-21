import sys
import cv2
import traceback
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QPen, QCursor
from PyQt5.QtWidgets import QLabel, QMainWindow, QGridLayout, QApplication, QVBoxLayout, QGroupBox

# our packages
from UI.projectorWindow import ProjectorWindow
from src.Preprocess import PreProcessImages
from src.ProcessImage import PreProcessImages as PreProcessImagesV2


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'PROJECTION AR'
        self.left = 300
        self.top = 100
        self.camera = 2

        # offsets
        self.pointerOffsetX = 123
        self.pointerOffsetY = 63
        self.imageOffsetX = 250
        self.imageOffsetY = 200
        self.is_secondWindow = True
        self.secondTransparncy = True

        self.sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        self.secondaryWindow = ProjectorWindow(None)
        self.secondaryWindow_final = ProjectorWindow(self.secondTransparncy)
        self.preProcessingTool = PreProcessImages()
        self.PreProcessImagesV2Tool = PreProcessImagesV2()

        # Flags
        self.video_started = False
        self.pencil_started = False
        self.erase_flag = False

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

        # side Button
        self.sideStartButton = QtWidgets.QToolButton(self)
        self.sideDrawButton = QtWidgets.QToolButton(self)
        self.sideEraseButton = QtWidgets.QToolButton(self)
        self.sidePauseButton = QtWidgets.QToolButton(self)
        self.sideExitButton = QtWidgets.QToolButton(self)

        # menu bar for file
        self.createMenu()
        # Build UI
        self.buildUI()

    def buildUI(self):
        """

        """
        # window location and title
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width(), self.height())
        self.setWindowIcon(QIcon("./assets/icons/icon-green.png"))
        self.showMaximized()
        sideButtonSize = QtCore.QSize(85, 55)

        # side Button process
        self.sideStartButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideStartButton.setIcon(QIcon('./assets/icons/SideButton/sidePlayIcon.png'))
        self.sideStartButton.released.connect(self.startVideo)
        self.sideStartButton.setIconSize(sideButtonSize)

        self.sideDrawButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideDrawButton.setIcon(QIcon('./assets/icons/SideButton/sideEditIcon.png'))
        self.sideDrawButton.released.connect(self.drawUsingPencil)
        self.sideDrawButton.setIconSize(sideButtonSize)

        self.sideEraseButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideEraseButton.setIcon(QIcon('./assets/icons/SideButton/sideEraseIcon.png'))
        self.sideEraseButton.released.connect(self.eraseDrawing)
        self.sideEraseButton.setIconSize(sideButtonSize)

        self.sidePauseButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sidePauseButton.setIcon(QIcon('./assets/icons/SideButton/sidePauseIcon.png'))
        self.sidePauseButton.released.connect(self.pauseDrawing)
        self.sidePauseButton.setIconSize(sideButtonSize)

        self.sideExitButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideExitButton.setIcon(QIcon('./assets/icons/SideButton/sideExitIcon.png'))
        self.sideExitButton.released.connect(self.exitApp)
        self.sideExitButton.setIconSize(sideButtonSize)

        # group the UI components
        buttonGroup = self.groupcomponents()

        #  final layout.. all components together
        self.finalUi(buttonGroup)

        # show the UI
        self.show()
        # create projector window
        self.secondaryWindow.show()

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
        self.threepxActionSize.triggered.connect(lambda: self.changePencilSize(3))
        self.threepxActionSize.setIcon(QIcon("./assets/icons/penSize/px3.png"))

        self.fivepxActionSize = self.brushSizeBar.addAction("5px")
        self.fivepxActionSize.triggered.connect(lambda: self.changePencilSize(5))
        self.fivepxActionSize.setIcon(QIcon("./assets/icons/penSize/px5.png"))

        self.sevenpxActionSize = self.brushSizeBar.addAction("7px")
        self.sevenpxActionSize.triggered.connect(lambda: self.changePencilSize(7))
        self.sevenpxActionSize.setIcon(QIcon("./assets/icons/penSize/px7.png"))

        self.ninepxActionSize = self.brushSizeBar.addAction("9px")
        self.ninepxActionSize.triggered.connect(lambda: self.changePencilSize(9))
        self.ninepxActionSize.setIcon(QIcon("./assets/icons/penSize/px9.png"))

        # Eraser size menu
        self.erase10ActionSize = self.eraserSizeBar.addAction("10px")
        self.erase10ActionSize.triggered.connect(lambda: self.changeEraserSize(10))
        self.erase10ActionSize.setIcon(QIcon("./assets/icons/penSize/px3.png"))

        self.erase20ActionSize = self.eraserSizeBar.addAction("20px")
        self.erase20ActionSize.triggered.connect(lambda: self.changeEraserSize(20))
        self.erase20ActionSize.setIcon(QIcon("./assets/icons/penSize/px5.png"))

        self.erase30ActionSize = self.eraserSizeBar.addAction("30px")
        self.erase30ActionSize.triggered.connect(lambda: self.changeEraserSize(30))
        self.erase30ActionSize.setIcon(QIcon("./assets/icons/penSize/px7.png"))

        self.erase40ActionSize = self.eraserSizeBar.addAction("40px")
        self.erase40ActionSize.triggered.connect(lambda: self.changeEraserSize(40))
        self.erase40ActionSize.setIcon(QIcon("./assets/icons/penSize/px9.png"))

    def groupcomponents(self):
        """

        """
        # button group box
        toolsButtonGroupBox = QGroupBox("Tools")
        toolsButtonGroupBox.setFixedWidth(100)
        toolsButtonGroupBox.setMaximumHeight(450)

        # vertical layout
        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(1, 0, 0, 1)

        vLayout.addWidget(self.sideStartButton)
        vLayout.addWidget(self.sideDrawButton)
        vLayout.addWidget(self.sideEraseButton)
        vLayout.addWidget(self.sidePauseButton)
        vLayout.addWidget(self.sideExitButton)

        # set the layout to the button group
        toolsButtonGroupBox.setLayout(vLayout)
        return toolsButtonGroupBox

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
            b.pressed.connect(lambda c=c: self.set_pen_color(c))
            layout.addWidget(b)

    def set_pen_color(self, c):
        self.brushColor = QtGui.QColor(c)

    def startVideo(self):
        """  This will start the camera feed """
        try:
            # if timer is stopped
            if not self.timer.isActive():
                # create video capture  and start timer
                self.cap = cv2.VideoCapture(self.camera)

                self.videoLabel.setText("Connecting to camera")
                self.video_started = True
                # self.change_button_status()
                # set timer timeout callback function
                self.timer.timeout.connect(self.displayImage)
                self.timer.start(100)

        except Exception as ex:
            print(ex)

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

            wrapped = cv2.resize(wrapped, (
            self.sizeObject.width() - self.imageOffsetX, self.sizeObject.height() - self.imageOffsetY))
            # get image info
            height, width, channel = wrapped.shape
            step = channel * width

            # create QImage and show it onto the label
            qImg = QImage(wrapped.data, width, height, step, QImage.Format_RGB888)
            self.videoLabel.setPixmap(QPixmap.fromImage(qImg))

        except Exception as exc:
            print(exc)

    def drawUsingPencil(self):

        # change the cursor to pencil
        if self.video_started:
            self.startVideoButton.setEnabled(False)
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
        qimg = pixmap.toImage()
        s = qimg.bits().asstring(w * h * channels_count)
        img = np.fromstring(s, dtype=np.uint8).reshape((w, h, channels_count))

        return img

    # compute homography
    def getHomography(self):
        K_cam = np.array([[1198.370216, 0.0000, 558.550289],
                          [0, 1217.432399, 303.112548],
                          [0, 0, 1]])

        K_proj = np.array([[1682.580944, 0.0000, 377.944090],
                           [0, 1592.522801, 259.182582],
                           [0, 0, 1]])

        T = np.array([-100.121874, -35.443266, 86.250559])

        R = np.array([[9.9753117267249736e-001, 2.4600138893772598e-002, 6.5775319938706903e-002],
                      [-2.5830952403295852e-002, 9.9950555626341375e-001, 1.7927768865717380e-002],
                      [-6.5301772139589140e-002, -1.9582547458668855e-002, 9.9767339464899940e-001]])
        H = K_proj * R * (np.linalg.inv(K_cam))

        return H

    # apply image transform
    def getHomographyTransform(self, H, image):

        width = image.shape[0]
        height = image.shape[1]
        transformedImage = cv2.warpPerspective(image, H, (height, width))
        return transformedImage

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

    # mouseMoveEvent(sefl, event)
    # Works: yes
    # TODO:
    #   - rise the annotation image as size(secondScreen.width, secondScreen.height)
    #   - resize secondary image to fit the screen
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

            # apply homography transform
            # numpyImage = self.pixmapToArray(QPixmap(scaled_pixmap))
            # H = self.getHomography()
            # hImage = self.getHomographyTransform(H, numpyImage)
            #
            # # display the image
            # # secImage = QPixmap.fromImage(hTransformed)
            # image = QtGui.QImage(hImage, hImage.shape[1], hImage.shape[0], hImage.shape[1] * 3,QtGui.QImage.Format_RGB888)
            # pix = QtGui.QPixmap(image)
            self.secondaryWindow_final.label.setPixmap(scaled_pixmap)
            # self.secondaryWindow_final.label.resize(self.secondaryWindow_final.width(), self.secondaryWindow_final.height())
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
    '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(ex)
        traceback.print_exc()
