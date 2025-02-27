from shotgun_api3 import Shotgun 
import os, sys, time

class Shotgrid : # 부모 클래스 (이름 수정 필요) 샷건 인포 한번에 뿌릴라고 만들었습니다. 모든 샷그리드 클래스 상속받아야함.
    def __init__(self, sg_url, script_name, api_key):
        self.sg = Shotgun(sg_url, script_name, api_key)

class UserInfo(Shotgrid) : 
    def __init__(self, sg_url, script_name, api_key):
        super().__init__(sg_url, script_name, api_key)
        
        self.email = ""
        self.name = ""
        self.dept = ""
        self.pos = ""
        
    def is_validate(self, email, name) :
        self.email = email
        self.name = name
        kname_filter = ['sg_korean_name', 'is', self.name]
        #name_filter = ['name', 'is', self.name]
        email_filter = ['email', 'is', self.email]
        self.userinfo = self.sg.find('HumanUser', [kname_filter, email_filter], ["id", "name", "department", "groups"])

        print(self.userinfo)
        
        if not len(self.userinfo) == 0 :
            self.id = self.userinfo[0]['id'] # id 받기
            self.dept = self.userinfo[0]['department']['name'] # DEPT 받기
            self.pos = self.userinfo[0]['groups'][0]['name'] # 포지션 받기 
            self.show_loading()
            return 1

        else :
            print("틀림!")
            self.show_error()
            return 0
        
    # return 해줄 때는 get_userid가 더 맞을거같아서 바꿉니다
    def get_userid(self) :
        return self.id
    
    # asset 파트인지 seq 파트인지 구별을 위해 사용되는 함수
    def get_user_part(self):
        asset_dept = {"model", "lookdev", "rig"}
        seq_dept = {"layout", "anim", "lighting", "comp"}

        if self.dept.lower() in asset_dept :
            return "asset"
        elif self.dept.lower() in seq_dept :
            return "seq"
        else :
            return "unkown"
    def show_loading(self) :
        pass

    def show_error(self) :
        print("에러창 실행")
        self.name = "" # 새 이름 받기
        self.email = "" # 새 이메일 받기
        #self.is_validate(email, name)

    def create_local_path(self) :
        pass

