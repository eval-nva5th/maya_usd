try :
    from PySide6.QtWidgets import QWidget, QTableWidget
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QTableWidgetItem, QSizePolicy
    from PySide6.QtGui import QPixmap, QPainter, QColor
    from PySide6.QtWidgets import QHeaderView, QAbstractItemView
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PySide2.QtWidgets import QWidget, QTableWidget
        from PySide2.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QTableWidgetItem, QSizePolicy
        from PySide2.QtGui import QPixmap, QPainter, QColor
        from PySide2.QtWidgets import QHeaderView, QAbstractItemView
        from PySide2.QtCore import Qt
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
import data
    
def update_prev_work(prev_task_data):
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
    data.dept_name.setText(prev_task_step)
    data.user_name.setText(prev_task_assignee)
    data.reviewer_text.setText(prev_task_reviewers)
    print (data.comment_text)
    data.comment_text.setText(f'" {prev_task_comment} "')

    # status color update
    color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"} # 데이터로 빼야함.
    for k, v in color_map.items() :
        if prev_task_status == k :
            status_color = v
    
    status_pixmap = QPixmap(10, 10)  # 작은 원 크기 설정
    status_pixmap.fill(QColor("transparent"))  # 배경 투명
    painter = QPainter(status_pixmap)
    painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
    painter.setPen(QColor(status_color))  # 테두리도 빨간색
    painter.drawEllipse(0, 0, 10, 10)  # (x, y, width, height) 원 그리기
    painter.end()

    # state_image.setPixmap(status_pixmap)

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
    data.info_table.setCellWidget(3, 2, status_widget)

def previous_get_data(): #############################################순우work
    """
    외부에서 데이터를 받아서 테이블에 추가하는 함수
    """
    user_name = "No data"
    play_blast = f"/home/rapa/다운로드/output1.mov" #mov파일경로
    status_text = "fin"
    color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"} # 데이터로 빼야함.
    for k, v in color_map.items() :
        if status_text == k :
            status_color = v
    comment_text = "나는 나와의 싸움에서 졌다. 하지만 이긴것도 나다\n-장순우-"
    
    return previous_work_item(user_name, play_blast, status_color, status_text, comment_text)

def previous_work_item(user, pb, status_color, status_text, cmt_txt):
        """
        외부에서 데이터를 받아서 Previous_work에 추가하는 함수
        """
        from event import VideoPlayer
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
        data.info_table = QTableWidget(4, 3)
        data.info_table.verticalHeader().setVisible(False)  # 번호(인덱스) 숨기기
        data.info_table.horizontalHeader().setVisible(False)  # 가로 헤더 숨기기
        data.info_table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)  # 크기 조정 허용
        data.info_table.setMinimumHeight(data.info_table.sizeHint().height())  # 최소 높이 조정
        data.info_table.setMaximumHeight(data.info_table.sizeHint().height())  # 최대 높이도 맞춤
        data.info_table.resizeRowsToContents()
        data.info_table.resizeColumnsToContents()
        data.info_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        data.info_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        data.info_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        data.info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 편집 비활성화
        data.info_table.setSelectionMode(QAbstractItemView.NoSelection)  # 선택 불가
        data.info_table.setShowGrid(False)

        # 강제로 높이를 내부 아이템 크기에 맞춤
        data.info_table.setFixedHeight(data.info_table.verticalHeader().length() + 16)

        data.info_table.setStyleSheet("""
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
            data.info_table.setItem(row, 0, QTableWidgetItem(label))  # 0열 (항목명) 추가

            item = QTableWidgetItem(":")  # 1열 (콜론 `:`) 아이템 생성
            item.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬 적용
            data.info_table.setItem(row, 1, item)  # 1열에 아이템 추가

        data.dept_name = QTableWidgetItem("No data")
        data.user_name = QTableWidgetItem(user)
        data.reviewer_text = QTableWidgetItem("Not Assigned")
        
        data.info_table.setItem(0, 2, data.dept_name)   # Dept
        data.info_table.setItem(1, 2, data.user_name)  # Assignee
        data.info_table.setItem(2, 2, data.reviewer_text)  # Reviewer
        # data.info_table.setItem(3, 2, state_text)  # Status

        # COMMENT 영역
        comment_label = QLabel("Comment  :")
        comment_label.setStyleSheet("padding-left: 1px;")
        comment_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 왼쪽 정렬 + 수직 중앙 정렬
        comment_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 가로/세로 모두 텍스트에 맞춤
        comment_label.adjustSize()  # 크기를 텍스트에 딱 맞게 조정

        data.comment_text = QLabel(f'" {cmt_txt} "')
        data.comment_text.setStyleSheet("padding-top: 2px;padding-left: 1px;")
        data.comment_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        data.comment_text.setWordWrap(True)

        state_image = QLabel(status_color)      
        # state_text = QLabel(status_text)  
        
        
        # 원 색칠
        status_pixmap = QPixmap(10, 10)  # 작은 원 크기 설정
        status_pixmap.fill(QColor("transparent"))  # 배경 투명
        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
        painter.setPen(QColor(status_color))  # 테두리도 빨간색
        painter.drawEllipse(0, 0, 10, 10)  # (x, y, width, height) 원 그리기
        painter.end()
        state_image.setPixmap(status_pixmap)

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

        data.info_table.setCellWidget(3, 2, status_wdidget)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        # info_layout.addWidget(previous_work)
        info_layout.addWidget(data.info_table)
        info_layout.addWidget(comment_label)
        info_layout.addWidget(data.comment_text)

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