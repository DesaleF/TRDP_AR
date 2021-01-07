import sys
from UI.PrimaryWindow import App
from PyQt5.QtWidgets import QApplication
from src.utils.utils import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec_())
    except ModuleNotFoundError:
        show_error_dialog("Module Not found" + ModuleNotFoundError.__name__)
    except Exception as general_exception:
        show_error_dialog(general_exception)