try : 
    from PySide2.QtWidgets import QLabel, QMessageBox, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
    from PySide2.QtGui import QPixmap, QPainter, QColor, Qt
except Exception :
    from PySide6.QtWidgets import QLabel, QMessageBox, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
    from PySide6.QtGui import QPixmap, QPainter, QColor, Qt
    
import maya.cmds as cmds
import maya.utils as mu
import os, sys
from loader.shotgrid_user_task import ClickedTask
from loader.event.custom_dialog import CustomDialog
from shotgrid_user_task import UserInfo, TaskInfoThread
from loader.ui import loader_ui
from core.add_new_task import *
from systempath import SystemPath
from shotgridapi import ShotgridAPI

from loader.ui.loading_ui import LoadingDialog
from PySide2.QtWidgets import QApplication

root_path = SystemPath().get_root_path()
sg = ShotgridAPI().shotgrid_connector()

#from loader.core.data_managers import version_file_data

def on_login_clicked(ui_instance):                        # 1번 실행중
    """
    로그인 버튼 실행
    """
    user = UserInfo()

    name = ui_instance.name_input.text()
    email = ui_instance.email_input.text()

    if name and email: #이름과 이메일에 값이 있을 때
        is_validate = user.is_validate(email, name)
        if not is_validate:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("아이디 또는 이메일이 일치하지 않습니다")
            popup.exec()

        # else: # 로그인 성공!
        #     ui_instance.close()
        #     main_window = loader_ui.UI()
        #     main_window.user = user
        #     main_window.user_name = name
        #     main_window.input_name = name
        #     main_window.setFixedSize(1100, 800)
        #     main_window.setCentralWidget(main_window.setup_layout()) # 로그인 창을 메인화면으로 변경
        #     main_window.center_window()
        #     main_window.show()

        else:  # 로그인 성공!
            ui_instance.close()

            # 로딩창 먼저 띄우기
            ui_instance.loading_window = LoadingDialog()
            ui_instance.loading_window.show()
            QApplication.processEvents()  # UI 즉시 업데이트

            ui_instance.task_thread = TaskInfoThread(user.id)
            ui_instance.task_thread.start()
            print("case~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            ui_instance.task_thread.finished_signal.connect(
                lambda task_info: show_loader_ui(user, name, ui_instance.loading_window, task_info)
            )

    else: # 이름과 이메일에 값이 없을 때
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle("Failure")
        popup.setText("이름과 이메일을 입력해주세요")
        popup.exec()

def show_loader_ui(user, name, loading_window, task_info):
    """
    로딩이 끝나면 로더 UI 실행
    """
    print("case~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~qqqq")
    loader_window = loader_ui.UI(task_info)
    loader_window.user = user
    loader_window.user_name = name
    loader_window.input_name = name
    loader_window.setFixedSize(1100, 800)
    loader_window.setCentralWidget(loader_window.setup_layout())
    loader_window.center_window()

    # TaskInfo 설정
    #loader_window.set_task_info(task_info)
    # 로딩창 닫기
    loading_window.close()
    # 로더 UI 실행
    loader_window.show()

def on_cell_clicked(ui_instance, row, _):
    if not ui_instance:
        return
    clicked_task_id = int(ui_instance.task_table.item(row, 2).text())
    
    prev_task_data, current_task_data = ui_instance.task_info.on_click_task(clicked_task_id)
    update_prev_work(ui_instance, prev_task_data)

    ct = ClickedTask(current_task_data)
    pub_path = ct.set_deep_path("pub")
    work_path = ct.set_deep_path("work")

    #file_name = ct.set_file_name()
    pub_list = ct.get_dir_items(pub_path)
    work_list = ct.get_dir_items(work_path)
    update_pub_table(ui_instance, pub_path, pub_list)
    update_work_table(ui_instance, work_path, work_list)
    
    try:
        ui_instance.work_table.cellDoubleClicked.disconnect()
    except Exception as e:
        print(e)
        pass  # 연결된 핸들러가 없을 경우 예외 발생할 수 있음, 무시해도 됨
    
    ui_instance.work_table.cellDoubleClicked.connect(lambda row, col: on_work_cell_clicked(ui_instance,ui_instance.work_table, row, col, ct, work_path))

def update_pub_table(ui_instance, pub_path, pub_list):

    ui_instance.pub_table.setRowCount(0)

    for file_info in pub_list:
        # Example of file_info: ["/nas/eval/elements/null.png", "Click for new dir and file", "", path]
        add_file_to_table(ui_instance.pub_table, file_info)

def update_work_table(ui_instance, work_path, work_list):

    ui_instance.work_table.setRowCount(0)  # Clear existing rows

    for file_info in work_list:
        add_file_to_table(ui_instance.work_table, file_info)

def add_file_to_table(table_widget, file_info):

    row = table_widget.rowCount()
    table_widget.insertRow(row)
    table_widget.setHorizontalHeaderLabels(["", "파일 이름", "최근 수정일"])
    table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
    table_widget.setColumnWidth(0, 30)  # 로고 열 (좁게 설정)
    table_widget.setColumnWidth(1, 330)  # 파일명 열 (길게 설정)
    table_widget.setColumnWidth(2,126)
    table_widget.verticalHeader().setDefaultSectionSize(30)
    table_widget.horizontalHeader().setVisible(True) 
    table_widget.verticalHeader().setVisible(False)

    # 로고
    image_label = QLabel()
    pixmap = QPixmap(file_info[0]).scaled(25, 25)
    image_label.setPixmap(pixmap)
    image_label.setAlignment(Qt.AlignCenter)
    table_widget.setCellWidget(row, 0, image_label)

    # File name or message
    file_item = QTableWidgetItem(file_info[1])
    table_widget.setItem(row, 1, file_item)

    # Edited time 
    time_item = QTableWidgetItem(file_info[2]) #if file_info[2] else "Unknown")
    table_widget.setItem(row, 2, time_item)

