try :
    from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTableWidgetItem
    from PySide6.QtGui import QPixmap, QPainter, QColor, QImage
    from PySide6.QtWidgets import QHeaderView, QAbstractItemView
    from PySide6.QtCore import Qt, QTimer
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
        from PySide2.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTableWidgetItem
        from PySide2.QtGui import QPixmap, QPainter, QColor, QImage
        from PySide2.QtWidgets import QHeaderView, QAbstractItemView
        from PySide2.QtCore import Qt, QTimer
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
import sys
import cv2
import numpy as np
import shotgun_api3
from shotgrid_user_task import UserInfo, TaskInfo

class VideoPlayer(QLabel):
    """
    비디오 재생을 위해 만든 함수
    """
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.setAlignment(Qt.AlignCenter)
        self.setText("Loading Video...")

        self.cap = cv2.VideoCapture(self.video_path)  # OpenCV 비디오 캡처 객체
        if not self.cap.isOpened():
            self.setText("Error: Cannot open video")
            return

        self.timer = QTimer(self)  # QTimer 사용
        self.timer.timeout.connect(self.update_frame)  # 일정 간격으로 업데이트
        self.timer.start(30)  # 30ms마다 실행 (약 33fps)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상 끝나면 처음부터 다시 재생
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR -> Qt는 RGB 변환 필요
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        self.setPixmap(pixmap)

