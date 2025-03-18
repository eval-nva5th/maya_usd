from systempath import SystemPath
root_path = SystemPath().get_root_path()
import os

# self.task_dict 순회 하면서 data 가공 후 add_task_to_table()

def task_data(ui_instance, task_table):
    #ui_instance.task_info.get_user_task(ui_instance.user.get_userid())
    task_dict = ui_instance.task_info.get_task_dict()

    ui_instance.color_map = {"ip": "#00CC66", "fin": "#868e96", "wtg": "#FF4C4C"}

    # {'proj_name': 'eval', 'content': 'bike_rig', 'entity_id': 1414, 'entity_type': 'assets',
    # 'entity_name': 'bike', 'start_date': '2025-02-17', 'due_date': '2025-02-19', 'status': 'fin',
    # 'step': 'Rig', 'entity_parent': 'Vehicle', 'prev_task_id': 5827, 'id': 5828}

    for task_id, task_data in task_dict.items() :

        task_name = task_data['content']

        proj_name = task_data['proj_name']
        entity_type = task_data['entity_type']
        entity_parent = task_data['entity_parent']
        entity_name = task_data['entity_name']

        status = task_data['status']
        step = task_data['step']

        start_date = task_data['start_date']
        due_date = task_data['due_date']
        

        thumb = f"{root_path}/show/{proj_name}/{entity_type}/{entity_parent}/{entity_name}/{step}/pub/maya/data/{entity_name}_{step}.jpg"
        if not os.path.exists(thumb):
            thumb = f"{root_path}/elements/no_image.jpg"
        else:
            pass

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

def previous_data(ui_instance):
        """
        외부에서 데이터를 받아서 테이블에 추가하는 함수
        """
        user_name = "NULL"
        play_blast = f"{root_path}/elements/no_video.mp4" #mov파일경로 ### 여기에 null file path 넣기 
        status_text = "fin"
        for k, v in ui_instance.color_map.items() :
            if status_text == k :
                status_color = v
        comment_text = "NULL"
        
        return ui_instance.previous_work_item(user_name, play_blast, status_color, status_text, comment_text)