from PySide2.QtWidgets import QApplication
from publisher.ui.publisher_ui import PublisherDialog
import sys

def run():
    #app = QApplication()
    save_dialog = PublisherDialog()
    save_dialog.show()
    #sys.exit(app.exec_())

if __name__ == "__main__":
    run()
