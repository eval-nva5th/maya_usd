try:
    from PySide6.QtWidgets import QLabel, QMessageBox, QWidget, QHBoxLayout
    from PySide6.QtGui import QPixmap, QPainter, QColor
except ImportError:
    from PySide2.QtWidgets import QLabel, QMessageBox, QWidget, QHBoxLayout
    from PySide2.QtGui import QPixmap, QPainter, QColor

from event.custom_dialog import CustomDialog
from core.video_player import VideoPlayer
from core.data_managers import version_file_data
import os

def on_login_clicked(ui_instance):
    """
    로그인 버튼 실행
    """
    name = ui_instance.name_input.text()
    email = ui_instance.email_input.text()
    if name and email: #이름과 이메일에 값이 있을 때
        is_validate = ui_instance.user.is_validate(email, name)
        if not is_validate:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("아이디 또는 이메일이 일치하지 않습니다")
            popup.exec()
        else:
            ui_instance.user_name = name
            ui_instance.setFixedSize(1100, 800)
            ui_instance.setCentralWidget(ui_instance.setup_layout()) # 로그인 창을 메인화면으로 변경
            ui_instance.center_window()

    else: # 이름과 이메일에 값이 없을 때
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle("Failure")
        popup.setText("이름과 이메일을 입력해주세요")
        popup.exec()

def on_cell_clicked(ui_instance, row, _):
    clicked_task_id = int(ui_instance.task_table.item(row, 2).text())
    pub_path, pub_list = ui_instance.task_info.get_pub_files(clicked_task_id)
    version_file_data(ui_instance, 'PUB', pub_path, pub_list)

    work_path , work_list = ui_instance.task_info.get_work_files(clicked_task_id)
    version_file_data(ui_instance, 'WORK', work_path, work_list)

    prev_task_data, current_task_data = ui_instance.task_info.on_click_task(clicked_task_id)
    prev_task_id = prev_task_data['id']

    update_prev_work(ui_instance, prev_task_data)

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
        print(file_path)
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

    # ui_instance.state_image.setPixmap(status_pixmap)

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


def on_work_cell_clicked(row, col, item, full_path) :
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
    # ui_instance.search_input.clear()