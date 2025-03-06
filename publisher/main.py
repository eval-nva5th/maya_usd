try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    from PySide2.QtWidgets import QApplication
    import maya.cmds as cmds
from ui.publisher_ui import PublisherDialog
import sys

if __name__ == "__main__":
    app = QApplication()
    save_dialog = PublisherDialog()
    save_dialog.show()
    sys.exit(app.exec())