def on_work_cell_clicked(ui_instance, table_widget, row, col, ct, path):
    from widget.ui.widget_ui import add_custom_ui_to_tab

    item = table_widget.item(row, col)
    print(ct)
    print(ct.entity_name, ct.content, ct.step)
    print(path)
    print(ct.set_file_name())
    print(f"Clicked item: {item.text()} at row {row}, column {col}")

    if item.text() == "No Dir No File":
       print(f"Open directory or create a new file at path")
       print(ct.set_file_name())
       is_dir, is_created = False, False
       if not is_created :
        dialog = CustomDialog(path, is_dir, is_created, ct)
        dialog.exec()
        # mainwindow 종료
        ui_instance.close()

    elif item.text() ==  "No File" :
        print("o directory x file")
        print(ct.set_file_name())
        is_dir, is_created = True, False
        if not is_created :
            print(ct.entity_name, ct.content) 
            dialog = CustomDialog(path, is_dir,is_created, ct)
            dialog.exec()
            #### mainwindow 종료
            ui_instance.close()

    else :
        full_path = f"{path}/{item.text()}"
        cmds.file(full_path, open=True, force=True)
        #### mainwindow 종료 
        ui_instance.close()

        add_custom_ui_to_tab(path, ct) ##### 위젯 넣는 함수
    

def update_prev_work(ui_instance, prev_task_data):
    prefix_path = f"{root_path}/show"
    file_path_list = []
    if prev_task_data['id'] != "None":
        print(prev_task_data)
        prev_task_id = prev_task_data['id']
        prev_task_name = prev_task_data['task_name']
        prev_task_assignee = prev_task_data['assignees']
        prev_task_reviewers = prev_task_data['reviewers']
        prev_task_status = prev_task_data['status']
        prev_task_step = prev_task_data['step']
        prev_task_comment = prev_task_data['comment']
        prev_task_project_name = prev_task_data['proj_name']
        if prev_task_data['type_name'] == "shot" :
            prev_task_type_name = "seq"
        elif prev_task_data['type_name'] == "asset" :
            prev_task_type_name = "assets"
        prev_task_category_name = prev_task_data['category']
        prev_task_n = prev_task_data['name']
        dir_path = os.path.join(prefix_path, prev_task_project_name, prev_task_type_name, prev_task_category_name, prev_task_n, prev_task_step,"pub/maya/data")
        file_name = f"{prev_task_n}_{prev_task_step}.mov"
        file_path = f"{dir_path}/{file_name}"

    else :
        prev_task_id = "No data"
        prev_task_name = "No data"
        prev_task_assignee = "No data"
        prev_task_reviewers = "No data"
        prev_task_status = "fin"
        prev_task_step = "No data"
        prev_task_comment = "No data for previous work"
        prev_task_project_name = "No data"
        prev_task_type_name = "No data"
        prev_task_category_name = "No data"
        file_path = ""

    # 테이블 업데이트
    ui_instance.dept_name.setText(prev_task_step)
    ui_instance.user_name.setText(prev_task_assignee)
    ui_instance.reviewer_text.setText(prev_task_reviewers)
    ui_instance.comment_text.setText(f'" {prev_task_comment} "')

    # status color update
    for k, v in ui_instance.color_map.items() :
        if prev_task_status == k :
            status_color = v
    
    status_pixmap = QPixmap(10, 10)  # 작은 원 크기 설정
    status_pixmap.fill(QColor("transparent"))  # 배경 투명
    painter = QPainter(status_pixmap)
    painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
    painter.setPen(QColor(status_color))  # 테두리도 빨간색
    painter.drawEllipse(0, 0, 10, 10)  # (x, y, width, height) 원 그리기
    painter.end()

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
    ui_instance.info_table.setCellWidget(3, 2, status_widget)
    ui_instance.video_widget.set_new_mov_file(file_path)

def on_sort_changed(ui_instance):
    """
    콤보박스 선택 변경 시 정렬 수행
    """
    selected_option = ui_instance.sort_combo.currentText()

    if selected_option == "data : latest":
        ascending = True
    elif selected_option == "date : earlist":
        ascending = False
    else:
        return  # 정렬이 아닌 경우 종료

    sort_table_by_due_date(ui_instance, ui_instance.task_table, ascending)

def sort_table_by_due_date(ui_instance, table_widget, ascending=True):
    tuple_list = []
    print(12345,ui_instance.task_data_dict)
    for index, data in enumerate(ui_instance.task_data_dict):
        due_date = data["due_date"] 
        data_index_tuple = (due_date, index)
        tuple_list.append(data_index_tuple)

    tuple_list.sort(key=lambda x: x[0], reverse=not ascending)

    new_task_list = []
    for _, index  in tuple_list:
        new_task_list.append(ui_instance.task_data_dict[index])

    table_widget.setRowCount(0)

    ui_instance.task_table_item(new_task_list)

def search_task(ui_instance):
    """
    검색 기능
    """
    search_text = ui_instance.search_input.text().strip().lower()

    for row in range(ui_instance.task_table.rowCount()):
        item = ui_instance.task_table.cellWidget(row, 1)  # Task Info 컬럼의 내용을 가져옴
        if item:
            labels = item.findChildren(QLabel)  # QLabel들 가져오기
            match = False
            for label in labels:
                if search_text in label.text().lower():  # 검색어가 포함된 경우
                    match = True
                    break

            ui_instance.task_table.setRowHidden(row, not match)  # 일치하지 않으면 숨김