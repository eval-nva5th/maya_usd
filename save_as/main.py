try : 
    from PySide2.QtWidgets import QApplication
except Exception :
    from PySide6.QtWidgets import QApplication

import sys
from save_as.ui.save_as_ui import SaveAsDialog
def run(ct):
    # app = QApplication(sys.argv)
    save_dialog = SaveAsDialog(ct)
    save_dialog.show()
    # sys.exit(app.exec_())
    return save_dialog

# if __name__ == "__main__":
# run()