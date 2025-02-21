try :
    from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox, QTreeWidget
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTreeWidgetItem, QTableWidgetItem
    from PySide6.QtGui import QPixmap, QPainter, QColor
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QHeaderView
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox, QTreeWidget
        from PySide2.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTreeWidgetItem, QTableWidgetItem
        from PySide2.QtGui import QPixmap, QPainter, QColor
        from PySide2.QtCore import Qt
        from PySide2.QtWidgets import QHeaderView
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
import sys

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EVAL")

        self.login_window = self.login_ui()
        self.setCentralWidget(self.login_window)

        self.setGeometry(600, 300, 400, 200)

    def file_data(self):
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        data = [
            ("/home/rapa/my_eval/logo.jpeg", "v0001", "anim test", "25.02.20, 19:07:04", "InHo"),
            ("/home/rapa/my_eval/logo.jpeg", "v0002", "feedback implemented", "25.02.20, 9:07:04", "InHo"),
            ("/home/rapa/my_eval/logo.jpeg", "v0003", " ", "25.02.19, 19:07:04", "InHo")
        ]

        for item in data:
            self.file_table_item(*item)

    def file_table_item(self, dcc_logo, version, name, storage_time, user_name):
        row = self.file_table.rowCount()
        self.file_table.insertRow(row)  # 새로운 행 추가

        self.file_table.setRowHeight(row, 80)  # 행 높이 고정
        self.file_table.resizeRowsToContents()  # 자동 크기 조절 활성화

        # DCC 로고 + 버전 (QVBoxLayout 사용)
        dcc_widget = QWidget()
        dcc_layout = QVBoxLayout()
        file_logo = QLabel()
        pixmap = QPixmap(dcc_logo).scaled(80, 50)  # 크기 조절
        file_logo.setPixmap(pixmap)
        file_version = QLabel(version)

        dcc_layout.addWidget(file_logo)
        dcc_layout.addWidget(file_version)
        dcc_layout.setContentsMargins(5, 5, 5, 5)
        dcc_widget.setLayout(dcc_layout)
        self.file_table.setCellWidget(row, 0, dcc_widget)  # 첫 번째 열에 추가

        # 파일명 (QTableWidgetItem 사용)
        file_item = QTableWidgetItem(name)
        self.file_table.setItem(row, 1, file_item)  # 두 번째 열에 추가

        # 담당자 + 저장 날짜 (QVBoxLayout 사용)
        user_widget = QWidget()
        user_layout = QVBoxLayout()
        file_user_name = QLabel(user_name)
        file_save_time = QLabel(storage_time)

        user_layout.addWidget(file_user_name)
        user_layout.addWidget(file_save_time)
        user_layout.setContentsMargins(5, 5, 5, 5)

        user_widget.setLayout(user_layout)
        self.file_table.setCellWidget(row, 2, user_widget)  # 세 번째 열에 추가

        # 행 높이 조정
        self.file_table.setRowHeight(row, 80)

    def make_file_table(self):
        """
        File UI (테이블 목록) 생성
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테이블 위젯 생성 (초기 행 개수: 0, 3개 컬럼)
        self.file_table = QTableWidget(0, 3)
        self.file_table.setHorizontalHeaderLabels(["버전", "파일명", "담당자"])
        self.file_table.setColumnWidth(0, 100) # 각 행 크기
        self.file_table.setColumnWidth(1, 300) 
        self.file_table.setColumnWidth(2, 150)

        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)

        self.file_table.horizontalHeader().setStretchLastSection(True) # 마지막 칼럼 확장....!

        # UI 레이아웃 적용
        layout.addWidget(self.file_table)
        self.file_data()

        return widget  # QWidget 반환

    def show_department_list(self):
        """
        QTableWidget으로 Departments 리스트 출력
        """
        table = QTableWidget(4, 1)  # 4행 1열 테이블 생성
        table.setHorizontalHeaderLabels(["Departments"])  # 헤더 설정
        table.setColumnWidth(0, 200)  # 열 크기 설정
        table.verticalHeader().setVisible(False)  # 왼쪽 인덱스 숨기기
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # 편집 불가능

        departments = ["Layout", "Animation", "FX", "Lighting"]

        for row, dept in enumerate(departments):
            item = QTableWidgetItem(dept)  # 텍스트 아이템 생성
            item.setTextAlignment(Qt.AlignCenter) # 가운데 정렬
            table.setItem(row, 0, item)  # 테이블에 추가
            table.setRowHeight(row, 50)  # 행 높이 설정

        table.resizeRowsToContents()

        # 레이아웃 적용
        layout = QVBoxLayout()
        layout.addWidget(table)

        container = QWidget()
        container.setLayout(layout)

        return container

    def make_asset_seq_table(self):
        """
        Task & Sequence UI 로드
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)

        right_layout = QVBoxLayout()
        self.assets_btn = QPushButton("Assets")
        self.sequence_btn = QPushButton("Sequence")
        self.assets_btn.clicked.connect(self.assets_data)
        self.sequence_btn.clicked.connect(self.sequence_data)

        tab_layout = QHBoxLayout()
        tab_layout.addWidget(self.assets_btn)
        tab_layout.addWidget(self.sequence_btn)

        # 트리 리스트 (QTreeWidget)
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.itemClicked.connect(self.tree_item_clicked)
        right_layout.addLayout(tab_layout)
        right_layout.addWidget(self.tree_widget)

        # 오른쪽 컨테이너 생성
        right_container = QWidget()
        right_container.setLayout(right_layout)

        # 왼쪽 Task Table UI 생성
        self.left_container = self.make_task_table()

        # 맨 오른쪽 부서 컨테이너 추가
        end_right_container = self.show_department_list()

        # 맨 끝 부서 컨테이너 추가
        self.last_container = self.make_file_table()

        # 전체 레이아웃 적용 (순서 변경)
        layout.addWidget(self.left_container, 3) # 왼쪽
        layout.addWidget(right_container, 1) # 중간
        layout.addWidget(end_right_container, 1) # 오른쪽
        layout.addWidget(self.last_container, 1) # 맨끝

        # 메인 레이아웃 크기 비율 조정
        layout.setStretchFactor(self.left_container, 3)  # Task Table
        layout.setStretchFactor(right_container, 2)  # Sequence / Asset 트리
        layout.setStretchFactor(end_right_container, 1)  # Departments
        layout.setStretchFactor(self.last_container, 2)  # 파일 테이블

        # 기본 Sequence 데이터 로드 (UI 시작 시 기본 화면)
        self.sequence_data()
        return widget

    def sequence_data(self):
        """
        시퀀스 트리 데이터 로드
        """
        self.tree_widget.clear()
        parent_item = QTreeWidgetItem(["SQ01"])
        self.tree_widget.addTopLevelItem(parent_item)

        sequence_data = [
            ("SH0010", "thumbnail1.png"),
            ("SH0020", "thumbnail2.png"),
            ("SH0030", "thumbnail3.png"),
            ("SH0040", "thumbnail4.png")
        ]

        for shot_name, thumb_path in sequence_data:
            child_item = QTreeWidgetItem([shot_name])
            parent_item.addChild(child_item)

    def assets_data(self):
        """
        에셋 트리 데이터 로드
        """
        self.tree_widget.clear()
        parent_item = QTreeWidgetItem(["Assets"])
        self.tree_widget.addTopLevelItem(parent_item)

        assets_data = [
            ("Character", "character_icon.png"),
            ("Environment", "env_icon.png"),
            ("Props", "props_icon.png")
        ]

        for asset_name, thumb_path in assets_data:
            child_item = QTreeWidgetItem([asset_name])
            parent_item.addChild(child_item)

    def tree_item_clicked(self, item):
        """
        트리에서 선택한 항목을 테이블에 업데이트
        """
        selected_name = item.text(0)
        self.update_task_table(selected_name)

    def on_login_click(self):
        """
        로그인 버튼 실행
        """
        name = self.name_input.text()
        email = self.email_input.text()

        if name and email: #이름과 이메일에 값이 있을 때
            print ("이름과 메일 값이 들어왔다.")
            self.resize(1200, 700)  # 메인 화면 크기 조정
            self.setMinimumSize(1000, 600)  
            self.setCentralWidget(self.make_asset_seq_table()) # 로그인 창을 메인화면으로 변경
        else: # 이름과 이메일에 값이 없을 때
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("로그인 실패")
            popup.exec()

    def make_task_table(self):
        """
        Task UI (테이블 목록) 생성
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테스크 검색, 정렬 UI 생성
        task_label = QLabel("Task")
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
        self.task_table = QTableWidget(0, 2)
        self.task_table.setHorizontalHeaderLabels(["Thumbnail", "Task Info"])
        self.task_table.setColumnWidth(0, 150)  # 썸네일 크기
        self.task_table.setColumnWidth(1, 300)  # 텍스트 크기(날짜 포함)

        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.task_table.horizontalHeader().setStretchLastSection(True)

        # UI 레이아웃 적용
        layout.addLayout(h_layout)
        layout.addWidget(self.task_table)

        # 테스크 데이터 업데이트 
        self.task_data()
        return widget  # QWidget 반환

    def task_data(self):
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        data = [
            ("/home/rapa/my_eval/task.jpeg", "SQ03-SH0010", "Animation", "25.02.19 - 25.02.20", "#00CC66"),
            ("/home/rapa/my_eval/task.jpeg", "SQ03-SH0020", "Assets", "26.02.19 - 27.02.20", "#FFD700"),
            ("/home/rapa/my_eval/task.jpeg", "SQ03-SH0030", "Blocking", "28.02.19 - 01.03.20", "#FF4C4C")
        ]

        for item in data:
            self.task_table_item(*item)

    def task_table_item(self, thumb, file_name, type, deadline, status_color):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)  # 새로운 행 추가

        self.task_table.setRowHeight(row, 80)  
        self.task_table.resizeRowsToContents() 

        # 썸네일
        task_thumb = QLabel()
        pixmap = QPixmap(thumb)  # 이미지 파일 경로
        task_thumb.setPixmap(pixmap.scaled(120, 70))  # 크기 조절
        self.task_table.setCellWidget(row, 0, task_thumb)

        widget = QWidget()
        layout = QHBoxLayout()

        # 샷 이름
        task_name = QLabel(file_name)

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

        layout.addLayout(text_layout)  # 오른쪽: 텍스트 그룹
        layout.setContentsMargins(5, 5, 5, 5)  # 여백 조정
        widget.setLayout(layout)

        # 테이블 위젯 추가
        self.task_table.setCellWidget(row, 1, widget)

        # 행 높이를 조정하여 잘리지 않도록 설정
        self.task_table.setRowHeight(row, 80)

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
    app = QApplication(sys.argv)
    print ("UI 인스턴스 생성 시작")
    ui = UI()  # UI 클래스 실행
    print ("UI 인스턴스 생성 완료")
    ui.show() # 최고 짱짱 순우
    app.exec()