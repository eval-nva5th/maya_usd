try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    from PySide2.QtWidgets import QApplication
    #import maya.cmds as cmds
import sys
from ui.loader_ui import UI
from ui.login_ui import LoginWidget

sys.path.append("/home/rapa/gitkraken/maya_usd/loader")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/core")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/event")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/ui")

# # app = QApplication.instance()  # 기존 인스턴스를 가져오기
# # if not app:
# #     app = QApplication([])  # 없으면 새로 생성

# def show_ui():
#     """ UI를 실행하는 함수 """
#     print("UI 인스턴스 생성 시작")
#     ui = UI()
#     ui.setFixedSize(400, 200)
#     print("UI 인스턴스 생성 완료")
#     ui.show()
#     return ui  # UI 인스턴스 반환

# if __name__ == "__main__":
#     show_ui()
# ---------------------------------------------------------------확인용 프로그램 실행 후 나중에 지우고 위에 코드 활성화.
app = QApplication()  # QApplication을 먼저 생성해야 함

if __name__ == "__main__":
    widget = LoginWidget()
    widget.setFixedSize(400, 200)
    widget.show()

    sys.exit(app.exec())