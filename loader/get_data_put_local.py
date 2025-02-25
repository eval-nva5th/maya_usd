from shotgrid_user_task import *

def get_path_items(dict) :
    dic


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

    task_id = 5852
    