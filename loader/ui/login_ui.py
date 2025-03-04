try :
    from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton,QVBoxLayout, QApplication
except ImportError:
    try:
        from PySide2.QtWidgets import QWidget, QLineEdit, QPushButton,QVBoxLayout, QApplication
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")

from event import on_login_click
import data

class LoginView(QWidget):
    """
    로그인 화면 UI
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 200)  # 로그인 창 크기 조절
        layout = QVBoxLayout(self)
        # 네임 임력
        data.name_input = QLineEdit("장순우") ################ 말풍선 제거하기
        #data.name_input.setPlaceholderText("NAME") # 흐릿한 글씨

        # 이메일 입력
        data.email_input = QLineEdit("f8d783@kw.ac.kr") ################ 말풍선 제거하기
        #data.email_input.setPlaceholderText("EMAIL") # 흐릿한 글씨
    
        # 엔터(RETURN) 키를 누르면 로그인 버튼 클릭과 동일하게 동작하도록 연결
        data.email_input.returnPressed.connect(on_login_click)
        data.name_input.returnPressed.connect(on_login_click)
        # 로그인 버튼
        login_btn = QPushButton("LOGIN")
        login_btn.clicked.connect(on_login_click)
            
        # 레이아웃 설정
        layout.addWidget(data.name_input)
        layout.addWidget(data.email_input)
        layout.addWidget(login_btn)

        self.center_window()

    def center_window(self):
        """ 창을 화면 중앙으로 이동하는 메서드 """
        frame_geometry = self.frameGeometry()  # 창의 현재 크기 가져오기
        screen = QApplication.primaryScreen().geometry()  # 현재 사용 중인 스크린의 크기
        screen_center = screen.center()  # 스크린 중앙 좌표
        frame_geometry.moveCenter(screen_center)  # 창의 중앙을 스크린 중앙으로 이동
        self.move(frame_geometry.topLeft())  # 실제 창 이동