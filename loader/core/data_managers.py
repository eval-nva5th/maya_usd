# self.task_dict 순회 하면서 data 가공 후 add_task_to_table()
def task_data(ui_instance, task_table):
    ui_instance.task_info.get_user_task(ui_instance.user.get_userid())
    task_dict = ui_instance.task_info.get_task_dict()

    ui_instance.color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"}

    for task_id, task_data in task_dict.items() :
        
        task_name = task_data['content']
        proj_name = task_data['proj_name']
        status = task_data['status']
        step = task_data['step']
        start_date = task_data['start_date']
        due_date = task_data['due_date']

        if task_data['task_type'] == 'Shot' : 
            low_data = task_data['shot_name']
            high_data = task_data['seq_name']
            thumb = f"/nas/eval/show/{proj_name}/seq/{high_data}/{low_data}/{step}/pub/maya/data/{low_data}_{step}_v001.jpg"
            print(thumb)

        elif task_data['task_type'] == 'Asset' :
            low_data = task_data['asset_name']
            high_data = task_data['asset_categ']
            thumb = f"/nas/eval/show/{proj_name}/assets/{high_data}/{low_data}/{step}/pub/maya/data/{low_data}_{step}_v001.jpg"
            
        for k, v in ui_instance.color_map.items() :
            if status == k :
                status_color = v
        data_set = f"{proj_name} | {high_data} | {low_data}"

        new_dict = {
            "task_id": task_id,
            "task_table": task_table,
            "thumb": thumb,
            "task_name": task_name,
            "data_set": data_set,
            "status_color": status_color,
            "status": status,
            "step": step,
            "start_date": start_date,
            "due_date": due_date
        }
        
        ui_instance.task_data_dict.append(new_dict)
    
    # ui_instance.task_table_item(task_id, task_table, thumb, task_name, data_set, status_color, status, step, date_set)


def previous_data(ui_instance):
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        user_name = "No data"
        play_blast = f"/home/rapa/다운로드/output1.mov" #mov파일경로
        status_text = "fin"
        for k, v in ui_instance.color_map.items() :
            if status_text == k :
                status_color = v
        comment_text = "나는 나와의 싸움에서 졌다. 하지만 이긴것도 나다\n-장순우-"
        
        return ui_instance.previous_work_item(user_name, play_blast, status_color, status_text, comment_text)

def version_file_data(ui_instance, version_type, file_path, file_list):
        data = []
        if version_type == "WORK":
            try:
                ui_instance.work_table.cellClicked.disconnect()
            except TypeError:
                print("TypeError Occured")
                pass  # Ignore if there are no connections yet
            except RuntimeError:
                print("cellClicked 시그널이 연결되지 않았음")
        
        if version_type == "PUB":
            try:
                ui_instance.pub_table.cellClicked.disconnect()
            except TypeError:
                print("TypeError Occured")
                pass  # Ignore if there are no connections yet
            except RuntimeError:
                print("cellClicked 시그널이 연결되지 않았음")

        if version_type == "WORK" :
            if not file_path == "" :
                for file in file_list :
                    data.append((file[0], file[1], file[2], file[3]))
            else : 
                data = [(f"/nas/eval/elements/null.png", "no work yet", "", "")]

        elif version_type == "PUB" :
            if not file_path == "" :
                for file in file_list :
                    data.append((file[0], file[1], file[2], file[3]))
            else : 
                data = [
                    (f"/nas/eval/elements/null.png", "no pub yet", "", "")
                ]
        else :
            print("something went wrong")
            data = [
                (f"/nas/eval/elements/null.png", "something went wrong", "", "")
            ]

        if version_type == "WORK":
            ui_instance.work_table.setRowCount(0)
            
            #ui_instance.work_table.cellClicked.connect(ui_instance.on_work_cell_click)
            for item in data:
                ui_instance.file_table_item(ui_instance.work_table, *item)

        elif version_type == "PUB":
            ui_instance.pub_table.setRowCount(0)
            for item in data:
                ui_instance.file_table_item(ui_instance.pub_table, *item)