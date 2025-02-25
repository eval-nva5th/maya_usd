from shotgrid_user_task import *
import os
import time

'''
task_id와 그 task에 붙은 task_dict를 기반으로 파일패스를 생성해 task와 연결되는 디렉토리 내의 파일을 리스트의 형식으로 담아온다.
pub과 work로 분기하였으며 파일이름과 함께 생성일과 최근 수정일도 time 라이브러리를 사용해 가져옴 (논의 필요)
그리고 이거 다른 파일에 붙여야하는데 어디다 붙일지 모르겠어서 일단 팠어요.

'''
def set_path_items(task_id) :
    root_path = '/nas/eval/show'
    
    task_dict = task.task_dict[task_id]
    project_name = task_dict['proj_name']
    task_type = task_dict['task_type']
    
    if task_type == "Asset"  : 
        asset_categ = task_dict['asset_categ']
        task_step = task_dict['step']
        asset_name = task_dict['asset_name']
    
        path = f"{root_path}/{project_name}/{task_type}/{asset_categ}/{asset_name}/{task_step}"
        
    else : #seq 일 때
        pass
    
    lower_path =path.lower()
    
    return lower_path
    
def get_pub_files(task_id) :
    path = set_path_items(task_id)
    pub_path = f"{path}/pub/maya/scenes"
    print(f"pub path : {pub_path}")
    pub_list = set_file_list(pub_path)
    print(f"the list in pub {pub_list}")
    
def get_work_files(task_id) :
    path = set_path_items(task_id)
    work_path = f"{path}/work/maya/scenes"
    print(f"work path : {work_path}")
    work_list = set_file_list(work_path)
    print(f"the list in work {work_list}")
    
def set_file_list(path) :
    
    data_list = []
    
    for file in os.listdir(path): # 확장자에 따라서 넣는거 해야함!!!
        
        file_path = os.path.join(path, file)
    
        initial_time = os.path.getctime(file_path) # 파일 생성일
        last_time = os.path.getmtime(file_path) # 최근 수정일 아이거쓰면좋을거같은데 뭔가애매해.
    
        initial_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(initial_time)) #이것도
        last_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time))
    
        data_list.append([file, initial_time_str, last_time_str]) 
            
    return data_list

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
    
    task_id = 5901
    #get_pub_files(task_id)
    #get_work_files(task_id)