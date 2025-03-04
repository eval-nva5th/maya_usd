from PySide6.QtWidgets import QFileDialog, QMessageBox

def open_file_browser(ui_instance):
        default_filename = ui_instance.filename_input.text().strip()
        default_filepath = ui_instance.filepath_input.text() if ui_instance.filepath_input.text() else "/nas/eval/"

        filepath, _ = QFileDialog.getSaveFileName(None, "Select File Path", f"{default_filepath}{default_filename}", "All Files (*)")
        if filepath:
            ui_instance.filepath_input.setText(filepath)


def save_file_as(ui_instance):
        filename = ui_instance.filename_input.text().strip()
        filepath = ui_instance.filepath_input.text().strip()
        
        if not filename or not filepath:
            QMessageBox.critical(ui_instance, "Error", "File name or File path does not exist", QMessageBox.Ok)
            return          

        full_path = f"{filepath}{filename}"
        
        # 파일 저장 및 버전업 로직 작성
        try:
            print(f"{full_path}에 파일 저장 시도")
            ui_instance.close()
        except FileNotFoundError:
            print("File path does not exist")
        except PermissionError:
            print("You do not have permission to save the file")
        except Exception as e:
            print(f"An unexpected error : {e}")