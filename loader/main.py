try :
    from PySide6.QtWidgets import QApplication
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication
        from datetime import datetime
        import re
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")

from ui.login_ui import LoginView
import data

if __name__ == "__main__":
    app = QApplication([])
    data.loginView = LoginView()
    data.loginView.show()
    app.exec()