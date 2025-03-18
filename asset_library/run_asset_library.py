try:
    from PySide2.QtWidgets import QApplication 
except Exception :
    from PySide6.QtWidgets import QApplication
import sys
from asset_library.ui.asset_library_ui import AssetLibUI

def run():
    asset_window = AssetLibUI()
    asset_window.show()

if __name__ == "__main__":
    app = QApplication()
    asset_window = AssetLibUI()
    asset_window.show()
    sys.exit(app.exec_())