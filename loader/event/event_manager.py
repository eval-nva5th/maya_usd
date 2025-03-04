try :
    from PySide6.QtWidgets import QMessageBox, QApplication, QTableWidget, QLabel
except ImportError:
    try:
        from PySide2.QtWidgets import QMessageBox, QApplication, QTableWidget, QLabel
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
import data
from shotgrid_user_task import UserInfo, TaskInfo
from ui.main_ui import MainView
from .dialog import CustomDialog

def on_sort_changed():
    """
    콤보박스 선택 변경 시 정렬 수행
    """
    selected_option = data.sort_combo.currentText()

    if selected_option == "ascending order":
        ascending = True
    elif selected_option == "descending order":
        ascending = False
    else:
        return  # 정렬이 아닌 경우 종료

    sort_table_by_due_date(data.task_table, ascending)

def sort_table_by_due_date(table_widget, ascending=True):
    tuple_list = []
    print (f"data.task_data_dict : {data.task_data_dict}")
    for index, info in enumerate(data.task_data_dict):
        due_date = info["due_date"] 
        data_index_tuple = (due_date, index)
        tuple_list.append(data_index_tuple)

    tuple_list.sort(key=lambda x: x[0], reverse=not ascending)

    new_task_list = []
    for _, index  in tuple_list:
        new_task_list.append(data.task_data_dict[index])

    table_widget.setRowCount(0)

    data.task_table_item(new_task_list)

def search_task():
    """
    검색 기능
    """
    search_text = data.search_input.text().strip().lower()

    for row in range(data.task_table.rowCount()):
        item = data.task_table.cellWidget(row, 1)  # Task Info 컬럼의 내용을 가져옴
        if item:
            labels = item.findChildren(QLabel)  # QLabel들 가져오기
            match = False
            for label in labels:
                if search_text in label.text().lower():  # 검색어가 포함된 경우
                    match = True
                    break

            data.task_table.setRowHidden(row, not match)  # 일치하지 않으면 숨김

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

def on_cell_clicked(row, column):
    # 테스크 테이블 선택시 진행되는 함수
    clicked_task_id = int(data.task_table.item(row, 2).text())
    print (clicked_task_id)
    pub_path, pub_list = data.task_info.get_pub_files(clicked_task_id)
    data.version_file_data('PUB', pub_path, pub_list)

    work_path , work_list = data.task_info.get_work_files(clicked_task_id)
    print('get_work_files', work_path , work_list)
    data.version_file_data('WORK', work_path, work_list)

    prev_task_data, current_task_data = data.task_info.on_click_task(clicked_task_id)
    print('prev_task_data', prev_task_data)
    prev_task_id = prev_task_data['id']
    print('prev_task_id',prev_task_id)
    data.update_prev_work(prev_task_data)

def on_login_click():
    """
    로그인 버튼 실행
    """
    app = QApplication.instance()  #현재 실행 중인 QApplication 가져오기
    main_window = MainView()
    app.main_window = main_window
    
    name = data.name_input.text()
    email = data.email_input.text()
    data.user = UserInfo(data.sg_url, data.script_name, data.api_key)

    if name and email: #이름과 이메일에 값이 있을 때
        is_validate = data.user.is_validate(email, name)
        print (f"is_validate : {is_validate}")
        if not is_validate:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("아이디 또는 이메일이 일치하지 않습니다")
            popup.exec()
        else:
            user_name = name
            main_window.resize(1100, 800)  # 메인 화면 크기 조정
            main_window.setCentralWidget(main_window.setup_layout()) # 로그인 창을 메인화면으로 변경
            main_window.center_window()
            main_window.show()
            data.loginView.close()

    else: # 이름과 이메일에 값이 없을 때
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle("Failure")
        popup.setText("이름과 이메일을 입력해주세요")
        popup.exec()
