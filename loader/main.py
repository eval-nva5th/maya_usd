import sys
sys.path.append("/home/rapa/gitkraken/maya_usd/loader")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/core")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/event")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/ui")
sys.path.append("/home/rapa/gitkraken/maya_usd/widget/ui")

from PySide2.QtWidgets import QApplication

from ui.loader_ui import UI
from ui.login_ui import LoginWidget



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
# ---------------------------------------------------------------로그인 위젯으로 변경함.
def show_ui():
    """ UI를 실행하는 함수 """
    print("UI 인스턴스 생성 시작")
    ui = LoginWidget()
    ui.setFixedSize(400, 200)
    print("UI 인스턴스 생성 완료")
    ui.show()
    return ui  # UI 인스턴스 반환

if __name__ == "__main__":
    show_ui()