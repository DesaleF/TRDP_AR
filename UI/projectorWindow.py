import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QDesktopWidget


# This UI serve as image display window for projector
# TODO:
class ProjectorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, transparent):
        super(ProjectorWindow, self).__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Secondary Window")
        self.label.setStyleSheet("background:transparent;")

        # create transparent layout
        layout.addWidget(self.label)
        self.setLayout(layout)

        # self.setStyleSheet("background:white;")
        if transparent:
            self.setAttribute(Qt.WA_TranslucentBackground)

        else:
            self.setStyleSheet("background:white;")

        # show the window on the second screen
        if QDesktopWidget.screenCount(QDesktopWidget()) > 1:
            monitor = QDesktopWidget().screenGeometry(1)
            self.move(monitor.left(), monitor.top())
        else:

            if not transparent:
                msg = QMessageBox()
                msg.setText('Projector Not detected. Thus the software will not work properly')

                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Error')
                msg.exec_()

        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)

        # to get the screen size
        for displayNr in range(QDesktopWidget().screenCount()):
            self.screen = QDesktopWidget().screenGeometry(displayNr)

        self.secHeight = self.screen.height()-20
        self.secWidth = self.screen.width()-20
        self.setMinimumSize(self.secWidth, self.secHeight)

        if not transparent:
            filename = './assets/models/Rectangle.png'
            dim = (self.secWidth, self.secHeight)

            img = cv2.resize(cv2.imread(filename), dim)
            _, _, channel = img.shape
            step = channel * self.secWidth

            qImg = QImage(img.data, self.secWidth, self.secHeight, step, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qImg))
