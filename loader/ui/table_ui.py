try :
    from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox, QDialog
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy, QToolButton
    from PySide6.QtGui import QPixmap, QPainter, QColor, QImage, QFont
    from PySide6.QtWidgets import QHeaderView, QAbstractItemView
    from PySide6.QtCore import Qt, QTimer
    from datetime import datetime
    import re
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
        from PySide2.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy
        from PySide2.QtGui import QPixmap, QPainter, QColor, QImage, QFont
        from PySide2.QtWidgets import QHeaderView, QAbstractItemView
        from PySide2.QtCore import Qt, QTimer
        from datetime import datetime
        import re
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")

def make_task_table():
        """
        Task UI (테이블 목록) 생성
        """
        widget = QWidget()  # 새 UI 위젯 생성
        layout = QVBoxLayout(widget)

        # 테스크 검색, 정렬 UI 생성
        task_label = QLabel("TASK")
        task_label.setStyleSheet("font-weight: bold;")
        search_input = QLineEdit() # 검색창
        search_but = QPushButton("SEARCH") # 검색버튼
        sort_combo = QComboBox()
        sort_combo.addItem("ascending order")  # 오름차순 정렬
        sort_combo.addItem("descending order")  # 내림차순 정렬

        # 테스크 검색, 정렬 레이아웃 정렬
        h_layout = QHBoxLayout()
        h_layout.addWidget(task_label)
        h_layout.addWidget(search_input)
        h_layout.addWidget(search_but)
        h_layout.addWidget(sort_combo)

        # 테이블 위젯 생성 (초기 행 개수: 0, 2개 컬럼)
        task_table = QTableWidget(0, 3)
        task_table.setHorizontalHeaderLabels(["Thumbnail", "Task Info", "Task ID"])
        task_table.setColumnHidden(2, True) # Task ID 숨김

        # # 테이블 이벤트 처리
        # task_table.cellClicked.connect(on_cell_clicked)
        # search_but.clicked.connect(search_task)
        # search_input.returnPressed.connect(search_task)
        # search_input.textChanged.connect(search_task)
        # sort_combo.currentIndexChanged.connect(on_sort_changed)

        # 테이블 크기설정
        task_table.setColumnWidth(0, 180)  # 로고 열 (좁게 설정)
        task_table.setColumnWidth(1, 300)  # 파일명 열 (길게 설정)
        task_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
        task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  # 로고 고정
        task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 파일명 확장
        task_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # 편집 비활성화
        task_table.resizeRowsToContents()
        task_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        task_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 가로 스크롤바 항상 숨김
        task_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 세로 스크롤바 넘치면 표시
        task_table.verticalHeader().setVisible(False) #행번호 숨김

        # UI 레이아웃 적용
        none_label = QLabel()
        layout.addWidget(none_label)
        layout.addLayout(h_layout)
        layout.addWidget(task_table)

        # 테스크 데이터 업데이트 
        # task_data(task_table)
        # task_table_item(task_data_dict)
        return widget  # QWidget 반환

def make_file_table(version_type):
    """
    File UI (테이블 목록) 생성
    version_type: "work" 또는 "pub"
    """
    
    widget = QWidget()  # 새 UI 위젯 생성
    layout = QVBoxLayout(widget)
    print ({f"version_type : {version_type}"})
    if version_type == "PUB":
        pub_table = QTableWidget(0, 3)
        table = pub_table  # Assign to pub_table
    elif version_type == "WORK":
        work_table = QTableWidget(0, 3)
        table = work_table  # Assign to work_table
        
    table.setHorizontalHeaderLabels(["", "파일 이름", "최근 수정일"])
    table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 편집 비활성화
    table.setColumnWidth(0, 30)  # 로고 열 (좁게 설정)
    table.setColumnWidth(1, 330)  # 파일명 열 (길게 설정)
    table.setColumnWidth(2,126)
    table.verticalHeader().setDefaultSectionSize(30)
    table.verticalHeader().setVisible(False)

    table.setAlternatingRowColors(True)
    layout.addWidget(table)

    file_path = ""
    file_list = ["NULL"]
    # version_file_data(version_type, file_path, file_list)

    return widget  # QWidget 반환