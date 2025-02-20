from shotgun_api3 import Shotgun 

class ShotgridUserInfo : 
    def __init__(self, server_url, script_name, api_key):
        self.sg = Shotgun(server_url, script_name, api_key)
        
    def is_validate(self, email, name) :
        name_filter = ['name', 'is', name]
        email_filter = ['email', 'is', email]
        self.userinfo = self.sg.find('HumanUser', [name_filter, email_filter], ["id", "name", "department", "groups"])
        
        if not len(self.userinfo) == 0 :
            self.id = self.userinfo[0]['id'] # id 받기
            self.department=self.userinfo[0]['department']['name'] # DEPT 받기
            self.position=self.userinfo[0]['groups'][0]['name'] # 포지션 받기 
            print("*"*30)
            print(f"확인 완료\nname : {name}\nemail : {email}\nid : {self.id}\ndept : {self.department}\nposition : {self.position}")
            print("*"*30)
            self.show_loading()

        else :
            print("틀림!")
            self.show_error()
            
    def show_loading(self) :
        self.get_task()
        pass

    def show_error(self) :
        print("에러창 실행")
        name = "" # 새 이름 받기
        email = "" # 새 이메일 받기
        #self.is_validate(email, name)
        pass

    def get_task(self):
        id_filter = {'type': 'HumanUser', 'id': self.id}
        tasks = self.sg.find("Task", [["task_assignees", "is", id_filter]], ["project", "content", "entity", "start_date", "due_date","sg_status_list"])

        for task in tasks :

            task_id = task['id']
            project_name = task['project']['name']
            content = task['content']
            shot_name = task['entity']['name']
            task_type = task['entity']['type']
            start_date = task['start_date']
            due_date = task['due_date']
            status = task['sg_status_list']
            print(f"task id :{task_id}\nproj name : {project_name}\ncontent : {content}\nshot name : {shot_name}\ntask type : {task_type}\nstart date : {start_date}\ndue date : {due_date}\nstatus : {status}")
            print("*"*30)

    def create_local_path(self) :
    
        pass

        
if __name__ == "__main__":
    sg_url = "https://nashotgrid.shotgrid.autodesk.com"
    script_name = "test"
    api_key = "hetgdrcey?8coevsotrgwTnhv"

    user = ShotgridUserInfo(sg_url, script_name, api_key)

    email = "p2xch@naver.com"
    name = "SEUNGYEON SHIN"
    user.is_validate(email, name)