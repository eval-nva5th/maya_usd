
from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
from PySide2.QtWidgets import QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QHeaderView, QAbstractItemView
from PySide2.QtCore import Qt
import maya.cmds as cmds

from loader.event import event_handler
from shotgrid_user_task import UserInfo, TaskInfo, ClickedTask
from core.video_player import VideoPlayer
from core.data_managers import previous_data, task_data

class UI(QMainWindow):
    def __init__(self):

        sg_url = "https://5thacademy.shotgrid.autodesk.com/"
        script_name = "sy_key"
        api_key = "vkcuovEbxhdoaqp9juqodux^x"
        self.user = UserInfo(sg_url, script_name, api_key)
        self.user_name = ""
        self.task_info = TaskInfo(sg_url, script_name, api_key)
        self.prefix_path = "/nas/eval/show"

        self.input_name = ""

        self.task_data_dict = []

        super().__init__()
        self.setWindowTitle("EVAL LOADER")
        self.center_window()

        self.work_table = QTableWidget(0,3)
        self.work_table.setSelectionBehavior(QTableWidget.SelectRows)  # 행 단위 선택
        self.work_table.setEditTriggers(QTableWidget.NoEditTriggers)  # **모든 셀 편집 막기**
        self.work_table.horizontalHeader().setVisible(False)  
        self.work_table.verticalHeader().setVisible(False) 
        self.pub_table = QTableWidget(0,3)
        self.pub_table.setSelectionBehavior(QTableWidget.SelectRows)  # 행 단위 선택
        self.pub_table.setEditTriggers(QTableWidget.NoEditTriggers)  # **모든 셀 편집 막기**
        self.pub_table.horizontalHeader().setVisible(False) 
        self.pub_table.verticalHeader().setVisible(False)  

    def setup_layout(self):
        """
        레이아웃 세팅
        """
        # 왼쪽 Task Table UI 생성
        self.task_container = self.make_task_table()
        self.task_container.setMinimumWidth(570)
        self.task_container.setMaximumWidth(570)  # TASK 최소 너비 지정, 안하면 너무 작아짐.
        self.task_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # 가로/세로 확장 허용
        #self.task_container.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        
        file_table_widget = QWidget()
        file_table_layout = QVBoxLayout(file_table_widget)

        # WORK 버전 UI 생성
        work_label = QLabel("WORK")
        work_label.setStyleSheet("font-weight : bold;padding-left: 10px;")
        work_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        # PUB 버전 UI 생성
        pub_label = QLabel("PUB")
        pub_label.setStyleSheet("font-weight : bold;padding-left: 10px;")
        pub_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        file_table_layout = QVBoxLayout()
        file_table_layout.addWidget(work_label)
        file_table_layout.addWidget(self.work_table)
        file_table_layout.addWidget(pub_label)
        file_table_layout.addWidget(self.pub_table)

        # PREVIOUS BLAST UI 생성
        previous_container = previous_data(self)

        widget = QWidget()
        layout = QHBoxLayout(widget)
        # 유저 레이아웃
        user_layout = QHBoxLayout()
        none_label = QLabel()
        user_name = QLabel(self.input_name)
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
        self.right_layout.addWidget(self.work_table, 2)
        self.right_layout.addWidget(pub_label)
        self.right_layout.addWidget(self.pub_table, 1)

        # 메인 레이아웃 세팅
        layout.addWidget(self.task_container, 3)
        layout.addLayout(self.right_layout, 2)

        return widget

    def previous_work_item(self, user, pb, status_color, status_text, cmt_txt):
        """
        외부에서 데이터를 받아서 Previous_work에 추가하는 함수
        """
        #동영상파일 재생
        self.video_widget = VideoPlayer(pb)
        self.video_widget.setStyleSheet("border: 2px solid #555; border-radius: 5px;")

        # 원본 크기 가져오기 (비율 유지)
        original_size = self.video_widget.size()  # 또는 self.video_widget.size()
        default_width = original_size.width()/2.5
        default_height = original_size.height()/2.5

        #self.video_widget.setAspectRatioMode(True)
        self.video_widget.setFixedSize(default_width, default_height)

        # 비율 유지하며 크기 자동 조정
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_widget.setScaledContents(True)  # 자동으로 크기 조절 (비율 유지)

        #정보 라벨
        previous_work = QLabel("PREVIOUS WORK")
        previous_work.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        previous_work.setStyleSheet("font-weight: bold;")

        # Prev Work 정보 테이블
        self.info_table = QTableWidget(4, 3)
        self.info_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.info_table.setFocusPolicy(Qt.NoFocus)
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
        pre_layout.addWidget(self.video_widget)
        pre_layout.addLayout(info_layout)

        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(previous_work)
        layout.addLayout(pre_layout)
        widget.setLayout(layout)

        return widget

    def handle_work_table_click(self, table_widget, row, col):
        if col != 1:  # Ensure it only fires for one column
            return
        print(f"Processing row {row}, column {col}")  # Debugging output

    def make_task_table(self):
        """
        Task UI (테이블 목록) 생성
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테스크 검색, 정렬 UI 생성
        task_label = QLabel("TASK")
        task_label.setStyleSheet("font-weight: bold;")
        self.search_input = QLineEdit() # 검색창
        self.search_but = QPushButton("SEARCH") # 검색버튼
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("data : latest")  # 오름차순 정렬
        self.sort_combo.addItem("date : earlist")  # 내림차순 정렬

        # 테스크 검색, 정렬 레이아웃 정렬
        h_layout = QHBoxLayout()
        h_layout.addWidget(task_label)
        h_layout.addWidget(self.search_input)
        h_layout.addWidget(self.search_but)
        h_layout.addWidget(self.sort_combo)

        # 테이블 위젯 생성 (초기 행 개수: 0, 2개 컬럼)
        self.task_table = QTableWidget(0, 3)
        self.task_table.setSelectionBehavior(QTableWidget.SelectRows)  # 행 단위 선택
        self.task_table.setEditTriggers(QTableWidget.NoEditTriggers)  # **모든 셀 편집 막기**
        self.task_table.setHorizontalHeaderLabels(["Thumbnail", "Task Info", "Task ID"])
        self.task_table.setColumnHidden(2, True) # Task ID 숨김

        # 테이블 이벤트 처리
        # self.task_table.cellDoubleClicked.connect(lambda row,col:on_cell_clicked(self,row,col))
        # self.search_but.clicked.connect(lambda:search_task(self))
        # self.search_input.returnPressed.connect(lambda:search_task(self))
        # self.search_input.textChanged.connect(lambda:search_task(self))
        # self.sort_combo.currentIndexChanged.connect(lambda:on_sort_changed(self)) 이거 둘중 하나로 처리해야함
        self.task_table.cellClicked.connect(lambda row,col:event_handler.on_cell_clicked(self,row,col))
        self.search_but.clicked.connect(lambda:event_handler.search_task(self))
        self.search_input.returnPressed.connect(lambda:event_handler.search_task(self))
        self.search_input.textChanged.connect(lambda:event_handler.search_task(self))
        self.sort_combo.currentIndexChanged.connect(lambda:event_handler.on_sort_changed(self))

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
        task_data(self, self.task_table)
        self.task_table_item(self.task_data_dict)
        return widget  # QWidget 반환

    def task_table_item(self,task_data_dict):
        for data in task_data_dict:
            task_id = data["task_id"]
            task_table = data["task_table"]
            thumb = data["thumb"]
            task_name = data["task_name"]
            data_set = data["data_set"]
            status_color = data["status_color"]
            status = data["status"]
            step = data["step"]
            start_date = data["start_date"]
            due_date = data["due_date"]

            date_set = f"{start_date} - {due_date}"

            row = task_table.rowCount()
            task_table.insertRow(row)  # 새로운 행 추가
            task_table.setItem(row, 2, QTableWidgetItem(str(task_id)))
            task_table.setRowHeight(row, 80)  
            task_table.resizeRowsToContents()

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
            data_set = QLabel(data_set)
            date_set = QLabel(date_set)
            status = QLabel(status)
            status.setStyleSheet("font-size: 10pt; color: grey")

            # 상태와 작업 유형을 수평 정렬
            status_layout = QHBoxLayout()
            status_layout.addWidget(task_status)  # 빨간 원 (●)
            status_layout.addWidget(status)
            
            #status_layout.addWidget(task_step)  # Animation
            status_layout.addStretch()  # 남은 공간 정렬

            text_layout = QVBoxLayout()

            #text_layout.addWidget(task_name)
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
            task_table.setCellWidget(row, 1, widget)
            # 행 높이를 조정하여 잘리지 않도록 설정
            task_table.setRowHeight(row, 80)

    # def login_ui(self):
    #     """
    #     로그인 화면 UI
    #     """
    #     widget = QWidget()
    #     layout = QVBoxLayout(widget)

    #     # 네임 임력
    #     self.name_input = QLineEdit("장순우") ################ 말풍선 제거하기
    #     # self.name_input.setPlaceholderText("NAME") # 흐릿한 글씨

    #     # 이메일 입력
    #     self.email_input = QLineEdit("f8d783@kw.ac.kr") ################ 말풍선 제거하기
    #     # self.email_input.setPlaceholderText("EMAIL") # 흐릿한 글씨

    #     # 엔터(RETURN) 키를 누르면 로그인 버튼 클릭과 동일하게 동작하도록 연결
    #     self.email_input.returnPressed.connect(lambda:on_login_clicked(self))
    #     self.name_input.returnPressed.connect(lambda:on_login_clicked(self))

    #     # 로그인 버튼
    #     self.login_btn = QPushButton("LOGIN")
    #     self.login_btn.clicked.connect(lambda:on_login_clicked(self))

    #     # 레이아웃 설정
    #     layout.addWidget(self.name_input)
    #     layout.addWidget(self.email_input)
    #     layout.addWidget(self.login_btn)

    #     return widget # 생성된 창 반환
    
    def center_window(self):
        frame_geometry = self.frameGeometry()  # 창의 프레임 가져오기
        screen = QApplication.primaryScreen()  # 현재 사용 중인 화면 가져오기
        screen_geometry = screen.availableGeometry().center()  # 화면의 중앙 좌표
        frame_geometry.moveCenter(screen_geometry)  # 창의 중심을 화면 중심으로 이동
        self.move(frame_geometry.topLeft())  # 최종적으로 창을 이동