try:
    from PySide6.QtWidgets import QApplication
except:
    from PySide2.QtWidgets import QApplication

from ui.publisher_ui import PublisherDialog
import sys

def runrun():
    
    save_dialog = PublisherDialog()
    save_dialog.show()

if __name__ == "__main__":
    runrun()
