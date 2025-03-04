try :
    from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QApplication
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QMainWindow
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PySide2.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QApplication
        from PySide2.QtWidgets import QVBoxLayout, QLabel, QMainWindow
        from PySide2.QtCore import Qt
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
from data import previous_get_data
import data

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setFixedSize(1100, 800)
        self.setWindowTitle("EVAL_LOADER")

        # 중앙 위젯 설정
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # self.setCentralWidget(central_widget)  # QMainWindow의 중앙 위젯 설정

    def setup_layout(self): ####################################################### 수정 진행
        """
        레이아웃 세팅
        """
        from ui import make_task_table, make_file_table
        # 왼쪽 Task Table UI 생성
        task_container = make_task_table()
        task_container.setMinimumWidth(570)
        task_container.setMaximumWidth(570)  # TASK 최소 너비 지정, 안하면 너무 작아짐.
        task_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 가로/세로 확장 허용

        # WORK 버전 UI 생성
        work_container = make_file_table("WORK")
        work_label = QLabel("WORK")
        work_label.setStyleSheet("font-weight : bold;padding-left: 10px;")
        work_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        # # PUB 버전 UI 생성
        pub_container = make_file_table("PUB")
        pub_label = QLabel("PUB")
        pub_label.setStyleSheet("font-weight : bold;padding-left: 10px;")
        pub_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        # # PREVIOUS BLAST UI 생성
        previous_container = previous_get_data()
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # # 유저 레이아웃
        user_layout = QHBoxLayout()
        none_label = QLabel()
        user_name = QLabel(data.name_input.text())
        user_name.setStyleSheet("font-weight: bold;")
        user_name.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        user_name.setAlignment(Qt.AlignRight)
        user_layout.addWidget(none_label)
        user_layout.addWidget(user_name)

        # work, pub, pb, 유저이름 레이아웃 세팅
        right_layout = QVBoxLayout()
        right_layout.addLayout(user_layout)
        right_layout.addWidget(previous_container, 2)
        right_layout.addWidget(work_label)
        right_layout.addWidget(work_container, 2)
        right_layout.addWidget(pub_label)
        right_layout.addWidget(pub_container, 1)

        # 메인 레이아웃 세팅
        layout.addWidget(task_container, 3)
        layout.addLayout(right_layout, 2)

        return widget
    
    def center_window(self):
        frame_geometry = self.frameGeometry()  # 창의 프레임 가져오기
        screen = QApplication.primaryScreen()  # 현재 사용 중인 화면 가져오기
        screen_geometry = screen.availableGeometry().center()  # 화면의 중앙 좌표
        frame_geometry.moveCenter(screen_geometry)  # 창의 중심을 화면 중심으로 이동
        self.move(frame_geometry.topLeft())  # 최종적으로 창을 이동