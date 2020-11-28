import sys
import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QPen, QCursor
from PyQt5.QtWidgets import QLabel, QMainWindow, QGridLayout, QApplication

# this UI serve as main window to draw the annotation
from UI.projectorWindow import ProjectorWindow


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'PROJECTION AR'
        self.left = 300
        self.top = 100
        # self.width = 1400
        # self.height = 900
        self.sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        self.secondaryWindow = ProjectorWindow()

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
        self.draw_pixmap = QPixmap(self.sizeObject.width()-20, self.sizeObject.height()-100)
        self.draw_pixmap.fill(Qt.transparent)
        self.painter = QPainter(self.draw_pixmap)
        self.annotation_label = QLabel(self)

        # custom drawing variables
        self.drawing = False
        self.brushSize = 6
        self.clear_size = 20
        self.brushColor = Qt.green
        self.lastPoint = QPoint()

        # cursor setting
        self.editCursor = QCursor(QPixmap("./assets/icons/cursor/icons8-edit-24.png"))
        self.eraseCursor = QCursor(QPixmap("./assets/icons/cursor/icons8-erase-28.png"))

        # 1. components of the UI
        self.createUIComponents()
        # 2. menu bar for file
        self.createMenu()
        # 3. Build UI
        self.buildUI()

    def buildUI(self):
        """

        """
        # window location and title
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width(), self.height())
        self.setWindowIcon(QIcon("../assets/icons/icon-green.png"))
        self.showMaximized()

        #  final layout.. all components together
        self.finalUi()

        # show the UI
        self.show()
        # create projector window
        self.secondaryWindow.show()

    def createUIComponents(self):
        """

        """
        # Main video label
        self.videoLabel = QLabel("Start Video", self)
        self.videoLabel.setFont(self.bold_font)
        # self.videoLabel.setStyleSheet("border: 1px solid black;")
        # self.change_button_status()

    def createMenu(self):
        """  Create and add menu items into menu bar
        """
        # list of menu bars
        self.fileMenuBar = self.menuBar().addMenu("File")
        self.editMenuBar = self.menuBar().addMenu("Edit")

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

    def finalUi(self):
        """

        """
        gridLayout = QGridLayout()

        # add widgets to the layout
        # gridLayout.addWidget(buttonGroup, 0, 0)
        gridLayout.addWidget(self.videoLabel, 0, 1, 1, 8)
        gridLayout.addWidget(self.annotation_label, 0, 1, 1, 8)

        # widget for the general layout
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(gridLayout)

    def startVideo(self):
        """  This will start the camera feed """
        try:
            # if timer is stopped
            if not self.timer.isActive():
                # create video capture  and start timer
                self.cap = cv2.VideoCapture(0)

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
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (self.sizeObject.width()-20, self.sizeObject.height()-100))

            # get image info
            height, width, channel = image.shape
            step = channel * width

            # create QImage and show it onto the label
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
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

    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "QtWidgets.QFileDialog.getOpenFileNames()",
            "", "Dicom Files (*.*)", options=options)
        if files:
            self.filePath = files[0]
            # go ahead and read the file if necessary

    # normal application exit
    def exitApp(self):
        if self.timer.isActive():
            self.cap.release()
        sys.exit(0)

    # add different events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.video_started:
            self.lastPoint = event.pos()
            self.lastPoint.setX(self.lastPoint.x() - 20)
            self.lastPoint.setY(self.lastPoint.y() - 15)

    def mouseMoveEvent(self, event):

        if (event.buttons() & Qt.LeftButton) and self.rect().contains(event.pos()):
            self.painter.setOpacity(0.9)
            currentPoint = event.pos()
            currentPoint.setX(currentPoint.x() - 20)
            currentPoint.setY(currentPoint.y() - 15)

            # drawing annotation
            if self.drawing:
                self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.painter.drawLine(self.lastPoint, currentPoint)

            # erasing the annotation
            elif self.erase_flag:
                r = QRect(QPoint(), self.clear_size*QSize())
                r.moveCenter(currentPoint)
                self.painter.save()

                self.painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
                self.painter.eraseRect(r)
                self.painter.restore()

            # set drawn annotation to the label and save last point
            self.annotation_label.setPixmap(self.draw_pixmap)
            self.lastPoint = currentPoint

            # update the paint in both screens
            self.secondaryWindow.label.setPixmap(self.draw_pixmap)
            self.secondaryWindow.label.resize(self.secondaryWindow.width(), self.secondaryWindow.height())
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


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(ex)
