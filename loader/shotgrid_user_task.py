try :
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import QThread, Signal, QMetaObject, Qt
except Exception :
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QThread, Signal, QMetaObject, Qt
    
from shotgun_api3 import Shotgun 

import os, sys, time
from loader.ui.loading_ui import LoadingDialog
from systempath import SystemPath
from shotgridapi import ShotgridAPI

root_path = SystemPath().get_root_path()
sg = ShotgridAPI().shotgrid_connector()

class TaskInfoThread(QThread):
    finished_signal = Signal(object)  # 리스트 형태로 TaskInfo 데이터 전달

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # user_id 저장

    def run(self):
        task_info = TaskInfo()
        task_info.get_user_task(self.user_id)
        task_dict = task_info.get_task_dict()  # Task 데이터 가져오기
        self.finished_signal.emit(task_info)  # 완료 신호 전달 

class UserInfo : 
    def __init__(self) :
        
        self.email = ""
        self.name = ""
        self.dept = ""
        self.pos = ""
        
    def is_validate(self, email, name) :
        '''
        샷그리드에서 받아온 두 값과 내부 데이터를 비교
        '''
        self.email = email
        self.name = name
        kname_filter = ['sg_korean_name', 'is', self.name]
        email_filter = ['email', 'is', self.email]
        self.userinfo = sg.find('HumanUser', [kname_filter, email_filter], ["id", "name", "department", "groups"])
        
        if not len(self.userinfo) == 0 :
            self.id = self.userinfo[0]['id'] # id 받기
            self.dept = self.userinfo[0]['department']['name'] # DEPT 받기
            self.pos = self.userinfo[0]['groups'][0]['name'] # 포지션 받기 
            return 1

        else :
            return 0
        
