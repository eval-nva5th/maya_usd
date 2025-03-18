try:
    from PySide2.QtWidgets import QMessageBox
except:
    from PySide6.QtWidgets import QMessageBox

import os, re
import maya.cmds as cmds

def save_file_as(ui_instance, version):
        print ("save_file_as 시작!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        filename = ui_instance.filename_input.text().strip()
        filepath = ui_instance.filepath_input.text().strip()
        format_type = ui_instance.format_combo.currentText()
        
        if not filename or not filepath:
            QMessageBox.critical(ui_instance, "Error", "File name or File path does not exist", QMessageBox.Ok)
            return          

        full_path = f"{filepath}/{filename}{format_type}"
        print ("퍼블리쉬 풀 패스!!!!!!!!!!!!!!!!!", full_path)

        new_path = convert_to_save_path(full_path)
        new_save_path = f"{new_path}/{filename}_{format_type}_{version}"
        print ("파일 네임 ", filename)
        print ("파일 타입", format_type)
        print ("퍼블리쉬 마야 저장 경로!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", new_save_path)
        
        # 파일 저장 및 버전업 로직 작성
        try:
            print(f"Saving file: {new_save_path}")
            # Maya 파일명 변경 및 저장
            cmds.file(rename=new_save_path)  # 파일명 변경
            if format_type == ".ma":
                cmds.file(save=True, type="mayaAscii")  # `.ma` 형식으로 저장
                QMessageBox.information(ui_instance, "Success", f"File saved: {new_save_path}", QMessageBox.Ok)
                ui_instance.close()
            if format_type == ".mb":
                cmds.file(save=True, type="mayaBinary")  # `.mb` 형식으로 저장
                QMessageBox.information(ui_instance, "Success", f"File saved: {new_save_path}", QMessageBox.Ok)
                ui_instance.close()
        except FileNotFoundError:
            print("File path does not exist")
        except PermissionError:
            print("You do not have permission to save the file")
        except Exception as e:
            print(f"An unexpected error : {e}")

def convert_to_save_path(file_path):
    """새로 저장할 경로"""
    directory_path = os.path.dirname(file_path)  
    path_parts = directory_path.strip("/").split("/")  

    if "work" in path_parts:
        work_index = path_parts.index("work")
        path_parts[work_index] = "pub"

    new_path = "/" + "/".join(path_parts)
    return new_path

def on_version_click(ui_instance, file_name):
    match = re.search(r"(.*)_v(\d+)$", file_name)
    if ui_instance.version_btn.isChecked():
        ui_instance.version_btn.setText("version down")
        base_name = match.group(1)  # "IronMan_model"
        version_number = int(match.group(2)) + 1  # 숫자 증가
        new_file_name = f"{base_name}_v{version_number:03d}"  # v### 형식 유지
        ui_instance.filename_input.setText(new_file_name)
    else:
        ui_instance.version_btn.setText("version up")
        ui_instance.filename_input.setText(file_name)