from shotgun_api3 import Shotgun 

#self.sg 가 부모인 클래스를 만들고
#거기서 저는 유저인포(sg) / 

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
        name_filter = ['name', 'is', name]
        email_filter = ['email', 'is', email]
        self.userinfo = self.sg.find('HumanUser', [name_filter, email_filter], ["id", "name", "department", "groups"])
        
        if not len(self.userinfo) == 0 :
            self.id = self.userinfo[0]['id'] # id 받기
            self.dept = self.userinfo[0]['department']['name'] # DEPT 받기
            self.pos = self.userinfo[0]['groups'][0]['name'] # 포지션 받기 
            # print("*"*30)
            # print(f"확인 완료\nname : {name}\nemail : {email}\nid : {self.id}\ndept : {self.dept}\nposition : {self.pos}")
            # print("*"*30)
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
        tasks = self.sg.find("Task", [["task_assignees", "is", id_filter]], ["project", "content", "entity", "start_date", "due_date","sg_status_list"])

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

            self.task_dict[task_id]['proj_name']=proj_name
            self.task_dict[task_id]['content']=task_name
            self.task_dict[task_id]['shot_name']=shot_name
            self.task_dict[task_id]['task_type']=task_type
            self.task_dict[task_id]['start_date']=start_date
            self.task_dict[task_id]['due_date']=due_date
            self.task_dict[task_id]['status']=status

    def on_click_task(self, id) : # 특정 태스크의 아이디에 해당하는 내부 정보들을 딕트의 형식으로 리턴

        for key, inner_dict in self.task_dict.items() :
            if key == id : 
                return inner_dict
            else :
                pass

#실행
if __name__ == "__main__":
    sg_url = "https://nashotgrid.shotgrid.autodesk.com"
    script_name = "test"
    api_key = "hetgdrcey?8coevsotrgwTnhv"

    user = UserInfo(sg_url, script_name, api_key)
    task = TaskInfo(sg_url, script_name, api_key)

    email = "p2xch@naver.com"
    name = "SEUNGYEON SHIN"

    user.is_validate(email, name)
    user_id = user.get_userid()
    task.get_user_task(user_id)

    print(task.task_dict)

    # task_id = 5853
    # print(task.on_click_task(task_id))

    
    