try :
    from PySide6.QtWidgets import QLabel, QTableWidgetItem
    from PySide6.QtGui import QPixmap
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PySide2.QtWidgets import QLabel, QTableWidgetItem
        from PySide2.QtGui import QPixmap
        from PySide2.QtCore import Qt
        import re
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
# from event import on_work_cell_clicked

def file_table_item(table_widget, dcc_logo, file_name, edited_time, full_path):
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

    # table_widget.cellClicked.connect(lambda row, col : on_work_cell_clicked(row, col, table_widget.item(row,col), full_path))

def version_file_data(version_type, file_path, file_list):
    print('version_file_data', version_type, file_path, file_list)
    # data = []
    # if version_type == "WORK":
    #     try:
    #         work_table.cellClicked.disconnect()
    #     except TypeError:
    #         print("이상하네")
    #         pass  # Ignore if there are no connections yet
    #     except RuntimeError:
    #         print("cellClicked 시그널이 연결되지 않았음")
    
    # if version_type == "PUB":
    #     try:
    #         pub_table.cellClicked.disconnect()
    #     except TypeError:
    #         print("이상하네2")
    #         pass  # Ignore if there are no connections yet
    #     except RuntimeError:
    #         print("cellClicked 시그널이 연결되지 않았음")

    # if version_type == "WORK" :
    #     if not file_path == "" :
    #         for file in file_list :
    #             data.append((file[0], file[1], file[2], file[3]))
    #     else : 
    #         data = [(f"/nas/eval/elements/null.png", "no work yet", "", "")]

    # elif version_type == "PUB" :
    #     if not file_path == "" :
    #         for file in file_list :
    #             data.append((file[0], file[1], file[2], file[3]))
    #     else : 
    #         data = [
    #             (f"/nas/eval/elements/null.png", "no pub yet", "", "")
    #         ]
    # else :
    #     print("something went wrong")
    #     data = [
    #         (f"/nas/eval/elements/null.png", "something went wrong", "", "")
    #     ]

    # if version_type == "WORK":
    #     work_table.setRowCount(0)
        
    #     #work_table.cellClicked.connect(on_work_cell_clicked)
    #     for item in data:
    #         file_table_item(work_table, *item)

    # elif version_type == "PUB":
    #     pub_table.setRowCount(0)
    #     for item in data:
    #         file_table_item(pub_table, *item)