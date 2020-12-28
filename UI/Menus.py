from PyQt5.QtGui import QIcon


class AppMenu:
    def __init__(self, primaryWindow):
        super(AppMenu, self).__init__()

        # list of menu bars
        self.fileMenuBar = primaryWindow.menuBar().addMenu("&File")
        self.editMenuBar = primaryWindow.menuBar().addMenu("&Edit")

        # pencil and eraser
        self.brushSizeBar = primaryWindow.menuBar().addMenu("&Pencil Size")
        self.eraserSizeBar = primaryWindow.menuBar().addMenu("&Eraser Size")

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
        self.pencilButton.triggered.connect(primaryWindow.drawUsingPencil)

        # rectangle tool
        self.rectangleButton.setIcon(QIcon("./assets/icons/icons8-rectangle-50.png"))

        # Erase tool
        self.eraseButton.setShortcut("Ctrl+X")
        self.eraseButton.setIcon(QIcon("./assets/icons/icons8-eraser.png"))
        self.eraseButton.triggered.connect(primaryWindow.eraseDrawing)

        # lasso tool
        self.lassoButton.setShortcut("Ctrl+L")
        self.lassoButton.setIcon(QIcon("./assets/icons/icons8-lasso-tool-48.png"))

        # Stop Video button
        self.stopVideoButton.setShortcut('Ctrl+P')
        self.stopVideoButton.setIcon(QIcon("./assets/icons/icons8-stop-squared-50.png"))
        self.stopVideoButton.triggered.connect(primaryWindow.pauseDrawing)

        # start button
        self.startVideoButton.setShortcut('Ctrl+S')
        self.startVideoButton.setIcon(QIcon("./assets/icons/icons8-start-50.png"))
        self.startVideoButton.triggered.connect(primaryWindow.startVideo)

        # create menu bar to put some menu Options
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setIcon(QIcon("./assets/icons/open_file_icon.png"))
        self.actionOpen.triggered.connect(primaryWindow.openFileNamesDialog)

        # add exit option to exit the program(keyboard shortcut ctrl+q)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setIcon(QIcon("./assets/icons/icons8-exit-50.png"))
        self.actionExit.triggered.connect(primaryWindow.exitApp)

        # Pencil size menu
        self.threePxActionSize = self.brushSizeBar.addAction("3px")
        self.threePxActionSize.triggered.connect(lambda: primaryWindow.changePencilSize(3))
        self.threePxActionSize.setIcon(QIcon("./assets/icons/penSize/px3.png"))

        self.fivePxActionSize = self.brushSizeBar.addAction("5px")
        self.fivePxActionSize.triggered.connect(lambda: primaryWindow.changePencilSize(5))
        self.fivePxActionSize.setIcon(QIcon("./assets/icons/penSize/px5.png"))

        self.sevenPxActionSize = self.brushSizeBar.addAction("7px")
        self.sevenPxActionSize.triggered.connect(lambda: primaryWindow.changePencilSize(7))
        self.sevenPxActionSize.setIcon(QIcon("./assets/icons/penSize/px7.png"))

        self.ninePxActionSize = self.brushSizeBar.addAction("9px")
        self.ninePxActionSize.triggered.connect(lambda: primaryWindow.changePencilSize(9))
        self.ninePxActionSize.setIcon(QIcon("./assets/icons/penSize/px9.png"))

        # Eraser size menu
        self.erase10ActionSize = self.eraserSizeBar.addAction("10px")
        self.erase10ActionSize.triggered.connect(lambda: primaryWindow.changeEraserSize(10))
        self.erase10ActionSize.setIcon(QIcon("./assets/icons/penSize/px3.png"))

        self.erase20ActionSize = self.eraserSizeBar.addAction("20px")
        self.erase20ActionSize.triggered.connect(lambda: primaryWindow.changeEraserSize(20))
        self.erase20ActionSize.setIcon(QIcon("./assets/icons/penSize/px5.png"))

        self.erase30ActionSize = self.eraserSizeBar.addAction("30px")
        self.erase30ActionSize.triggered.connect(lambda: primaryWindow.changeEraserSize(30))
        self.erase30ActionSize.setIcon(QIcon("./assets/icons/penSize/px7.png"))

        self.erase40ActionSize = self.eraserSizeBar.addAction("40px")
        self.erase40ActionSize.triggered.connect(lambda: primaryWindow.changeEraserSize(40))
        self.erase40ActionSize.setIcon(QIcon("./assets/icons/penSize/px9.png"))
