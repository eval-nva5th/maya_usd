from PySide2.QtWidgets import QApplication

import sys
print(sys.path)
from asset_library.ui.asset_library_ui import AssetLibUI
def run():
    app = QApplication()
    asset_window = AssetLibUI()
    asset_window.show()
    sys.exit(app.exec_())
run()