class UI(QMainWindow):
    def __init__(self):
        sg_url = "https://nashotgrid.shotgrid.autodesk.com"
        script_name = "test"
        api_key = "hetgdrcey?8coevsotrgwTnhv"
        self.user = UserInfo(sg_url, script_name, api_key)   
        super().__init__()
        self.setWindowTitle("EVAL_LOADER")

        self.login_window = self.login_ui()
        self.setCentralWidget(self.login_window)

    def setup_layout(self):
        """
        레이아웃 세팅
        """
        # 왼쪽 Task Table UI 생성
        task_container = self.make_task_table()
        # WORK 버전 UI 생성
        work_container = self.make_file_table("work")
        work_label = QLabel("WORK")
        # PUB 버전 UI 생성
        pub_container = self.make_file_table("pub")
        pub_label = QLabel("PUB")
        # PREVIOUS BLAST UI 생성
        previous_container = self.previous_data()

        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 버전, 타입 레이아웃
        v_layout = QVBoxLayout()
        v_layout.addWidget(work_label)
        v_layout.addWidget(work_container)
        v2_layout = QVBoxLayout()
        v2_layout.addWidget(pub_label)
        v2_layout.addWidget(pub_container)
        
        # work, pub 레이아웃 세팅
        version_layout = QHBoxLayout()
        version_layout.addLayout(v_layout)
        version_layout.addLayout(v2_layout)

        # work, pub, pb 레이아웃 세팅
        right_layout = QVBoxLayout()
        right_layout.addWidget(previous_container)
        right_layout.addLayout(version_layout)

        # 메인 레이아웃 세팅
        layout.addWidget(task_container)
        layout.addLayout(right_layout)

        return widget

    def previous_data(self):
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        user_name = "SOONWOOOO"
        play_blast = f"loader/loader_ui_sample/PB.mov" #mov파일경로
        status_color = "red"
        status_text = "진행중"
        comment_text = "뒷작업을 잘 부탁해. 부족해도...............오....디코해..."
        
        return self.previous_work_item(user_name, play_blast, status_color, status_text, comment_text)

    def previous_work_item(self, user, pb, status_color, status_text, cmt_txt):
        """
        외부에서 데이터를 받아서 Previous_work에 추가하는 함수
        """
        #동영상파일 재생
        video_widget = VideoPlayer(pb)
        video_widget.setStyleSheet("border: 2px solid #555; border-radius: 5px;")

        #정보 라벨
        previous_work = QLabel("PREVIOUS WORK")
        user_name = QLabel(user)     
        state_image = QLabel(status_color)      
        state_text = QLabel(status_text)  
        comment_label = QLabel("COMMENT")     
        comment_text = QLabel(f'" {cmt_txt} "')
        comment_text.setWordWrap(True)

        # 원 색칠
        status_pixmap = QPixmap(10, 10)  # 작은 원 크기 설정
        status_pixmap.fill(QColor("transparent"))  # 배경 투명
        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
        painter.setPen(QColor(status_color))  # 테두리도 빨간색
        painter.drawEllipse(0, 0, 10, 10)  # (x, y, width, height) 원 그리기
        painter.end()
        state_image.setPixmap(status_pixmap)

        # 공간 라벨
        null_label = QLabel()
        # 상태 레이아웃
        state_layout = QHBoxLayout()
        state_layout.addWidget(state_image)
        state_layout.addWidget(state_text)
        state_layout.addStretch()
        # 정보 레이아웃
        info_layout = QVBoxLayout()
        info_layout.addWidget(user_name)
        info_layout.addLayout(state_layout)
        info_layout.addWidget(comment_label)
        info_layout.addWidget(comment_text)
        # 넓히기 위한 레이아웃
        null_layout = QVBoxLayout()
        null_layout.addWidget(null_label)
        null_layout.addLayout(info_layout)
        # PB 레이아웃
        pre_layout = QHBoxLayout()
        pre_layout.addWidget(video_widget)
        pre_layout.addLayout(null_layout)

        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(previous_work)
        layout.addLayout(pre_layout)
        widget.setLayout(layout)

        return widget

    def make_file_table(self, version_type):
        """
        File UI (테이블 목록) 생성
        version_type: "work" 또는 "pub"
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테이블 위젯 생성 (초기 행 개수: 0, 3개 컬럼)
        file_table = QTableWidget(0, 3)
        file_table.setHorizontalHeaderLabels(["version", "file name", "user"])
        file_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
        file_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 비활성화
        file_table.setColumnWidth(0, 80)  # 로고 열 (좁게 설정)
        file_table.setColumnWidth(1, 300)  # 파일명 열 (길게 설정)

        file_table.setAlternatingRowColors(True)
        file_table.setStyleSheet("alternate-background-color: #2a2a2a; background-color: #1e1e1e;")


        file_table.setStyleSheet("""
            QTableView::item { border-right: none; }  /* 세로선 숨김 */
            QTableView { border-left: 1px black; }  /* 왼쪽 테두리 복구 */
            QTableWidget::item:selected { background-color: #005f87; color: white; } /* 더 선명한 색상으로 변경 */
        """)

        # 테이블 크기 조정
        file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  # 로고 고정
        file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 파일명 확장
        file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 담당자 최소 크기 맞춤
        file_table.verticalHeader().setVisible(False) # 행 번호 숨기기
        file_table.resizeRowsToContents()  # 행 크기 자동 조정
        file_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 가로 스크롤바 항상 숨김
        file_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 세로 스크롤바 넘치면 표시

        # UI 레이아웃 적용
        layout.addWidget(file_table)
        self.version_file_data(version_type, file_table)

        return widget  # QWidget 반환
    
    def version_file_data(self, version_type, file_table):
        """
        version_type: "work" 또는 "pub" 데이터를 구분하여 로드
        table: 데이터를 추가할 QTableWidget 객체
        """
        data = []

        if version_type == "work":
            data = [
                (f"loader/loader_ui_sample/logo.jpeg", "v0001", "anim test", "25.02.20, 19:07:04", "InHo"),
                (f"loader/loader_ui_sample/logo.jpeg", "v0002", "feedback implemented", "25.02.20, 9:07:04", "InHo"),
                (f"loader/loader_ui_sample/logo.jpeg", "v0003", " ", "25.02.19, 19:07:04", "InHo")
            ]
        if version_type == "pub":
            data = [
                (f"./loader/loader_ui_sample/logo.jpeg", "v0005", "anim test", "25.02.20, 19:07:04", "InHo"),
                (f"./loader/loader_ui_sample/logo.jpeg", "v0006", "feedback implemented", "25.02.20, 9:07:04", "InHo"),
                (f"./loader/loader_ui_sample/logo.jpeg", "v0007", " ", "25.02.19, 19:07:04", "InHo")
            ]

        file_table.setRowCount(0)
        for item in data:
            self.file_table_item(file_table, *item)
    
    def file_table_item(self, file_table, dcc_logo, version, name, storage_time, user_name):
        print(dcc_logo)
        row = file_table.rowCount()
        file_table.insertRow(row)  # 새로운 행 추가

        file_table.setRowHeight(row, 80)  # 행 높이 고정
        file_table.resizeRowsToContents()  # 자동 크기 조절 활성화

        # DCC 로고 + 버전 (QVBoxLayout 사용)
        dcc_widget = QWidget()
        dcc_layout = QVBoxLayout()

        file_logo = QLabel()
        pixmap = QPixmap(dcc_logo).scaled(80, 50)  # 크기 조절
        file_logo.setPixmap(pixmap)
        file_version = QLabel(version)
        file_logo.setAlignment(Qt.AlignCenter)
        file_version.setAlignment(Qt.AlignCenter)

        dcc_layout.addWidget(file_logo)
        dcc_layout.addWidget(file_version)
        dcc_layout.setContentsMargins(5, 5, 5, 5)
        dcc_widget.setLayout(dcc_layout)
        file_table.setCellWidget(row, 0, dcc_widget)  # 첫 번째 열에 추가

        # 파일명 (QTableWidgetItem 사용)
        file_item = QTableWidgetItem(name)
        file_table.setItem(row, 1, file_item)  # 두 번째 열에 추가

        # 담당자 + 저장 날짜 (QVBoxLayout 사용)
        user_widget = QWidget()
        user_layout = QVBoxLayout()
        file_user_name = QLabel(user_name)
        file_save_time = QLabel(storage_time)
        file_user_name.setAlignment(Qt.AlignRight)
        file_save_time.setAlignment(Qt.AlignRight)

        user_layout.addWidget(file_user_name)
        user_layout.addWidget(file_save_time)
        user_layout.setContentsMargins(5, 5, 5, 5)

        user_widget.setLayout(user_layout)
        file_table.setCellWidget(row, 2, user_widget)  # 세 번째 열에 추가

        # 행 높이 조정
        file_table.setRowHeight(row, 80)

    def make_task_table(self):
        """
        Task UI (테이블 목록) 생성
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테스크 검색, 정렬 UI 생성
        task_label = QLabel("TASK")
        search_input = QLineEdit() # 검색창
        search_input.setPlaceholderText("SEARCH") # 흐릿한 글씨
        search_but = QPushButton("검색") # 검색버튼
        combo_box = QComboBox()

        # 테스크 검색, 정렬 레이아웃 정렬
        h_layout = QHBoxLayout()
        h_layout.addWidget(task_label)
        h_layout.addWidget(search_input)
        h_layout.addWidget(search_but)
        h_layout.addWidget(combo_box)

        # 테이블 위젯 생성 (초기 행 개수: 0, 2개 컬럼)
        task_table = QTableWidget(0, 2)
        task_table.setHorizontalHeaderLabels(["Thumbnail", "Task Info"])

        # 테이블 크기설정
        task_table.setColumnWidth(0, 180)  # 로고 열 (좁게 설정)
        task_table.setColumnWidth(1, 300)  # 파일명 열 (길게 설정)
        task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  # 로고 고정
        task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 파일명 확장
        task_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 비활성화
        task_table.resizeRowsToContents()  # 행 크기 자동 조정
        task_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 가로 스크롤바 항상 숨김
        task_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 세로 스크롤바 넘치면 표시
        task_table.verticalHeader().setVisible(False) #행번호 숨김

        # UI 레이아웃 적용
        layout.addLayout(h_layout)
        layout.addWidget(task_table)

        # 테스크 데이터 업데이트 
        self.task_data(task_table)
        return widget  # QWidget 반환

    def task_data(self, task_table):
        """
        외부에서 데이터를 받아서 task에 추가하는 함수
        """
        data = [
            (f"loader/loader_ui_sample/task.jpeg", "SQ03-SH0010", "Animation", "25.02.19 - 25.02.20", "#00CC66"),
            (f"loader/loader_ui_sample/task.jpeg", "SQ03-SH0020", "Assets", "26.02.19 - 27.02.20", "#FFD700"),
            (f"loader/loader_ui_sample/task.jpeg", "SQ03-SH0030", "Blocking", "28.02.19 - 01.03.20", "#FF4C4C")
        ]

        for item in data:
            self.task_table_item(task_table, *item)

    def task_table_item(self, task_table, thumb, file_name, type, deadline, status_color):
        row = task_table.rowCount()
        task_table.insertRow(row)  # 새로운 행 추가

        task_table.setRowHeight(row, 80)  
        task_table.resizeRowsToContents() 

        # 썸네일
        task_thumb = QLabel()
        pixmap = QPixmap(thumb)  # 이미지 파일 경로
        task_thumb.setPixmap(pixmap.scaled(120, 70))  # 크기 조절
        task_thumb.setAlignment(Qt.AlignCenter)  # 이미지를 중앙 정렬
        task_thumb.setScaledContents(True)  # QLabel 크기에 맞게 이미지 조정
        task_table.setCellWidget(row, 0, task_thumb)

        # 상태 표시 (● 빨간색 원)
        task_status = QLabel()
        status_pixmap = QPixmap(12, 12)  # 작은 원 크기 설정
        status_pixmap.fill(QColor("transparent"))  # 배경 투명

        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
        painter.setPen(QColor(status_color))  # 테두리도 빨간색
        painter.drawEllipse(0, 0, 12, 12)  # (x, y, width, height) 원 그리기
        painter.end()
        task_status.setPixmap(status_pixmap)

        # 작업 유형
        task_type = QLabel(type)
        # 마감 기한
        task_deadline = QLabel(deadline)
        # 샷 이름
        task_name = QLabel(file_name)

        # 상태와 작업 유형을 수평 정렬
        status_layout = QHBoxLayout()
        status_layout.addWidget(task_status)  # 빨간 원 (●)
        status_layout.addWidget(task_type)  # Animation
        status_layout.addStretch()  # 남은 공간 정렬

        # 텍스트 정보 수직 정렬 (샷 이름 + 상태 + 마감 기한)
        text_layout = QVBoxLayout()
        text_layout.addWidget(task_name)  # 샷 이름
        text_layout.addLayout(status_layout)  # 상태 + 작업 유형
        text_layout.addWidget(task_deadline)  # 마감 기한

        widget = QWidget()
        layout = QHBoxLayout()

        layout.addLayout(text_layout)  # 오른쪽: 텍스트 그룹
        layout.setContentsMargins(5, 5, 5, 5)  # 여백 조정
        widget.setLayout(layout)

        # 테이블 위젯 추가
        task_table.setCellWidget(row, 1, widget)

        # 행 높이를 조정하여 잘리지 않도록 설정
        task_table.setRowHeight(row, 80)

    def on_login_click(self):
        """
        로그인 버튼 실행
        """
        name = self.name_input.text()
        email = self.email_input.text()
        if name and email: #이름과 이메일에 값이 있을 때
            is_validate = self.user.is_validate(email, name)
            if not is_validate:
                popup = QMessageBox()
                popup.setIcon(QMessageBox.Warning)
                popup.setWindowTitle("Failure")
                popup.setText("아이디 또는 이메일이 일치하지 않습니다")
                popup.exec()
            else:
                self.resize(1440, 800)  # 메인 화면 크기 조정
                self.setCentralWidget(self.setup_layout()) # 로그인 창을 메인화면으로 변경
        else: # 이름과 이메일에 값이 없을 때
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("이름과 이메일을 입력해주세요")
            popup.exec()

    def login_ui(self):
        """
        로그인 화면 UI
        """
        widget = QWidget()
        widget.setFixedSize(400, 200)  # 로그인 창 크기 조절
        layout = QVBoxLayout(widget)

        # 네임 임력
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("NAME") # 흐릿한 글씨

        # 이메일 입력
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("EMAIL") # 흐릿한 글씨

        # 로그인 버튼
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.clicked.connect(self.on_login_click)

        # 레이아웃 설정
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.login_btn)

        return widget # 생성된 창 반환
    
if __name__ == "__main__":
    # 앱 실행
    app = QApplication([])
    print ("UI 인스턴스 생성 시작")
    ui = UI()  # UI 클래스 실행
    print ("UI 인스턴스 생성 완료")
    ui.show() # 최고 짱짱 순우
    app.exec()