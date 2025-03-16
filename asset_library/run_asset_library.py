from PySide2.QtWidgets import QApplication
import sys
from asset_library.ui.asset_library_ui import AssetLibUI
def run():
    # app = QApplication()
    asset_window = AssetLibUI()
    asset_window.show()
    # sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication()
    asset_window = AssetLibUI()
    asset_window.show()
    sys.exit(app.exec_())