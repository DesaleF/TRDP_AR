from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


# this UI serve as image display window for projector
class ProjectorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Secondary Window")
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)

        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setStyleSheet("background:transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showMaximized()