class TaskInfo(Shotgrid) :
    
    def __init__(self, sg_url, script_name, api_key):
        super().__init__(sg_url, script_name, api_key)
        self.task_dict = {}

    def get_user_task(self, user_id):
        #UserInfo에서 갖고온 id를 파라미터로 갖고와 그 아이디에 해당하는 태스크를 딕트 형식으로 저장

        id_filter = {'type': 'HumanUser', 'id': user_id}
        tasks = self.sg.find("Task", [["task_assignees", "is", id_filter]], ["project", "content", "entity", "start_date", "due_date","sg_status_list", "step"])
        
        for task in tasks :

            task_id = task['id']
            self.task_dict[task_id] = {}
            proj_name = task['project']['name']
            task_name = task['content']
            shot_name = task['entity']['name']
            task_type = task['entity']['type']
            start_date = task['start_date']
            due_date = task['due_date']
            status = task['sg_status_list']
            step = task['step']['name']

            self.task_dict[task_id]['proj_name']=proj_name
            self.task_dict[task_id]['content']=task_name
            
            self.task_dict[task_id]['task_type']=task_type
            self.task_dict[task_id]['start_date']=start_date
            self.task_dict[task_id]['due_date']=due_date
            self.task_dict[task_id]['status']=status
            self.task_dict[task_id]['step'] = step
            
            asset_id = task['entity']['id']

            self.branch_asset_seq(task_type, task_id, asset_id, shot_name) # asset seq로 딕트 형식/저장방법 분기

    def branch_asset_seq(self, task_type, task_id, asset_id, shot_name) :

        if task_type == "Shot" :
            seq_contents = self.sg.find("Shot", [["id", "is", asset_id]], ["tasks", "sg_sequence"])
            seq_name = seq_contents[0]['sg_sequence']['name']

            self.task_dict[task_id]['shot_name'] = shot_name
            self.task_dict[task_id]['seq_name'] = seq_name
            self.task_dict[task_id]['shot_id'] = asset_id
        
        elif task_type == "Asset" :
            asset_contents = self.sg.find("Asset", [["id", "is", asset_id]], ["tasks", "sg_asset_type"])
            asset_category_name = asset_contents[0]['sg_asset_type']
            self.task_dict[task_id]['asset_name']=shot_name
            self.task_dict[task_id]['asset_categ'] = asset_category_name

            self.task_dict[task_id]['asset_id'] = asset_id

    def get_task_dict(self) :
        return self.task_dict
    
    def get_prev_task(self, task_id) :
        # 현재 태스크 정보
        current_task = self.task_dict[task_id]
        # something went wrong
        if not current_task:
            return None
        
        # type_name(shot_id/asset_id)이 같은 태스크들 찾기
        related_tasks = []
        type_id = current_task.get("shot_id") or current_task.get("asset_id")

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
        tasks = self.sg.find("Task", filters, fields)

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

    def on_click_task(self, id) : # 특정 태스크의 아이디에 해당하는 내부 정보들을 딕트의 형식으로 리턴
        prev_task_id = self.get_prev_task(id)
        current_task_id = id
        current_dict = {}
        current_dict["id"] = current_task_id
        current_dict["proj_name"] = self.task_dict[current_task_id]['proj_name']
        current_dict["task_type"] = self.task_dict[current_task_id]['task_type'].lower()
        current_dict["category"] = self.task_dict[current_task_id].get('seq_name') or self.task_dict[current_task_id].get('asset_categ').lower()
        current_dict["name"] = self.task_dict[current_task_id].get('shot_name') or self.task_dict[current_task_id].get('asset_name').lower()
        current_dict["step"] = self.task_dict[current_task_id]['step']



        prev_dict = {}
        if prev_task_id :
            fields = ["id", "code", "description", "published_file_type", "entity"]
            filters = [["task", "is", {"type": "Task", "id": prev_task_id}]]  # 원하는 필터를 추가할 수 있음 (예: 특정 프로젝트, 특정 파일 타입 등)

            published_file = self.sg.find_one("PublishedFile", filters, fields)
            comment = published_file.get('description', 'No Description')
            
            prev_task_data = self.sg.find_one("Task", [["id", "is", prev_task_id]], ["project","content", "entity","step", "task_assignees", "sg_status_list"])
            prev_task_proj = prev_task_data['project']['name']

            entity_type = prev_task_data['entity']['type']
            entity_id = prev_task_data['entity']['id']
            if entity_type == "Shot":
                entity_data = self.sg.find_one("Shot", [["id", "is", entity_id]], ["sg_sequence"])
                prev_task_category = entity_data.get("sg_sequence", {}).get("name", "No Sequence")

            elif entity_type == "Asset":
                entity_data = self.sg.find_one("Asset", [["id", "is", entity_id]], ["sg_asset_type"])
                prev_task_category = entity_data.get("sg_asset_type", "No Asset Type")
            
            prev_task_name = prev_task_data['entity'].get('name') or prev_task_data['entity'].get('name')
            prev_task_id = prev_task_data['id']
            prev_task_task_name = prev_task_data['content']
            prev_task_step = prev_task_data['step']['name']
            prev_task_assignees = [assignee['name'] for assignee in prev_task_data['task_assignees']]
            prev_task_status = prev_task_data['sg_status_list']
            prev_task_assignees = ", ".join(prev_task_assignees)

            prev_dict["id"] = prev_task_id
            prev_dict["proj_name"] = prev_task_proj
            prev_dict["type_name"] = entity_type.lower()
            prev_dict["category"] = prev_task_category.lower()
            prev_dict["name"] = prev_task_name            

            prev_dict["task_name"] = prev_task_task_name
            prev_dict["step"] = prev_task_step.lower()
            prev_dict["assignees"] = prev_task_assignees
            prev_dict["status"] = prev_task_status
            prev_dict["comment"] = comment
        else :
            prev_dict["id"] = "None"
            prev_dict["proj_name"] = "None"
            prev_dict["type_name"] = "None"
            prev_dict["category"] = "None"
            prev_dict["name"] = "None"

            prev_dict["task_name"] = "None"
            prev_dict["step"] = "None"
            prev_dict["assignees"] = "None"
            prev_dict["status"] = "None"
            prev_dict["comment"] = "None"
        print(prev_dict)

        return prev_dict, current_dict

    def set_path_items(self,task_id) :
        '''
        task_id와 그 task에 붙은 task_dict를 기반으로 파일패스를 생성해 task와 연결되는 디렉토리 내의 파일을 리스트의 형식으로 담아온다.
        pub과 work로 분기하였으며 파일이름과 함께 생성일과 최근 수정일도 time 라이브러리를 사용해 가져옴 (논의 필요)
        그리고 이거 다른 파일에 붙여야하는데 어디다 붙일지 모르겠어서 일단 팠어요.
        '''  
        root_path = '/nas/eval/show'
        
        task_dict = self.task_dict[task_id]
        project_name = task_dict['proj_name']
        task_type = task_dict['task_type']
        
        if task_type == "Asset"  : 
            asset_categ = task_dict['asset_categ']
            task_step = task_dict['step']
            task_type = "assets"
            asset_name = task_dict['asset_name']
        
            path = f"{root_path}/{project_name}/{task_type}/{asset_categ}/{asset_name}/{task_step}"
            
        else : #seq 일 때
            pass
        
        lower_path =path.lower()
    
        return lower_path
    
    def get_pub_files(self, task_id) :
        path = self.set_path_items(task_id)
        pub_path = f"{path}/pub/maya/scenes"
        print(f"pub path : {pub_path}")
        pub_list = self.set_file_list(pub_path)
        print(f"the list in pub {pub_list}")

        return pub_path, pub_list
        
    def get_work_files(self, task_id) :
        path = self.set_path_items(task_id)
        work_path = f"{path}/work/maya/scenes"
        print(f"work path : {work_path}")
        work_list = self.set_file_list(work_path)
        print(f"the list in work {work_list}")

        return work_path, work_list
        
        ##### 여기서 ext 나눠서 
    def set_file_list(self, path) :
        
        data_list = []
        file.split[-3:0]
        for file in os.listdir(path): # 확장자에 따라서 넣는거 해야함!!!
            
            file_path = os.path.join(path, file)
        
            last_time = os.path.getmtime(file_path) # 최근 수정일 아이거쓰면좋을거같은데 뭔가애매해.
            last_time_str = time.strftime('%m/%d %H:%M:%S', time.localtime(last_time))
            #data_list.append(file)
            #data_list.append(last_time_str)

            data_list.append([file, last_time_str]) 
                
        return data_list

#실행
if __name__ == "__main__":
    sg_url = "https://hi.shotgrid.autodesk.com/"
    script_name = "Admin_SY"
    api_key = "kbuilvikxtf5v^bfrivDgqhxh"

    user = UserInfo(sg_url, script_name, api_key)
    task = TaskInfo(sg_url, script_name, api_key)

    email = "p2xch@naver.com"
    name = "신승연"

    user.is_validate(email, name)
    user_id = user.get_userid()
    print(f"user info : {user.name} | {user.email} | {user.id} | {user.dept} | {user.pos}")
    task.get_user_task(user_id)

    for task_id, value in task.task_dict.items() :
        print(f"task id : {task_id} | task name : {value['content']}")
        task.get_pub_files(task_id)
        task.get_work_files(task_id)