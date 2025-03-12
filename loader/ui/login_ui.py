
from PySide2.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QApplication
import maya.cmds as cmds

from event.event_handler import on_login_clicked

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        로그인 화면 UI 초기화
        """
        layout = QVBoxLayout(self)

        # 네임 입력
        self.name_input = QLineEdit("장순우")  # 말풍선 제거 (기본값 설정)
        # self.name_input.setPlaceholderText("NAME") # 흐릿한 글씨
        
        # 이메일 입력
        self.email_input = QLineEdit("f8d783@kw.ac.kr")  # 말풍선 제거
        # self.email_input.setPlaceholderText("EMAIL") # 흐릿한 글씨

        # 엔터(RETURN) 키를 누르면 로그인 버튼 클릭과 동일하게 동작
        self.email_input.returnPressed.connect(lambda:on_login_clicked(self))
        self.name_input.returnPressed.connect(lambda:on_login_clicked(self))

        # 로그인 버튼
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.clicked.connect(lambda:on_login_clicked(self))

        # 레이아웃 설정
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.login_btn)

        self.center_window()

    def center_window(self):
        """주어진 위젯을 화면 중앙으로 이동"""
        screen_geometry = QApplication.primaryScreen().geometry()  # 화면 전체 크기 가져오기
        widget_geometry = self.frameGeometry()  # 현재 위젯 크기 가져오기
        center_point = screen_geometry.center()  # 화면 중앙 좌표
        widget_geometry.moveCenter(center_point)  # 창의 중심을 화면 중앙으로 설정
        self.move(widget_geometry.topLeft())