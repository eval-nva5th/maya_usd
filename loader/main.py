# try: 
#     from PySide2.QtWidgets import QApplication
# except Exception :
#     from PySide6.QtWidgets import QApplication

from loader.ui.login_ui import LoginWidget

def show_ui():
    """ UI를 실행하는 함수 """
    print("UI 인스턴스 생성 시작")
    ui = LoginWidget()
    ui.setFixedSize(400, 200)
    ui.show()
    print("UI 인스턴스 생성 완료")
    return ui  # UI 인스턴스 반환

if __name__ == "__main__":
    show_ui()