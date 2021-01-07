import sys
from UI.PrimaryWindow import App
from PyQt5.QtWidgets import QApplication


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print("================================")
        print("Appplication couldn't start.")
        print("Error:" + ex)
        print("================================")





