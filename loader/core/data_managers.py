# self.task_dict 순회 하면서 data 가공 후 add_task_to_table()

def task_data(ui_instance, task_table):
    ui_instance.task_info.get_user_task(ui_instance.user.get_userid())
    task_dict = ui_instance.task_info.get_task_dict()

    ui_instance.color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"}

    #{'proj_name': 'eval', 'content': 'bike_rig', 'entity_id': 1414, 'entity_type': 'assets',
    # 'entity_name': 'bike', 'start_date': '2025-02-17', 'due_date': '2025-02-19', 'status': 'fin',
    # 'step': 'Rig', 'entity_parent': 'Vehicle', 'prev_task_id': 5827, 'id': 5828}

    for task_id, task_data in task_dict.items() :
        # each_task = ClickedTask(task_id)

        # path = each_task.set_deep_path("pub", "data")
        # thumb = f"{path}/{each_task.entity_name}_{each_task.step}.jpg"

        task_name = task_data['content']

        proj_name = task_data['proj_name']
        entity_type = task_data['entity_type']
        entity_parent = task_data['entity_parent']
        entity_name = task_data['entity_name']

        status = task_data['status']
        step = task_data['step']

        start_date = task_data['start_date']
        due_date = task_data['due_date']
        

        thumb = f"/nas/eval/show/{proj_name}/{entity_type}/{entity_parent}/{entity_name}/{step}/pub/maya/data/{entity_name}_{step}_v001.jpg"

        # if entity_type == 'seq' : 
        #     low_data = task_data['shot_name']
        #     high_data = task_data['seq_name']
        #     thumb = f"/nas/eval/show/{proj_name}/seq/{high_data}/{low_data}/{step}/pub/maya/data/{low_data}_{step}_v001.jpg"
        #     print(thumb)

        # elif task_data['task_type'] == 'assets' :
        #     low_data = task_data['asset_name']
        #     high_data = task_data['asset_categ']
        #     thumb = f"/nas/eval/show/{proj_name}/assets/{high_data}/{low_data}/{step}/pub/maya/data/{low_data}_{step}_v001.jpg"
            
        for k, v in ui_instance.color_map.items() :
            if status == k :
                status_color = v
        data_set = f"{proj_name} | {entity_parent} | {entity_name}"

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
    
    #ui_instance.task_table_item(task_id, task_table, thumb, task_name, data_set, status_color, status, step, date_set)

def previous_data(ui_instance):
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        user_name = "No data"
        play_blast = f"/home/rapa/다운로드/output1.mov" #mov파일경로 ### 여기에 null file path 넣기 
        status_text = "fin"
        for k, v in ui_instance.color_map.items() :
            if status_text == k :
                status_color = v
        comment_text = "나는 나와의 싸움에서 졌다. 하지만 이긴것도 나다\n-장순우-"
        
        return ui_instance.previous_work_item(user_name, play_blast, status_color, status_text, comment_text)


# def version_file_data(ui_instance, version_type, file_path, file_list): ################### 이거 어떻게 할지에 대한 수정이 필요함
#         data = []
#         if version_type == "WORK":
#             try:
#                 ui_instance.work_table.cellClicked.disconnect()
#             except TypeError:
#                 print("TypeError Occured")
#                 pass  # Ignore if there are no connections yet
#             except RuntimeError:
#                 print(file_path, file_list)
#                 print("cellClicked 시그널이 연결되지 않았음")
        
#         if version_type == "PUB":
#             try:
#                 ui_instance.pub_table.cellClicked.disconnect()
#             except TypeError:
#                 print("TypeError Occured")
#                 pass  # Ignore if there are no connections yet
#             except RuntimeError:
#                 print(file_path, file_list)
#                 print("cellClicked 시그널이 연결되지 않았음")

#         if version_type == "WORK" :
#             if not file_path == "" :
#                 for file in file_list :
#                     data.append((file[0], file[1], file[2], file[3]))
#             else : 
#                 data = [(f"/nas/eval/elements/null.png", "no work yet", "", "")]

#         elif version_type == "PUB" :
#             if not file_path == "" :
#                 for file in file_list :
#                     data.append((file[0], file[1], file[2], file[3]))
#             else : 
#                 data = [
#                     (f"/nas/eval/elements/null.png", "no pub yet", "", "")
#                 ]
#         else :
#             print("something went wrong")
#             data = [
#                 (f"/nas/eval/elements/null.png", "something went wrong", "", "")
#             ]

#         if version_type == "WORK":
#             ui_instance.work_table.setRowCount(0)

#             for item in data:
#                 ui_instance.add_file_table_item(ui_instance.work_table, *item)

#         elif version_type == "PUB":
#             ui_instance.pub_table.setRowCount(0)
#             for item in data:
#                 ui_instance.add_file_table_item(ui_instance.pub_table, *item)