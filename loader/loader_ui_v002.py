try :
    from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy
    from PySide6.QtGui import QPixmap, QPainter, QColor, QImage, QFont
    from PySide6.QtWidgets import QHeaderView, QAbstractItemView
    from PySide6.QtCore import Qt, QTimer
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
        from PySide2.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy
        from PySide2.QtGui import QPixmap, QPainter, QColor, QImage, QFont
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
import os
import time

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
        sg_url = "https://hi.shotgrid.autodesk.com/"
        script_name = "Admin_SY"
        api_key = "kbuilvikxtf5v^bfrivDgqhxh"
        self.user = UserInfo(sg_url, script_name, api_key)
        self.user_name = ""
        self.task_info = TaskInfo(sg_url, script_name, api_key)
        self.prefix_path = "/nas/eval/show"
        
        super().__init__()
        self.setWindowTitle("EVAL_LOADER")
        self.center_window()

        self.login_window = self.login_ui()
        self.setCentralWidget(self.login_window)

    def setup_layout(self):
        """
        레이아웃 세팅
        """
        # 왼쪽 Task Table UI 생성
        self.task_container = self.make_task_table()
        self.task_container.setMinimumWidth(570)
        self.task_container.setMaximumWidth(570)  # TASK 최소 너비 지정, 안하면 너무 작아짐.
        self.task_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 가로/세로 확장 허용
        # WORK 버전 UI 생성
        work_container = self.make_file_table("work")
        work_label = QLabel("WORK")
        work_label.setStyleSheet("font-weight: bold;")
        work_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) #가로, 세로 고정 크기 조정
        # PUB 버전 UI 생성
        pub_container = self.make_file_table("pub")
        pub_label = QLabel("PUB")
        pub_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        pub_label.setStyleSheet("font-weight: bold;")
        # PREVIOUS BLAST UI 생성
        previous_container = self.previous_data()

        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 유저 레이아웃
        user_layout = QHBoxLayout()
        none_label = QLabel()
        user_name = QLabel(self.name_input.text())
        user_name.setStyleSheet("font-weight: bold;")
        user_name.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        user_name.setAlignment(Qt.AlignRight)
        user_layout.addWidget(none_label)
        user_layout.addWidget(user_name)

        # work, pub, pb, 유저이름 레이아웃 세팅
        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(user_layout)
        self.right_layout.addWidget(previous_container, 2)
        self.right_layout.addWidget(work_label)
        self.right_layout.addWidget(work_container, 2)
        self.right_layout.addWidget(pub_label)
        self.right_layout.addWidget(pub_container, 1)

        # 메인 레이아웃 세팅
        layout.addWidget(self.task_container, 3)
        layout.addLayout(self.right_layout, 2)

        return widget

    def previous_data(self): #############################################순우work
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        user_name = "No data"
        play_blast = f"/home/rapa/다운로드/output1.mov" #mov파일경로
        status_text = "fin"
        for k, v in self.color_map.items() :
            if status_text == k :
                status_color = v
        comment_text = "나는 나와의 싸움에서 졌다. 하지만 이긴것도 나다\n-장순우-"
        
        return self.previous_work_item(user_name, play_blast, status_color, status_text, comment_text)

    def previous_work_item(self, user, pb, status_color, status_text, cmt_txt):
        """
        외부에서 데이터를 받아서 Previous_work에 추가하는 함수
        """
        #동영상파일 재생
        video_widget = VideoPlayer(pb)
        video_widget.setStyleSheet("border: 2px solid #555; border-radius: 5px;")

        # 원본 크기 가져오기 (비율 유지)
        original_size = video_widget.size()  # 또는 video_widget.size()
        default_width = original_size.width()/2.5
        default_height = original_size.height()/2.5

        #video_widget.setAspectRatioMode(True)
        video_widget.setFixedSize(default_width, default_height)

        # 비율 유지하며 크기 자동 조정
        video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        video_widget.setScaledContents(True)  # 자동으로 크기 조절 (비율 유지)

        #정보 라벨
        previous_work = QLabel("PREVIOUS WORK")
        previous_work.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        previous_work.setStyleSheet("font-weight: bold;")

        # Prev Work 정보 테이블
        self.info_table = QTableWidget(4, 3)
        self.info_table.verticalHeader().setVisible(False)  # 번호(인덱스) 숨기기
        self.info_table.horizontalHeader().setVisible(False)  # 가로 헤더 숨기기
        self.info_table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)  # 크기 조정 허용
        self.info_table.setMinimumHeight(self.info_table.sizeHint().height())  # 최소 높이 조정
        self.info_table.setMaximumHeight(self.info_table.sizeHint().height())  # 최대 높이도 맞춤
        self.info_table.resizeRowsToContents()
        self.info_table.resizeColumnsToContents()
        self.info_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.info_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.info_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 편집 비활성화
        self.info_table.setSelectionMode(QAbstractItemView.NoSelection)  # 선택 불가
        self.info_table.setShowGrid(False)

        # 강제로 높이를 내부 아이템 크기에 맞춤
        self.info_table.setFixedHeight(self.info_table.verticalHeader().length() + 16)

        self.info_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: transparent;
            }
            QTableWidget::item {
                border: none;
                background: transparent;
            }
        """)

        # 데이터 삽입
        labels = ["Dept", "Assignee", "Reviewer", "Status"]

        for row, label in enumerate(labels):
            self.info_table.setItem(row, 0, QTableWidgetItem(label))  # 0열 (항목명) 추가

            item = QTableWidgetItem(":")  # 1열 (콜론 `:`) 아이템 생성
            item.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬 적용
            self.info_table.setItem(row, 1, item)  # 1열에 아이템 추가

        self.dept_name = QTableWidgetItem("No data")
        self.user_name = QTableWidgetItem(user)
        self.reviewer_text = QTableWidgetItem("Not Assigned")
        
        self.info_table.setItem(0, 2, self.dept_name)   # Dept
        self.info_table.setItem(1, 2, self.user_name)  # Assignee
        self.info_table.setItem(2, 2, self.reviewer_text)  # Reviewer
        # self.info_table.setItem(3, 2, self.state_text)  # Status

        # COMMENT 영역
        comment_label = QLabel("Comment  :")
        comment_label.setStyleSheet("padding-left: 1px;")
        comment_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 왼쪽 정렬 + 수직 중앙 정렬
        comment_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 가로/세로 모두 텍스트에 맞춤
        comment_label.adjustSize()  # 크기를 텍스트에 딱 맞게 조정

        self.comment_text = QLabel(f'" {cmt_txt} "')
        self.comment_text.setStyleSheet("padding-top: 2px;padding-left: 1px;")
        self.comment_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.comment_text.setWordWrap(True)

        self.state_image = QLabel(status_color)      
        # self.state_text = QLabel(status_text)  
        
        
        # 원 색칠
        status_pixmap = QPixmap(10, 10)  # 작은 원 크기 설정
        status_pixmap.fill(QColor("transparent"))  # 배경 투명
        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
        painter.setPen(QColor(status_color))  # 테두리도 빨간색
        painter.drawEllipse(0, 0, 10, 10)  # (x, y, width, height) 원 그리기
        painter.end()
        self.state_image.setPixmap(status_pixmap)

        status_wdidget = QWidget()
        status_layout = QHBoxLayout(status_wdidget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(2)

        # 상태 아이콘 QLabel
        status_icon_label = QLabel()
        # status_icon_label.setStyleSheet("border : 1px solid black")
        status_icon_label.setPixmap(status_pixmap)

        # 아이콘 크기 제한 (픽셀 크기에 맞게 조정)
        icon_size = status_pixmap.size()
        status_icon_label.setFixedSize(icon_size)  # 원본 크기에 맞게 고정

        status_text_label = QLabel(status_text)
        # status_text_label.setStyleSheet("border : 1px solid black")

        # 레이아웃에 아이콘과 텍스트 추가
        status_layout.addWidget(status_icon_label)
        status_layout.addWidget(status_text_label)

        self.info_table.setCellWidget(3, 2, status_wdidget)


        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        # info_layout.addWidget(previous_work)
        info_layout.addWidget(self.info_table)
        info_layout.addWidget(comment_label)
        info_layout.addWidget(self.comment_text)

        # PB 레이아웃
        pre_layout = QHBoxLayout()
        pre_layout.setSpacing(20)
        pre_layout.addWidget(video_widget)
        pre_layout.addLayout(info_layout)

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

        if version_type == "pub":
            self.pub_table = QTableWidget(0, 3)
            table = self.pub_table  # Assign to pub_table
        elif version_type == "work":
            self.work_table = QTableWidget(0, 3)
            table = self.work_table  # Assign to work_table

        table.setHorizontalHeaderLabels(["로고", "파일 이름", "최근 수정일"])
        table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 편집 비활성화
        table.setColumnWidth(0, 30)  # 로고 열 (좁게 설정)
        table.setColumnWidth(1, 300)  # 파일명 열 (길게 설정)
        table.verticalHeader().setDefaultSectionSize(30)

        table.setAlternatingRowColors(True)
        layout.addWidget(table)

        file_path = ""
        file_list = ["NULL"]
        self.version_file_data(version_type, file_path, file_list)

        return widget  # QWidget 반환
    
    def version_file_data(self, version_type, file_path, file_list):
        data = []

        if version_type == "work" :
            if not file_path == "" :
                for file in file_list :
                    data.append((f"/nas/sam/config/config/icons/pixar_usd_publish.png", file[0], file[1]))
            else : 
                data = [(f"/nas/sam/config/config/icons/pixar_usd_publish.png", "no work yet", "25-02-20")]

        elif version_type == "pub" :
            if not file_path == "" :
                for file in file_list :
                    data.append((f"/nas/sam/config/config/icons/pixar_usd_publish.png", file[0], file[1]))
            else : 
                data = [
                    (f"/nas/sam/config/config/icons/pixar_usd_publish.png", "no pub yet", "25-02-20")
                ]
        else :
            print("뭐임")
            data = [
                (f"/nas/sam/config/config/icons/pixar_usd_publish.png", "NULL", "25-02-20")
            ]

        if version_type == "work":
            self.work_table.setRowCount(0)  # Clear the work table rows
            for item in data:
                self.file_table_item(self.work_table, *item)  # Update the work table

        elif version_type == "pub":
            self.pub_table.setRowCount(0)  # Clear the pub table rows
            for item in data:
                self.file_table_item(self.pub_table, *item)  # Update the pub table
    
    def file_table_item(self, table_widget, dcc_logo, file_name, edited_time):
        row = table_widget.rowCount()
        table_widget.insertRow(row)  # 새로운 행 추가

        #DCC 로고
        file_logo = QLabel()
        pixmap = QPixmap(dcc_logo).scaled(30, 30)  # 크기 조절
        file_logo.setPixmap(pixmap)
        #file_logo.setScaledContents(True) # 크기에 맞게 이미지가 자동으로 축소/확대됨.
        file_logo.setAlignment(Qt.AlignCenter)
        table_widget.setCellWidget(row, 0, file_logo)  # 첫 번째 열에 추가

        # 파일명 (QTableWidgetItem 사용)
        name_table = QTableWidgetItem(f"{file_name}")
        table_widget.setItem(row, 1, name_table)  # 두 번째 열에 추가
        print(file_name)

        # 저장 날짜 
        time_table = QTableWidgetItem(f"{edited_time}")
        table_widget.setItem(row, 2, time_table)  # 세 번째 열에 추가
        print(edited_time)

    def make_task_table(self):
        """
        Task UI (테이블 목록) 생성
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테스크 검색, 정렬 UI 생성
        task_label = QLabel("TASK")
        task_label.setStyleSheet("font-weight: bold;")
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
        self.task_table = QTableWidget(0, 3)
        self.task_table.setHorizontalHeaderLabels(["Thumbnail", "Task Info", "Task ID"])
        self.task_table.setColumnHidden(2, True) # Task ID 숨김

        # 테이블 이벤트 처리
        self.task_table.cellClicked.connect(self.on_cell_clicked)

        # 테이블 크기설정
        self.task_table.setColumnWidth(0, 180)  # 로고 열 (좁게 설정)
        self.task_table.setColumnWidth(1, 300)  # 파일명 열 (길게 설정)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  # 로고 고정
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 파일명 확장
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 비활성화
        self.task_table.resizeRowsToContents()
        self.task_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.task_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 가로 스크롤바 항상 숨김
        self.task_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 세로 스크롤바 넘치면 표시
        self.task_table.verticalHeader().setVisible(False) #행번호 숨김

        # UI 레이아웃 적용
        none_label = QLabel()
        layout.addWidget(none_label)
        layout.addLayout(h_layout)
        layout.addWidget(self.task_table)

        # 테스크 데이터 업데이트 
        self.populate_task_dict()
        return widget  # QWidget 반환

    # self.task_dict 순회 하면서 data 가공 후 add_task_to_table()
    def populate_task_dict(self):
        self.task_info.get_user_task(self.user.get_userid())
        task_dict = self.task_info.get_task_dict()

        self.color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"}

        for task_id, task_data in task_dict.items() :
            thumb = "loader/loader_ui_sample/task.jpeg"
            task_name = task_data['content']
            proj_name = task_data['proj_name']
            status = task_data['status']
            step = task_data['step']
            start_date = task_data['start_date']
            due_date = task_data['due_date']

            if task_data['task_type'] == 'Shot' : 
                low_data = task_data['shot_name']
                high_data = task_data['seq_name']
                
            elif task_data['task_type'] == 'Asset' :
                low_data = task_data['asset_name']
                high_data = task_data['asset_categ']
                
            for k, v in self.color_map.items() :
                if status == k :
                    status_color = v

            data_set = f"{low_data} | {high_data} | {proj_name}"
            date_set = f"{start_date} - {due_date}"
            self.add_task_to_table(task_id, thumb, task_name, data_set, status_color, status, step, date_set)

    # self.task_table에 data binding
    def add_task_to_table(self, task_id, thumb, task_name, data_set, status_color, status, step, date_set):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)
        
        self.task_table.setItem(row, 2, QTableWidgetItem(str(task_id)))

        self.task_table.setRowHeight(row, 80)  
        self.task_table.resizeRowsToContents()

        task_name = QLabel(task_name)
        task_name.setStyleSheet("font-size: 16pt;")
        task_step = QLabel(step)
        task_step.setStyleSheet("color: grey")
        task_step.setAlignment(Qt.AlignRight)

        # 프로젝트 네임
        task_name_layout = QHBoxLayout()
        task_name_layout.addWidget(task_name)
        task_name_layout.addWidget(task_step)

        # 썸네일
        task_thumb = QLabel()
        pixmap = QPixmap(thumb)  # 이미지 파일 경로
        task_thumb.setPixmap(pixmap.scaled(120, 70))  # 크기 조절
        task_thumb.setAlignment(Qt.AlignCenter)  # 이미지를 중앙 정렬
        task_thumb.setScaledContents(True)  # QLabel 크기에 맞게 이미지 조정
        self.task_table.setCellWidget(row, 0, task_thumb)

        # 상태 표시 (●)
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
        data_set = QLabel(data_set)
        date_set = QLabel(date_set)
        status = QLabel(status)
        status.setStyleSheet("font-size: 10pt; color: grey")

        # 상태와 작업 유형을 수평 정렬
        status_layout = QHBoxLayout()
        status_layout.addWidget(task_status)
        status_layout.addWidget(status)
        status_layout.addStretch() 

        text_layout = QVBoxLayout()
        text_layout.addLayout(task_name_layout)
        text_layout.addLayout(status_layout)  # 상태 + 작업 유형
        text_layout.addWidget(data_set)
        text_layout.addWidget(date_set)


        widget = QWidget()
        layout = QHBoxLayout()

        layout.addLayout(text_layout)  # 오른쪽: 텍스트 그룹
        layout.setContentsMargins(5, 5, 5, 5)  # 여백 조정
        widget.setLayout(layout)

        # 테이블 위젯 추가
        self.task_table.setCellWidget(row, 1, widget)
        # 행 높이를 조정하여 잘리지 않도록 설정
        self.task_table.setRowHeight(row, 80)

    def on_cell_clicked(self, row, _):
        clicked_task_id = int(self.task_table.item(row, 2).text())
        print(clicked_task_id)
        pub_path, pub_list = self.task_info.get_pub_files(clicked_task_id)
        self.version_file_data('pub', pub_path, pub_list)

        work_path , work_list = self.task_info.get_work_files(clicked_task_id)
        self.version_file_data('work', work_path, work_list)

        prev_task_data, current_task_data = self.task_info.on_click_task(clicked_task_id)
        prev_task_id = prev_task_data['id']

        self.update_prev_work(prev_task_data)

        print(f"현재 창 크기 - 너비: {self.width()}px, 높이: {self.height()}px")

        # Task container 크기 출력
        if hasattr(self, 'task_container'):
            print(f"Task Container 크기 - 너비: {self.task_container.width()}px, 높이: {self.task_container.height()}px")
        else:
            print("Task Container가 초기화되지 않았습니다.")

        # Right container 크기 출력
        if hasattr(self, 'right_layout'):
            right_container = self.right_layout.parentWidget()  # 부모 위젯 가져오기
            if right_container:
                print(f"Right Container 크기 - 너비: {right_container.width()}px, 높이: {right_container.height()}px")
            else:
                print("Right Container의 부모 위젯이 없습니다.")
        else:
            print("Right Layout이 초기화되지 않았습니다.")
        

    def update_prev_work(self, prev_task_data):
        if prev_task_data['id'] != "None":
            prev_task_id = prev_task_data['id']
            prev_task_name = prev_task_data['task_name']
            prev_task_assignee = prev_task_data['assignees']
            prev_task_reviewers = prev_task_data['reviewers']
            prev_task_status = prev_task_data['status']
            prev_task_step = prev_task_data['step']
            prev_task_comment = prev_task_data['comment']
        else :
            prev_task_id = "No data"
            prev_task_name = "No data"
            prev_task_assignee = "No data"
            prev_task_reviewers = "No data"
            prev_task_status = "fin"
            prev_task_step = "No data"
            prev_task_comment = "No data for previous work"

        # 테이블 업데이트
        self.dept_name.setText(prev_task_step)
        self.user_name.setText(prev_task_assignee)
        self.reviewer_text.setText(prev_task_reviewers)
        self.comment_text.setText(f'" {prev_task_comment} "')

        # status color update
        for k, v in self.color_map.items() :
            if prev_task_status == k :
                status_color = v
        
        status_pixmap = QPixmap(10, 10)  # 작은 원 크기 설정
        status_pixmap.fill(QColor("transparent"))  # 배경 투명
        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
        painter.setPen(QColor(status_color))  # 테두리도 빨간색
        painter.drawEllipse(0, 0, 10, 10)  # (x, y, width, height) 원 그리기
        painter.end()

        # self.state_image.setPixmap(status_pixmap)

        # 기존 위젯 제거 후 새로 추가
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(2)

        # 상태 아이콘 QLabel
        status_icon_label = QLabel()
        status_icon_label.setPixmap(status_pixmap)
        status_icon_label.setFixedSize(status_pixmap.size())  # 아이콘 크기 고정

        # 상태 텍스트 QLabel
        status_text_label = QLabel(prev_task_status)

        # 레이아웃에 아이콘과 텍스트 추가
        status_layout.addWidget(status_icon_label)
        status_layout.addWidget(status_text_label)

        # 기존 셀 위젯 제거 후 새 위젯 설정
        self.info_table.setCellWidget(3, 2, status_widget)

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
                self.user_name = name
                self.resize(1200, 800)  # 메인 화면 크기 조정
                self.setCentralWidget(self.setup_layout()) # 로그인 창을 메인화면으로 변경
                self.center_window()
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
        self.name_input = QLineEdit("신승연") ################ 말풍선 제거하기
        # self.name_input.setPlaceholderText("NAME") # 흐릿한 글씨

        # 이메일 입력
        self.email_input = QLineEdit("p2xch@naver.com") ################ 말풍선 제거하기
        # self.email_input.setPlaceholderText("EMAIL") # 흐릿한 글씨

        # 엔터(RETURN) 키를 누르면 로그인 버튼 클릭과 동일하게 동작하도록 연결
        self.email_input.returnPressed.connect(self.on_login_click)
        self.name_input.returnPressed.connect(self.on_login_click)

        # 로그인 버튼
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.clicked.connect(self.on_login_click)

        # 레이아웃 설정
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.login_btn)

        return widget # 생성된 창 반환
    
    def center_window(self):
        frame_geometry = self.frameGeometry()  # 창의 프레임 가져오기
        screen = QApplication.primaryScreen()  # 현재 사용 중인 화면 가져오기
        screen_geometry = screen.availableGeometry().center()  # 화면의 중앙 좌표
        frame_geometry.moveCenter(screen_geometry)  # 창의 중심을 화면 중심으로 이동
        self.move(frame_geometry.topLeft())  # 최종적으로 창을 이동

if __name__ == "__main__":
    app = QApplication([])
    print ("UI 인스턴스 생성 시작")
    ui = UI() 
    print ("UI 인스턴스 생성 완료")
    ui.show() 
    app.exec()