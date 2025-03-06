try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    from PySide2.QtWidgets import QApplication
    import maya.cmds as cmds
try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    from PySide2.QtWidgets import QApplication
    import maya.cmds as cmds

from ui.loader_ui import UI

# 기존 QApplication 확인 후 생성
app = QApplication.instance()  # 기존 인스턴스를 가져오기
if not app:
    app = QApplication([])  # 없으면 새로 생성

def show_ui():
    """ UI를 실행하는 함수 """
    print("UI 인스턴스 생성 시작")
app = QApplication.instance()  # 기존 인스턴스를 가져오기
if not app:
    app = QApplication([])  # 없으면 새로 생성

def show_ui():
    """ UI를 실행하는 함수 """
    print("UI 인스턴스 생성 시작")
    ui = UI()
    ui.setFixedSize(400, 200)
    print("UI 인스턴스 생성 완료")
    ui.show()
    return ui  # UI 인스턴스 반환

# if __name__ == "__main__":
#     show_ui()
#     app.exec()
