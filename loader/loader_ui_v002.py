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
import sys
import cv2
import numpy as np
import shotgun_api3
from shotgrid_user_task import UserInfo, TaskInfo
import os
import time
import sys, subprocess
# from ui import login_view

class CustomDialog(QDialog):
    def __init__(self, full_path, file_name):
        super().__init__()

        # Set up the dialog layout
        # Create two LineEdits
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(file_name)
        self.line_edit.setFixedWidth(300)
        self.switch = QToolButton(self)
        self.switch.setCheckable(True)

        self.switch.setText(".mb")
        self.switch.setStyleSheet("""
            QToolButton {
                background-color: #ccc;
                border-radius: 10px;
                padding: 5px;
                color: white;
                background-color : #a47864;
                            
            }
            QToolButton:checked {
                background-color: #6667AB;
            }
            QToolButton:!checked {
                background-color: #a47864;
            }
        """)

        self.switch.clicked.connect(self.on_toggle)

        self.create_button = QPushButton("Create", self)
        self.exit_button = QPushButton("Exit", self)
        
        self.create_button.clicked.connect(lambda: self.on_click_create(full_path))
        self.exit_button.clicked.connect(self.on_click_exit)

        text_layout = QHBoxLayout()
        text_layout.addWidget(self.line_edit)
        text_layout.addWidget(self.switch)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.exit_button)

        full_layout = QVBoxLayout()
        full_layout.addLayout(text_layout)
        full_layout.addLayout(button_layout)

        self.setLayout(full_layout)
        self.setWindowTitle("create new work file")
        
    def on_toggle(self):
        if self.switch.isChecked():
            self.switch.setText(".ma")
        else:
            self.switch.setText(".mb")

    def on_click_create(self, full_path):
        line_edit_text = self.line_edit.text()
        ext = self.switch.text()
        run_path = f"{full_path}/{line_edit_text}{ext}"
        print(run_path)
        self.dialog_flag = False
        self.accept()  # Close the dialog

    def on_click_exit(self) :
        print("종료")
        self.dialog_flag = False
        self.accept()

