try : 
    from PySide2.QtWidgets import QMessageBox
except Exception :
    from PySide6.QtWidgets import QMessageBox

def publish(ui_instance):
        filename = ui_instance.filename_input.text().strip()
        filepath = ui_instance.filepath_input.text().strip()
        
        if not filename or not filepath:
            QMessageBox.critical(ui_instance, "Error", "File name or File path does not exist", QMessageBox.Ok)
            return          

        full_path = f"{filepath}{filename}"
        
        # 파일 저장 및 버전업 로직 작성
        try:
            print(f"퍼블리쉬 시도")
            ui_instance.close()
        except FileNotFoundError:
            print("File path does not exist")
        except PermissionError:
            print("You do not have permission to save the file")
        except Exception as e:
            print(f"An unexpected error : {e}")