class TaskInfo :
    def __init__(self):
        self.task_thread = None
        self.task_dict = {}
        self.prev_task_dict = {}

    def get_user_task(self, user_id):
        #UserInfo에서 갖고온 id를 파라미터로 갖고와 그 아이디에 해당하는 태스크를 딕트 형식으로 저장
        '''
        로딩창 실행 코드인데 잠시 주석처리 해두었습니다!
        '''
        id_filter = {'type': 'HumanUser', 'id': user_id}
        tasks = sg.find("Task", [["task_assignees", "is", id_filter]], ["project", "content", "entity", "start_date", "due_date","sg_status_list", "step"])
        total_tasks = len(tasks)
        print(f"할당된 태스크 정보를 가져오는 중입니다 ... 총 {total_tasks}개")

        for i, task in enumerate(tasks, start=1) :
            progress_text = (f"처리 중: {i}/{total_tasks} ({(i/total_tasks)*100:.2f}%) 완료")
            print (progress_text)

            current_task_id = task['id']
            proj_name = task['project']['name']
            proj_id = task['project']['id']
            task_name = task['content']
            entity_name = task['entity']['name']
            entity_type = task['entity']['type']
            entity_id = task['entity']['id']
            start_date = task['start_date']
            due_date = task['due_date']
            status = task['sg_status_list']
            step = task['step']['name']

            self.task_dict[current_task_id] = {}
            self.task_dict[current_task_id]['assignee_id'] = user_id
            self.task_dict[current_task_id]['proj_id'] = proj_id
            self.task_dict[current_task_id]['proj_name']=proj_name
            self.task_dict[current_task_id]['content']=task_name
            self.task_dict[current_task_id]['entity_id'] = entity_id
            self.task_dict[current_task_id]['entity_type']=entity_type
            self.task_dict[current_task_id]['entity_name'] = entity_name
            self.task_dict[current_task_id]['start_date']=start_date
            self.task_dict[current_task_id]['due_date']=due_date
            self.task_dict[current_task_id]['status']=status
            self.task_dict[current_task_id]['step'] = step

            #{5828: {'proj_name': 'eval', 'content': 'bike_rig', 'entity_name': 'bike', 'entity_type': 'Asset', 'start_date': '2025-02-17', 'due_date': '2025-02-19', 'status': 'fin', 'step': 'Rig'}

            self.branch_entity_type(entity_type, current_task_id, entity_id) # asset seq로 딕트 형식/저장방법 분기
            prev_task_id = self.get_prev_task(current_task_id)
            self.task_dict[current_task_id]['prev_task_id'] = prev_task_id
    
            if prev_task_id :
                # ShotGrid에서 Description data 가져오기 
                fields = ["id", "code", "description", "published_file_type", "entity"]
                filters = [["task", "is", {"type": "Task", "id": prev_task_id}]]

                published_file = sg.find_one("PublishedFile", filters, fields)
                if not published_file :
                    comment = "None"
                else : 
                    comment = published_file.get('description') #, 'No Description')
                #comment = comment['description']

                # ShotGrid에서 Previous Task data 가져오기
                prev_task_data = sg.find_one(
                                                "Task", 
                                                [["id", "is", prev_task_id]], 
                                                ["project","content", "entity","step", "task_assignees","task_reviewers", "sg_status_list"]
                                                )
                
                prev_task_proj = prev_task_data['project']['name']
                entity_type = prev_task_data['entity']['type']
                entity_id = prev_task_data['entity']['id']
                if entity_type == "Shot":
                    entity_data = sg.find_one("Shot", [["id", "is", entity_id]], ["sg_sequence"])
                    prev_task_category = entity_data.get("sg_sequence", {}).get("name", "No Sequence")

                elif entity_type == "Asset":
                    entity_data = sg.find_one("Asset", [["id", "is", entity_id]], ["sg_asset_type"])
                    prev_task_category = entity_data.get("sg_asset_type", "No Asset Type")
                
                prev_task_name = prev_task_data['entity'].get('name') or prev_task_data['entity'].get('name')
                prev_task_id = prev_task_data['id']
                prev_task_task_name = prev_task_data['content']
                prev_task_step = prev_task_data['step']['name']
                prev_task_assignees = [assignee['name'] for assignee in prev_task_data['task_assignees']]
                prev_task_reviewers = [reviewer['name'] for reviewer in prev_task_data['task_reviewers']]
                prev_task_status = prev_task_data['sg_status_list']
                prev_task_assignees = ", ".join(prev_task_assignees)
                prev_task_reviewers = ", ".join(prev_task_reviewers)

                self.prev_task_dict[prev_task_id] = {}
                self.prev_task_dict[prev_task_id]["proj_name"] = prev_task_proj
                self.prev_task_dict[prev_task_id]["type_name"] = entity_type.lower()
                self.prev_task_dict[prev_task_id]["category"] = prev_task_category
                self.prev_task_dict[prev_task_id]["name"] = prev_task_name            

                self.prev_task_dict[prev_task_id]["task_name"] = prev_task_task_name
                self.prev_task_dict[prev_task_id]["step"] = prev_task_step.lower()
                self.prev_task_dict[prev_task_id]["assignees"] = prev_task_assignees
                self.prev_task_dict[prev_task_id]["reviewers"] = prev_task_reviewers
                self.prev_task_dict[prev_task_id]["status"] = prev_task_status
                self.prev_task_dict[prev_task_id]["comment"] = comment
                
            else :
                pass

    def branch_entity_type(self, entity_type, task_id, entity_id) :

        if entity_type == "Shot" :
            seq_contents = sg.find("Shot", [["id", "is", entity_id]], ["tasks", "sg_sequence"])
            
            seq_name = seq_contents[0]['sg_sequence']['name']
            self.task_dict[task_id]['entity_type'] = "seq"
            self.task_dict[task_id]['entity_parent'] = seq_name
            
        elif entity_type == "Asset" :
            asset_contents = sg.find("Asset", [["id", "is", entity_id]], ["tasks", "sg_asset_type"])

            asset_category_name = asset_contents[0]['sg_asset_type']
            self.task_dict[task_id]['entity_type'] = "assets"
            self.task_dict[task_id]['entity_parent'] = asset_category_name

    def get_task_dict(self) :
        return self.task_dict
    
    def get_prev_task(self, task_id) :
        # 현재 태스크 정보
        current_task = self.task_dict[task_id]
        if not current_task:
            return None
        
        # type_id(shot_id/asset_id)이 같은 태스크들 찾기
        related_tasks = []
        type_id = current_task.get("entity_id") #or current_task.get("asset_id")
        filters = [
            {
                "filter_operator": "or",
                "filters": [
                    ["entity", "is", {"type": "Shot", "id": type_id}],
                    ["entity", "is", {"type": "Asset", "id": type_id}]
                ]
            }
        ]

        # 가져올 필드 목록
        fields = ["id", "content", "step", "sg_status_list", "task_assignees"]

        # ShotGrid API에서 태스크 조회
        tasks = sg.find("Task", filters, fields)

        for task in tasks:
            task_assignees = " ,".join([assignee['name'] for assignee in task['task_assignees']])
            t = {}
            t["content"] = task['content']
            t["step"] = task['step']['name']
            t["status"] = task['sg_status_list']
            t["assignees"] = task_assignees
            related_tasks.append((task['id'], t))     

        # for task_id, task in self.task_dict.items():
        #     if task.get("shot_id") == type_id or task.get("asset_id") == type_id :
        #         related_tasks.append((task_id, task))
        
        # 현재 태스크의 스텝
        current_step = current_task['step'].lower()
        # 스텝 매핑 해줄 스텝맵
        step_map = {
        "rig": ["model"],
        "texture": ["model"],
        "animation": ["layout"],
        "light": ["animation", "layout"]
        }

        # 현재 스텝이 model/layout이면 None
        if current_step in {"model", "layout"}:
            return None
        
        # 스텝 맵을 사용한 이전 스텝 찾기
        prev_steps = step_map.get(current_step, None)
        if not prev_steps:
            return None
        
        # type_name(shot_name/asset_name)이 같은 태스크 리스트에서 이전 스텝인 태스크 아이디 찾기
        for prev_step in prev_steps:
            for prev_task_id, prev_task in reversed(related_tasks):
                if prev_task.get("step").lower() == prev_step:
                    return prev_task_id
        return None

    # asset 일 시 {5828: {'proj_name': 'eval', 'content': 'bike_rig', 'entity_id': 1414, 'entity_type': 'assets', 'entity_name': 'bike', 'start_date': '2025-02-17', 'due_date': '2025-02-19', 'status': 'fin', 'step': 'Rig', 'entity_parent': 'Vehicle', 'prev_task_id': 5827}
    def on_click_task(self, id) : # 특정 태스크의 아이디에 해당하는 내부 정보들을 딕트의 형식으로 리턴
        current_task_id = id
        current_dict = {}
        current_dict = self.task_dict[current_task_id]
        current_dict["id"] = current_task_id
        
        prev_task_dict = {}
        prev_task_id = self.task_dict[current_task_id]['prev_task_id']
        if self.prev_task_dict.get(prev_task_id) == None :
            prev_task_dict["id"] = 0
            prev_task_dict["proj_name"] = ""
            prev_task_dict["type_name"] = ""
            prev_task_dict["category"] = ""
            prev_task_dict["name"] = ""            

            prev_task_dict["task_name"] = ""
            prev_task_dict["step"] = ""
            prev_task_dict["assignees"] = ""
            prev_task_dict["reviewers"] = ""
            prev_task_dict["status"] = ""
            prev_task_dict["comment"] = ""
            
        else :
            prev_task = self.prev_task_dict[prev_task_id]
            prev_task_dict["id"] = prev_task_id
            prev_task_dict["proj_name"] = prev_task['proj_name']
            prev_task_dict["type_name"] = prev_task['type_name']
            prev_task_dict["category"] = prev_task['category']
            prev_task_dict["name"] = prev_task['name']            

            prev_task_dict["task_name"] = prev_task['task_name']
            prev_task_dict["step"] = prev_task['step']
            prev_task_dict["assignees"] = prev_task['assignees']
            prev_task_dict["reviewers"] = prev_task['reviewers']
            prev_task_dict["status"] = prev_task['status']
            prev_task_dict["comment"] = prev_task['comment']
        return prev_task_dict, current_dict

