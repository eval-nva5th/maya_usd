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
from loader_ui_v002 import UI
# from ui import login_view
from ui.login_ui import LoginView
 
if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginView()
    login_window.show()
    app.exec()

    # app = QApplication([])
    # print ("UI 인스턴스 생성 시작")
    # ui = UI() 
    # print ("UI 인스턴스 생성 완료")
    # ui.show() 
    # app.exec()