
from PySide2.QtWidgets import QLabel, QMessageBox, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
from PySide2.QtGui import QPixmap, QPainter, QColor, Qt
import maya.cmds as cmds
import maya.utils as mu

import os, sys
from shotgrid_user_task import ClickedTask
from loader.event.custom_dialog import CustomDialog
from shotgrid_user_task import UserInfo
from loader.ui.loader_ui import UI
# from loader.core.data_managers import version_file_data

sys.path.append("/home/rapa/gitkraken/maya_usd/loader")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/core")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/event")
sys.path.append("/home/rapa/gitkraken/maya_usd/loader/ui")
sys.path.append("/home/rapa/gitkraken/maya_usd/widget") 
widget_ui_path = os.path.abspath("/home/rapa/gitkraken/maya_usd/widget/ui")
sys.path.append(widget_ui_path)

def on_login_clicked(ui_instance):                        ######################### 1번 실행중
    """
    로그인 버튼 실행
    """
    sg_url = "https://hi.shotgrid.autodesk.com/"
    script_name = "Admin_SY"
    api_key = "kbuilvikxtf5v^bfrivDgqhxh"
    user = UserInfo(sg_url, script_name, api_key)

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

        else: # 로그인 성공!
            ui_instance.close()
            loader_ui = UI()
            loader_ui.user = user
            loader_ui.user_name = name
            loader_ui.input_name = name
            loader_ui.setFixedSize(1100, 800)
            loader_ui.setCentralWidget(loader_ui.setup_layout()) # 로그인 창을 메인화면으로 변경
            loader_ui.center_window()
            loader_ui.show()

    else: # 이름과 이메일에 값이 없을 때
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle("Failure")
        popup.setText("이름과 이메일을 입력해주세요")
        popup.exec()

def on_cell_clicked(ui_instance, row, _):
    if not ui_instance:
        return
    clicked_task_id = int(ui_instance.task_table.item(row, 2).text())
    
    prev_task_data, current_task_data = ui_instance.task_info.on_click_task(clicked_task_id)
    update_prev_work(ui_instance, prev_task_data)

    ct = ClickedTask(current_task_data)
    pub_path = ct.set_deep_path("pub")
    work_path = ct.set_deep_path("work")
    file_name = ct.set_file_name()
    pub_list = ct.get_dir_items(pub_path)
    work_list = ct.get_dir_items(work_path)

    update_pub_table(ui_instance, pub_path, pub_list)
    update_work_table(ui_instance, work_path, work_list)
    print(pub_list, work_list)
    ui_instance.work_table.cellClicked.connect(lambda row, col: on_work_cell_clicked(ui_instance.work_table, row, col, work_path, file_name, ct))

def update_pub_table(ui_instance, pub_path, pub_list):

    ui_instance.pub_table.setRowCount(0)

    for file_info in pub_list:
        # Example of file_info: ["/nas/eval/elements/null.png", "Click for new dir and file", "", path]
        add_file_to_table(ui_instance.pub_table, file_info)

def update_work_table(ui_instance, work_path, work_list):

    ui_instance.work_table.setRowCount(0)  # Clear existing rows

    for file_info in work_list:
        add_file_to_table(ui_instance.work_table, file_info)

    #ui_instance.work_table.cellClicked.connect(lambda row, col: on_work_cell_clicked(ui_instance, file_info[3], row, col))

def add_file_to_table(table_widget, file_info):

    row = table_widget.rowCount()
    table_widget.insertRow(row)

    table_widget.setHorizontalHeaderLabels(["", "파일 이름", "최근 수정일"])
    table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 전체 행 선택
    table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 편집 비활성화
    table_widget.setColumnWidth(0, 30)  # 로고 열 (좁게 설정)
    table_widget.setColumnWidth(1, 330)  # 파일명 열 (길게 설정)
    table_widget.setColumnWidth(2,126)
    table_widget.verticalHeader().setDefaultSectionSize(30)
    table_widget.verticalHeader().setVisible(False)

    # Image (DCC logo)
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

def on_work_cell_clicked(table_widget, row, col, path, file_name, ct):
    from widget_ui import CustomUI, add_custom_ui_to_tab

    item = table_widget.item(row, col)
    print(f"Clicked item: {item.text()} at row {row}, column {col}")

    if item.text() == "No Dir No File":
        print(f"Open directory or create a new file at path")
        is_dir = False
        dialog = CustomDialog(path, file_name, is_dir, ct)
        dialog.exec()

    elif item.text() ==  "No File" :
        print("o directory x file")
        is_dir = True
        dialog = CustomDialog(path, file_name, is_dir, ct)
        dialog.exec()

    else :
        full_path = f"{path}/{item.text()}"
        cmds.file(full_path, open=True) ################################################################파일여는부분
        print(ct.entity_id, ct.id, ct.proj_id)

        print(f"{item.text()}가 열립니다.") 

        add_custom_ui_to_tab(path)
        customUI = CustomUI(path, ct)
        customUI.exec()

def update_prev_work(ui_instance, prev_task_data):
    prefix_path = "/nas/eval/show"
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