class ClickedTask:

    def __init__(self, id_dict):
        '''
        태스크 테이블을 클릭 시 이 클래스 객체가 생성됨.
        하나의 태스크 딕트형식을 파라미터로 갖고오며 그 값을 바탕으로 클래스 변수와 함수를 생성하였음. 
        '''
        self.id = id_dict["id"]
        self.assignee_id = id_dict["assignee_id"]
        self.content = id_dict["content"]
        self.proj_id = id_dict["proj_id"]
        self.project_name = id_dict["proj_name"]
        self.entity_id = id_dict["entity_id"]
        self.entity_type = id_dict["entity_type"]
        self.entity_name = id_dict["entity_name"]
        self.entity_parent = id_dict['entity_parent']
        self.step = id_dict['step'].lower()
        self.status = id_dict['status']
        self.root_path = f"{root_path}/show"

    def __repr__(self):
        return f"ClickedTask(id={self.id}, project_id={self.proj_id}, project_name={self.project_name}, entity_id = {self.entity_id}, entity_type = {self.entity_type}, entity_parent ={self.entity_parent}, step={self.step})"
    
    def set_base_path(self):
        base_path = f"{self.root_path}/{self.project_name}/{self.entity_type}/{self.entity_parent}/{self.entity_name}"
        return base_path
    
    def set_shallow_path(self):
        shallow_path = f"{self.root_path}/{self.project_name}/{self.entity_type}/{self.entity_parent}/{self.entity_name}/{self.step}"
        return shallow_path
    
    def set_deep_path(self, pub_or_work, dcc_type = "maya", export_type="scenes") :
        '''
        파라미터에 따라 필요한 패스를 쉽게 만들 수 있음. 
        '''
        deep_path = f"{self.root_path}/{self.project_name}/{self.entity_type}/{self.entity_parent}/{self.entity_name}/{self.step}/{pub_or_work}/{dcc_type}/{export_type}"
        return deep_path

    def set_file_name(self) :
        file_name =  f"{self.entity_name}_{self.step}_v001"
        return file_name

    def get_dir_items(self, deep_path) :
        '''
        파라미터로 받아온 패스에 파일이 없을 시 테이블에 위 상황을 출력한다.
        그리고 파일이 존재하는 경우는 내림차순 형식으로 파일을 저장하고 이중리스트 형식으로 리턴. 
        '''
        data_list = []

        if not os.path.exists(deep_path) :
            full_path = f"{deep_path}/{self.set_file_name()}"
            data_list.append([f"{root_path}/elements/null.png", "No Dir No File", "", full_path])
        else : 
            data_list = self.set_file_list(deep_path)
            full_path = f"{deep_path}/{self.set_file_name()}"
            if  len(data_list) > 1 :
                sorted_list = sorted(data_list, key=lambda x: int(x[1].split('_v')[-1].split('.')[0]) if '_v' in x[1] and '.' in x[1] else 0, reverse=True) # 버전 내림차순 정렬 (+예외처리 )
                data_list = sorted_list
            elif len(data_list) == 0 :
                data_list.append([f"{root_path}/elements/null.png", "No File", "", full_path])
        
        return data_list
    
    def set_file_list(self, path) :
        '''
        생성한 패스를 순회하며 각 파일에 관한 정보를 리스트의 형식으로 만들고, 그 묶음을 리스트로 저장한다.
        '''
        data_list = []

        for file in os.listdir(path):
            if '.' in file:
                _, ext = file.split('.')
            else:
                ext = ''
            if ext == "usd" :
                ext_image = f"{root_path}/elements/usd_logo"
            elif ext in ["ma","mb"] :
                ext_image = f"{root_path}/elements/maya_logo"
            file_path = os.path.join(path, file)
            last_time = os.path.getmtime(file_path)
            last_time_str = time.strftime('%m/%d %H:%M:%S', time.localtime(last_time))

            data_list.append([ext_image, file, last_time_str, file_path]) 

        return data_list