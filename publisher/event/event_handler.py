try:
    from PySide2.QtWidgets import QMessageBox
except:
    from PySide6.QtWidgets import QMessageBox

import os, re, shutil
import maya.cmds as cmds
from publisher.core.model_publish import model_publish
from publisher.core.lookdev_publish import lookdev_publish
from publisher.core.shot_publish import shot_publish

def publish(ui_instance, work_path, pub_path, project_name, entity_parent, entity_name, dept):

        filename = ui_instance.filename_input.text().strip()
        filepath = ui_instance.filepath_input.text().strip()
        format_type = ui_instance.format_combo.currentText()
        
        if not filename or not filepath:
            QMessageBox.critical(ui_instance, "Error", "File name or File path does not exist", QMessageBox.Ok)
            return

<<<<<<< HEAD
        model_publish (project_name, entity_parent, entity_name, dept)
        lookdev_publish (project_name, entity_parent, entity_name, dept)
        shot_publish (project_name, entity_parent, entity_name, dept)

        export_work_path = f"{work_path}/{filename}{format_type}"
        export_pub_path = f"{pub_path}/{filename}{format_type}"
        # 파일 저장 및 버전업 로직 작성
        try:
            print(f"Saving file: {work_path}")
            # Maya 파일명 변경 및 저장
            cmds.file(rename=export_work_path)  # 파일명 변경
            if format_type == ".ma":
                cmds.file(save=True, type="mayaAscii")  # `.ma` 형식으로 저장
                shutil.copy2(export_work_path, export_pub_path)
                QMessageBox.information(ui_instance, "완료", f"파일 퍼블리시 경로: {export_work_path} \n {export_pub_path}", QMessageBox.Ok)
                ui_instance.close()
            if format_type == ".mb":
                cmds.file(save=True, type="mayaBinary")  # `.mb` 형식으로 저장
                shutil.copy2(export_work_path, export_pub_path)
                QMessageBox.information(ui_instance, "완료", f"파일 퍼블리시 경로: {export_work_path} \n {export_pub_path}", QMessageBox.Ok)
=======
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
>>>>>>> e4aa7cc8f08c354681b68136afd74718df64b69a
                ui_instance.close()
        except FileNotFoundError:
            print("File path does not exist")
        except PermissionError:
            print("You do not have permission to save the file")
        except Exception as e:
            print(f"An unexpected error : {e}")

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