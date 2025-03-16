from PySide2.QtWidgets import QFileDialog, QMessageBox
import maya.cmds as cmds
import re
from DefaultConfig import DefaultConfig

default_config = DefaultConfig()
root_path = default_config.get_root_path()

def open_file_browser(ui_instance):
        default_filename = ui_instance.filename_input.text().strip()
        default_filepath = ui_instance.filepath_input.text() if ui_instance.filepath_input.text() else root_path # 이거 수정한거 물어보기

        filepath, _ = QFileDialog.getSaveFileName(None, "Select File Path", f"{default_filepath}{default_filename}", "All Files (*)")
        if filepath:
            ui_instance.filepath_input.setText(filepath)

def save_file_as(ui_instance):
        
        filename = ui_instance.filename_input.text().strip()
        filepath = ui_instance.filepath_input.text().strip()
        format_type = ui_instance.format_combo.currentText()
        
        if not filename or not filepath:
            QMessageBox.critical(ui_instance, "Error", "File name or File path does not exist", QMessageBox.Ok)
            return          

        full_path = f"{filepath}/{filename}{format_type}"
        
        # 파일 저장 및 버전업 로직 작성
        try:
            print(f"Saving file: {full_path}")
            # Maya 파일명 변경 및 저장
            cmds.file(rename=full_path)  # 파일명 변경
            if format_type == ".ma":
                cmds.file(save=True, type="mayaAscii")  # `.ma` 형식으로 저장
                QMessageBox.information(ui_instance, "Success", f"File saved: {full_path}", QMessageBox.Ok)
                ui_instance.close()
            if format_type == ".mb":
                cmds.file(save=True, type="mayaBinary")  # `.mb` 형식으로 저장
                QMessageBox.information(ui_instance, "Success", f"File saved: {full_path}", QMessageBox.Ok)
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