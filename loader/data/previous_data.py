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
        info_table = QTableWidget(4, 3)
        info_table.verticalHeader().setVisible(False)  # 번호(인덱스) 숨기기
        info_table.horizontalHeader().setVisible(False)  # 가로 헤더 숨기기
        info_table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)  # 크기 조정 허용
        info_table.setMinimumHeight(info_table.sizeHint().height())  # 최소 높이 조정
        info_table.setMaximumHeight(info_table.sizeHint().height())  # 최대 높이도 맞춤
        info_table.resizeRowsToContents()
        info_table.resizeColumnsToContents()
        info_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        info_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        info_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 편집 비활성화
        info_table.setSelectionMode(QAbstractItemView.NoSelection)  # 선택 불가
        info_table.setShowGrid(False)

        # 강제로 높이를 내부 아이템 크기에 맞춤
        info_table.setFixedHeight(info_table.verticalHeader().length() + 16)

        info_table.setStyleSheet("""
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
            info_table.setItem(row, 0, QTableWidgetItem(label))  # 0열 (항목명) 추가

            item = QTableWidgetItem(":")  # 1열 (콜론 `:`) 아이템 생성
            item.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬 적용
            info_table.setItem(row, 1, item)  # 1열에 아이템 추가

        dept_name = QTableWidgetItem("No data")
        user_name = QTableWidgetItem(user)
        reviewer_text = QTableWidgetItem("Not Assigned")
        
        info_table.setItem(0, 2, dept_name)   # Dept
        info_table.setItem(1, 2, user_name)  # Assignee
        info_table.setItem(2, 2, reviewer_text)  # Reviewer
        # info_table.setItem(3, 2, state_text)  # Status

        # COMMENT 영역
        comment_label = QLabel("Comment  :")
        comment_label.setStyleSheet("padding-left: 1px;")
        comment_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 왼쪽 정렬 + 수직 중앙 정렬
        comment_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 가로/세로 모두 텍스트에 맞춤
        comment_label.adjustSize()  # 크기를 텍스트에 딱 맞게 조정

        comment_text = QLabel(f'" {cmt_txt} "')
        comment_text.setStyleSheet("padding-top: 2px;padding-left: 1px;")
        comment_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        comment_text.setWordWrap(True)

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

        info_table.setCellWidget(3, 2, status_wdidget)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        # info_layout.addWidget(previous_work)
        info_layout.addWidget(info_table)
        info_layout.addWidget(comment_label)
        info_layout.addWidget(comment_text)

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