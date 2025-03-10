from PySide2.QtWidgets import QApplication

import sys 
sys.path.append("/home/rapa/gitkraken/maya_usd/save_as")

import core
import event
import ui
from ui.save_as_ui import SaveAsDialog

def run() : 
    #app = QApplication(sys.argv)
    save_dialog = SaveAsDialog()
    save_dialog.show()
    #sys.exit(app.exec_())

if __name__ == "__main__":
    run()