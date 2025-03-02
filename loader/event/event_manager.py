try :
    from PySide6.QtWidgets import QMessageBox
except ImportError:
    try:
        from PySide2.QtWidgets import QMessageBox
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
import data as login_data
from shotgrid_user_task import UserInfo
from ui.main_ui import MainView

def on_login_click():
    """
    로그인 버튼 실행
    """
    name = login_data.name_input.text()
    email = login_data.email_input.text()
    user = UserInfo(login_data.sg_url, login_data.script_name, login_data.api_key)

    if name and email: #이름과 이메일에 값이 있을 때
        is_validate = user.is_validate(email, name)
        print (f"is_validate : {is_validate}")
        if not is_validate:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("아이디 또는 이메일이 일치하지 않습니다")
            popup.exec()
        else:
            user_name = name
            main_window = MainView()
            main_window.show()
            main_window.resize(1100, 800)  # 메인 화면 크기 조정
            main_window.setCentralWidget(main_window.setup_layout()) # 로그인 창을 메인화면으로 변경
            main_window.center_window()
            print ("로그인 성공")

    else: # 이름과 이메일에 값이 없을 때
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle("Failure")
        popup.setText("이름과 이메일을 입력해주세요")
        popup.exec()