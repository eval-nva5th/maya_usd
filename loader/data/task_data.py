try :
    from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHBoxLayout
    from PySide6.QtWidgets import QVBoxLayout, QLabel
    from PySide6.QtGui import QPixmap, QPainter, QColor
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PySide2.QtWidgets import QWidget, QTableWidgetItem, QHBoxLayout
        from PySide2.QtWidgets import QVBoxLayout, QLabel
        from PySide2.QtGui import QPixmap, QPainter, QColor
        from PySide2.QtCore import Qt
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
from shotgrid_user_task import TaskInfo
import data
def task_table_item(task_data_dict):
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

# task_dict 순회 하면서 data 가공 후 add_task_to_table()
def task_get_data(task_table):
    data.task_info = TaskInfo(data.sg_url, data.script_name, data.api_key)
    data.task_info.get_user_task(data.user.get_userid())
    task_dict = data.task_info.get_task_dict()

    color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"}

    for task_id, task_data in task_dict.items() :
        
        task_name = task_data['content']
        proj_name = task_data['proj_name']
        status = task_data['status']
        step = task_data['step']
        start_date = task_data['start_date']
        due_date = task_data['due_date']

        if task_data['task_type'] == 'Shot' : 
            low_data = task_data['shot_name']
            high_data = task_data['seq_name']
            thumb = f"/nas/eval/show/{proj_name}/seq/{high_data}/{low_data}/{step}/pub/maya/data/{low_data}_{step}_v001.jpg"
            print(thumb)

        elif task_data['task_type'] == 'Asset' :
            low_data = task_data['asset_name']
            high_data = task_data['asset_categ']
            thumb = f"/nas/eval/show/{proj_name}/assets/{high_data}/{low_data}/{step}/pub/maya/data/{low_data}_{step}_v001.jpg"
            
        for k, v in color_map.items() :
            if status == k :
                status_color = v
        data_set = f"{proj_name} | {high_data} | {low_data}"

        task_new_dict = {
            "task_id": task_id,
            "task_table": task_table,
            "thumb": thumb,
            "task_name": task_name,
            "data_set": data_set,
            "status_color": status_color,
            "status": status,
            "step": step,
            "start_date": start_date,
            "due_date": due_date
        }
        
        data.task_data_dict.append(task_new_dict)