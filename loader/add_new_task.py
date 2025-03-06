import maya.cmds as cmds
import os

def create_asset_path(project_name, asset_name, asset_type, dept): 
    if dept == "model":
        root_directory = '/nas/eval/show'
        asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)
        # asset_name으로 된 파일 생성.
        os.makedirs(asset_root_path, exist_ok=True)
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, "pub", "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        print("작업환경이 생성되었습니다.")
    else:
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")

def create_shot_stage(project_name, shot_name, shot_num, dept): 
    if dept == "layout":
        root_directory = '/nas/eval/show'
        asset_root_path = os.path.join(root_directory, project_name, "seq", shot_name, shot_num)
        # shot_name으로 된 파일 자동생성.
        os.makedirs(asset_root_path, exist_ok=True)
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, "pub", "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        print("작업환경이 생성되었습니다.")
    else:
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")


# asset 선수 작업자가 있다면, 그 usd를 reference로 불러오는 함수. ex)ironman_rig라면 ironman_model.usd 파일을 reference로 불러오기.
def load_model_reference(project_name, asset_name, asset_type, dept):
    # dept가 lookdev 혹은 rig라면 실행되는 함수
    if dept in ["lookdev", "rig"]:
        root_directory = '/nas/eval/show'
        # asset들이 들어있는 경로 패스
        asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)
        # asset_name으로 된 파일 자동생성.
        os.makedirs(asset_root_path, exist_ok=True)
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, status, "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        usd_type_list = ["usd", "usda", "usdc"]
        for usd_type in usd_type_list:
            model_pub_path = os.path.join(asset_root_path, "model", "pub", "usd")
            model_usd_filename = f"{asset_name}_model.{usd_type}"
            usd_reference_path = os.path.join(model_pub_path, model_usd_filename)
        if os.path.exists(usd_reference_path):
            namespace = asset_name + "_model"
            cmds.file(usd_reference_path, reference=True, namespace=namespace)
    else:
        print("해당 dept는 지원하지 않습니다.")

# shot 선수 작업자가 있다면, 그 usd를 reference로 불러오는 함수.
def load_shot_reference(project_name, shot_name, shot_num, dept): 
    root_directory = '/nas/eval/show'
    shot_root_path = os.path.join(root_directory, project_name, "seq", shot_name, shot_num)
    # shot_name으로 된 파일 자동생성.
    os.makedirs(shot_root_path, exist_ok=True)
    # 현재 status의 상태, pub과 work파일을 만들어준다.
    workflows = ["pub", "work"]
    for status in workflows:
        status_folder_path = os.path.join(shot_root_path, dept, status, "maya", "scenes")
        os.makedirs(status_folder_path, exist_ok=True)
        usd_folder_path = os.path.join(shot_root_path, dept, "pub", "usd")
        os.makedirs(usd_folder_path, exist_ok=True)
    usd_type_list = ["usd", "usda", "usdc"]
    if dept == "animation":
        for usd_type in usd_type_list:
            layout_pub_path = os.path.join(shot_root_path, "layout", "pub", "usd")
            layout_usd_filename = f"{shot_num}_layout.{usd_type}"
            usd_reference_path = os.path.join(layout_pub_path, layout_usd_filename)
        # 만약 pub파일에 layout.usd가 있다면 maya 내에 reference로 가져온다.
        if os.path.exists(usd_reference_path):
            namespace = shot_num + "_layout"
            cmds.file(usd_reference_path, reference=True, namespace=namespace)
        else:
            print("layout 선수작업이 존재하지 않습니다.")
    else:
        print("해당 dept는 지원하지 않습니다.")

    #만약 dept가 light 경우, animation의 usd파일을 레퍼런스로 가져와야 한다.
    if dept == "light":
        for usd_type in usd_type_list:
            animation_pub_path = os.path.join(shot_root_path, "animation", "pub", "usd")
            animation_usd_filename = f"{shot_num}_animation.{usd_type}"
            usd_reference_path = os.path.join(animation_pub_path, animation_usd_filename)
        # 만약 pub파일에 animation.usd가 있다면 maya 내에 reference로 가져온다.
        if os.path.exists(usd_reference_path):
            namespace = shot_num + "_animation"
            cmds.file(usd_reference_path, reference=True, namespace=namespace)
        else:
            print("animation 선수작업이 존재하지 않습니다.")
    else:
        print("해당 dept는 지원하지 않습니다.")

# work파일에 작업하던 마야 파일을 불러온다.
# asset 작업자와 seq 작업자가 로드하는 방식이 같기 때문에, 인자를 task_name, task type으로 해놓았다.
def load_work(project_name, task_name, task_type, dept, work_ver):
    root_directory = '/nas/eval/show'
    asset_dept_type_list = ["model", "lookdev", "rig"]
    maya_type_list = ["mb", "ma"]
    if dept in asset_dept_type_list:
        for maya_type in maya_type_list:
            # 여기에 들어가는 task_name은 asset name, task_type은 asset_type이 되어야 한다.
            asset_work_path= os.path.join(root_directory, project_name, "assets", task_name, task_type, dept, "work", "maya", "scenes", f"{task_type}_{dept}_{work_ver}.{maya_type}")

            if os.path.exists(asset_work_path):
                cmds.file(asset_work_path, open=True, force=True)
                return
            else:
                print("maya file이 없습니다.")

    seq_dept_type_list = ["layout", "animation", "light"]
    if dept in seq_dept_type_list:
        for maya_type in maya_type_list:
            # 여기에 들어가는 task_name은 shot__name task_type은 shot_num이 되어야 한다.
            seq_work_path = os.path.join(root_directory, project_name, "seq", task_name, task_type, dept, "work", "maya", "scenes", f"{task_type}_{dept}_{work_ver}.{maya_type}")
            if os.path.exists(seq_work_path):
                cmds.file(seq_work_path, open=True, force=True)
                return
            else:
                print("maya file이 없습니다.")