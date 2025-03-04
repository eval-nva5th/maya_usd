import os
import shutil
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget

def put_into_path():

    app = QApplication([])
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setDirectory("/nas/sy_test_folder/encoding_trial") 
    
    if file_dialog.exec_():
        file_name = file_dialog.selectedFiles()[0]

        root_path = "/nas/eval/show"
        project_name = "eval"
        #project_name = input("project name : ")
        set_type = "1"
        #set_type = input("work type (assets = 1, seq = 2) : ")

        if set_type == "1":
            set_type_str = "assets"
            raw, _ = os.path.splitext(os.path.basename(file_name))
            splited = raw.split('_')
            index = len(splited)
            task_type = splited[index-2]
            ver = splited[index-1]
            asset_name = raw.replace(f"_{task_type}_{ver}", "")
            work_type = "pub"

            asset_type = input("asset type (prop: 1, vehicle: 2, character: 3, environment: 4) : ")
            
            if asset_type == "1":
                asset_type = "prop"
            elif asset_type == "2":
                asset_type = "vehicle"
            elif asset_type == "3":
                asset_type = "character"
            elif asset_type == "4":
                asset_type = "environment"

            path = f"{root_path}/{project_name}/{set_type_str}/{asset_type}/{asset_name}/{task_type}/{work_type}/maya/data/"
            #print(path)

            if not os.path.exists(path):
                os.makedirs(path)

            destination_file = os.path.join(path, os.path.basename(file_name))
            shutil.copy2(file_name, destination_file)
                
            print(f"옮겨짐 {destination_file}")

        elif set_type == "2":
            raw, _ = os.path.splitext(os.path.basename(file_name))
            splited = raw.split('_')
            set_type_str = "seq"
            seq_name = splited[0]
            shot_name = f"{splited[0]}_{splited[1]}"
            task_type = splited[2]
            #ver = splited[3]
            
            work_types = ["pub"]
            for work_type in work_types :
                path = f"{root_path}/{project_name}/{set_type_str}/{seq_name}/{shot_name}/{task_type}/{work_type}/maya/data/"

                if not os.path.exists(path):
                    os.makedirs(path)

                destination_file = os.path.join(path, os.path.basename(file_name))
                shutil.copy2(file_name, destination_file)
                
                print(f"옮겨짐 {destination_file}")
    
        else:
            print("무언가문제가잇음")

# 함수 실행
if __name__ == "__main__":
    put_into_path()