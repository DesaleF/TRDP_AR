from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout


class SideBar:
    def __init__(self, primaryWindow):
        super(SideBar, self).__init__()

        # button group box
        self.toolsButtonGroupBox = QGroupBox("Tools")
        self.toolsButtonGroupBox.setFixedWidth(100)
        self.toolsButtonGroupBox.setMaximumHeight(450)

        # side Button
        self.sideStartButton = QtWidgets.QToolButton(primaryWindow)
        self.sideDrawButton = QtWidgets.QToolButton(primaryWindow)

        self.sideEraseButton = QtWidgets.QToolButton(primaryWindow)
        self.sidePauseButton = QtWidgets.QToolButton(primaryWindow)
        self.sideExitButton = QtWidgets.QToolButton(primaryWindow)

        # vertical layout
        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(1, 0, 0, 1)
        sideButtonSize = QtCore.QSize(90, 77)

        # side Button process
        self.sideStartButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideStartButton.setIcon(QIcon('./assets/icons/SideButton/sidePlayIcon.png'))
        self.sideStartButton.released.connect(primaryWindow.startVideo)
        self.sideStartButton.setIconSize(sideButtonSize)

        self.sideDrawButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideDrawButton.setIcon(QIcon('./assets/icons/SideButton/sideEditIcon.png'))
        self.sideDrawButton.released.connect(primaryWindow.drawUsingPencil)
        self.sideDrawButton.setIconSize(sideButtonSize)

        self.sideEraseButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideEraseButton.setIcon(QIcon('./assets/icons/SideButton/sideEraseIcon.png'))
        self.sideEraseButton.released.connect(primaryWindow.eraseDrawing)
        self.sideEraseButton.setIconSize(sideButtonSize)

        self.sidePauseButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sidePauseButton.setIcon(QIcon('./assets/icons/SideButton/sidePauseIcon.png'))
        self.sidePauseButton.released.connect(primaryWindow.pauseDrawing)
        self.sidePauseButton.setIconSize(sideButtonSize)

        self.sideExitButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.sideExitButton.setIcon(QIcon('./assets/icons/SideButton/sideExitIcon.png'))
        self.sideExitButton.released.connect(primaryWindow.exitApp)
        self.sideExitButton.setIconSize(sideButtonSize)

        # group the UI components
        vLayout.addWidget(self.sideStartButton)
        vLayout.addWidget(self.sideDrawButton)
        vLayout.addWidget(self.sideEraseButton)

        vLayout.addWidget(self.sidePauseButton)
        vLayout.addWidget(self.sideExitButton)
        self.toolsButtonGroupBox.setLayout(vLayout)

