from PySide2.QtWidgets import QApplication

import sys 
from ui.save_as_ui import SaveAsDialog

if __name__ == "__main__":
    app = QApplication()
    save_dialog = SaveAsDialog()
    save_dialog.show()
    sys.exit(app.exec())