class UI(QMainWindow):
    def __init__(self):
        sg_url = "https://hi.shotgrid.autodesk.com/"
        script_name = "Admin_SY"
        api_key = "kbuilvikxtf5v^bfrivDgqhxh"
        self.user = UserInfo(sg_url, script_name, api_key)
        self.user_name = ""
        self.task_info = TaskInfo(sg_url, script_name, api_key)
        self.prefix_path = "/nas/eval/show"

        self.task_data_dict = []
        
        super().__init__()  
        self.setWindowTitle("EVAL_LOADER")
        self.center_window()

        self.login_window = login_view()
        self.setCentralWidget(self.login_window)

    
    
    def version_file_data(self, version_type, file_path, file_list):
        data = []
        if version_type == "WORK":
            try:
                self.work_table.cellClicked.disconnect()
            except TypeError:
                print("이상하네")
                pass  # Ignore if there are no connections yet
            except RuntimeError:
                print("cellClicked 시그널이 연결되지 않았음")
        
        if version_type == "PUB":
            try:
                self.pub_table.cellClicked.disconnect()
            except TypeError:
                print("이상하네2")
                pass  # Ignore if there are no connections yet
            except RuntimeError:
                print("cellClicked 시그널이 연결되지 않았음")

        if version_type == "WORK" :
            if not file_path == "" :
                for file in file_list :
                    data.append((file[0], file[1], file[2], file[3]))
            else : 
                data = [(f"/nas/eval/elements/null.png", "no work yet", "", "")]

        elif version_type == "PUB" :
            if not file_path == "" :
                for file in file_list :
                    data.append((file[0], file[1], file[2], file[3]))
            else : 
                data = [
                    (f"/nas/eval/elements/null.png", "no pub yet", "", "")
                ]
        else :
            print("something went wrong")
            data = [
                (f"/nas/eval/elements/null.png", "something went wrong", "", "")
            ]

        if version_type == "WORK":
            self.work_table.setRowCount(0)
            
            #self.work_table.cellClicked.connect(self.on_work_cell_clicked)
            for item in data:
                self.file_table_item(self.work_table, *item)

        elif version_type == "PUB":
            self.pub_table.setRowCount(0)
            for item in data:
                self.file_table_item(self.pub_table, *item)
    
    def file_table_item(self, table_widget, dcc_logo, file_name, edited_time, full_path):
        
        row = table_widget.rowCount()
        table_widget.insertRow(row)  # 새로운 행 추가

        #DCC 로고
        file_logo = QLabel()
        pixmap = QPixmap(dcc_logo).scaled(25, 25)  # 크기 조절
        file_logo.setPixmap(pixmap)
        #file_logo.setScaledContents(True) # 크기에 맞게 이미지가 자동으로 축소/확대됨.
        file_logo.setAlignment(Qt.AlignCenter)
        table_widget.setCellWidget(row, 0, file_logo)  # 첫 번째 열에 추가

        # 파일명 (QTableWidgetItem 사용)
        name_table = QTableWidgetItem(f"{file_name}")
        table_widget.setItem(row, 1, name_table)  # 두 번째 열에 추가
        # print(file_name)

        # 저장 날짜 
        time_table = QTableWidgetItem(f"{edited_time}")
        table_widget.setItem(row, 2, time_table)  # 세 번째 열에 추가
        # print(edited_time)

        table_widget.cellClicked.connect(lambda row, col : self.on_work_cell_clicked(row, col, table_widget.item(row,col), full_path))

    def on_work_cell_clicked(self, row, col, item, full_path) :
    # item과 관련된 작업을 처리
        if item.text() ==  "Double Click for new work file" :
            print("여기서 아이템 생성 시작")
            print(full_path)
            path_slice = full_path.split('/')
            file_name =  f"{path_slice[7]}_{path_slice[8]}_v001"
            dialog = CustomDialog(full_path, file_name)
            dialog.exec()

        else :
            print(f"Row: {row}, Column: {col}, Item: {full_path}")
            #subprocess.run(["maya", "-file", full_path], check=True) 
    def on_sort_changed(self):
        """
        콤보박스 선택 변경 시 정렬 수행
        """
        selected_option = self.sort_combo.currentText()

        if selected_option == "ascending order":
            ascending = True
        elif selected_option == "descending order":
            ascending = False
        else:
            return  # 정렬이 아닌 경우 종료

        self.sort_table_by_due_date(self.task_table, ascending)

    def sort_table_by_due_date(self, table_widget, ascending=True):
        tuple_list = []
        for index, data in enumerate(self.task_data_dict):
            due_date = data["due_date"] 
            data_index_tuple = (due_date, index)
            tuple_list.append(data_index_tuple)

        tuple_list.sort(key=lambda x: x[0], reverse=not ascending)

        new_task_list = []
        for _, index  in tuple_list:
            new_task_list.append(self.task_data_dict[index])

        table_widget.setRowCount(0)

        self.task_table_item(new_task_list)

    def search_task(self):
        """
        검색 기능
        """
        search_text = self.search_input.text().strip().lower()

        for row in range(self.task_table.rowCount()):
            item = self.task_table.cellWidget(row, 1)  # Task Info 컬럼의 내용을 가져옴
            if item:
                labels = item.findChildren(QLabel)  # QLabel들 가져오기
                match = False
                for label in labels:
                    if search_text in label.text().lower():  # 검색어가 포함된 경우
                        match = True
                        break

                self.task_table.setRowHidden(row, not match)  # 일치하지 않으면 숨김
        # self.search_input.clear()

    # self.task_dict 순회 하면서 data 가공 후 add_task_to_table()
    def task_data(self, task_table):
        self.task_info.get_user_task(self.user.get_userid())
        task_dict = self.task_info.get_task_dict()

        self.color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"}

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
                
            for k, v in self.color_map.items() :
                if status == k :
                    status_color = v
            data_set = f"{proj_name} | {high_data} | {low_data}"

            new_dict = {
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
            
            self.task_data_dict.append(new_dict)
        
        # self.task_table_item(task_id, task_table, thumb, task_name, data_set, status_color, status, step, date_set)

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

    def on_cell_clicked(self, row, _):
        clicked_task_id = int(self.task_table.item(row, 2).text())
        pub_path, pub_list = self.task_info.get_pub_files(clicked_task_id)
        self.version_file_data('PUB', pub_path, pub_list)

        work_path , work_list = self.task_info.get_work_files(clicked_task_id)
        self.version_file_data('WORK', work_path, work_list)

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

    def center_window(self):
        frame_geometry = self.frameGeometry()  # 창의 프레임 가져오기
        screen = QApplication.primaryScreen()  # 현재 사용 중인 화면 가져오기
        screen_geometry = screen.availableGeometry().center()  # 화면의 중앙 좌표
        frame_geometry.moveCenter(screen_geometry)  # 창의 중심을 화면 중심으로 이동
        self.move(frame_geometry.topLeft())  # 최종적으로 창을 이동