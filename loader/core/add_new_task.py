import maya.cmds as cmds
import os

def create_asset_path(project_name, asset_name, asset_type, dept): 
    """
    model같이 선수작업자가 없을 시에, 폴더(작업환경)를 생성해주고, 마야파일도 생성시켜준다.
    """
    if dept == "model":
        root_directory = '/nas/eval/show'
        asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)
        os.makedirs(asset_root_path, exist_ok=True)
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, "pub", "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        work_path = os.path.join(asset_root_path, dept, "work", "maya", "scenes")
        maya_binary_path = os.path.join(work_path, f"{asset_name}_{dept}_v001.mb")

        cmds.file(new=True, force=True)
        cmds.file(rename=maya_binary_path)
        cmds.file(save=True, type="mayaBinary")

        if os.path.exists(maya_binary_path):
            cmds.file(maya_binary_path, open=True, force=True)
        print("작업환경이 생성되었습니다.")
    else:
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")

def create_shot_stage(project_name, shot_name, shot_num, dept): 
    """
    layout같이 선수작업자가 없을 시에, 폴더(작업환경)를 생성해주고, 마야파일도 생성시켜준다.
    """
    if dept == "layout":
        root_directory = '/nas/eval/show'
        shot_root_path = os.path.join(root_directory, project_name, "seq", shot_name, shot_num)
        os.makedirs(shot_root_path, exist_ok=True)
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(shot_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(shot_root_path, dept, "pub", "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        work_path = os.path.join(shot_root_path, dept, "work", "maya", "scenes")
        maya_binary_path = os.path.join(work_path, f"{shot_num}_{dept}_v001.mb")

        cmds.file(new=True, force=True)
        cmds.file(rename=maya_binary_path)
        cmds.file(save=True, type="mayaBinary")

        if os.path.exists(maya_binary_path):
            cmds.file(maya_binary_path, open=True, force=True)
        print("작업환경이 생성되었습니다.")
    else:
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")


def load_model_reference(project_name, asset_name, asset_type, dept):
    """
    첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다.
    또한 선수작업을 reference로 불러온다.
    ex) Ironman_lookdev_v001.mb 생성. Ironman_model.usd파일을 reference로 불러온다.
    하지만 rig 작업파일은 추후에 animation 작업자가 layout에서 넘어온 asset데이터들을 rig파일로 변경시켜줘야 하기 때문에,
    rig에는 lookdev데이터도 포함이 되어있어야 한다.
    그래서 rig는 Ironman_model.usd이 아닌, 루트스테이지 즉,Ironman.usd를 reference로 불러와서 작업을 한다.
    """
    root_directory = '/nas/eval/show'
    asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)
    if dept == "lookdev":
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, "pub", "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        work_path = os.path.join(asset_root_path, dept, "work", "maya", "scenes")
        maya_binary_path = os.path.join(work_path, f"{asset_name}_{dept}_v001.mb")

        cmds.file(new=True, force=True)
        cmds.file(rename=maya_binary_path)
        cmds.file(save=True, type="mayaBinary")

        if os.path.exists(maya_binary_path):
            cmds.file(maya_binary_path, open=True, force=True)

        usd_type_list = ["usd", "usda", "usdc"]
        for usd_type in usd_type_list:
            model_pub_path = os.path.join(asset_root_path, "model", "pub", "usd")
            model_usd_filename = f"{asset_name}_model.{usd_type}"
            usd_reference_path = os.path.join(model_pub_path, model_usd_filename)
            if os.path.exists(usd_reference_path):
                namespace = asset_name + "_model"
                cmds.file(usd_reference_path, reference=True, namespace=namespace)

    elif dept == "rig":
        workflows = ["pub", "work"]
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, "pub", "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
        work_path = os.path.join(asset_root_path, dept, "work", "maya", "scenes")
        maya_binary_path = os.path.join(work_path, f"{asset_name}_{dept}_v001.mb")

        cmds.file(new=True, force=True)
        cmds.file(rename=maya_binary_path)
        cmds.file(save=True, type="mayaBinary")

        if os.path.exists(maya_binary_path):
            cmds.file(maya_binary_path, open=True, force=True)
        usd_type_list = ["usd", "usda", "usdc"]
        for usd_type in usd_type_list:
            asset_root_usd_filename = f"{asset_name}.{usd_type}"
            root_reference_path = os.path.join(asset_root_path, asset_root_usd_filename)
            if os.path.exists(root_reference_path):
                namespace = asset_name
                cmds.file(root_reference_path, reference=True, namespace=namespace)
        else:
            print("rootstage가 존재하지 않습니다.")
    else:
        print("해당 dept는 지원하지 않습니다.")

def load_shot_reference(project_name, shot_name, shot_num, dept): 
    """
    첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다.
    또한 선수작업을 reference로 불러온다.
    ex) OPN_0010_animation_v001.mb 생성. OPN_0010_layout.usd파일을 reference로 불러온다.
    """
    root_directory = '/nas/eval/show'
    shot_root_path = os.path.join(root_directory, project_name, "seq", shot_name, shot_num)
    # shot_name으로 된 파일 자동생성.
    os.makedirs(shot_root_path, exist_ok=True)
    workflows = ["pub", "work"]
    for status in workflows:
        status_folder_path = os.path.join(shot_root_path, dept, status, "maya", "scenes")
        os.makedirs(status_folder_path, exist_ok=True)
        usd_folder_path = os.path.join(shot_root_path, dept, "pub", "usd")
        os.makedirs(usd_folder_path, exist_ok=True)
        work_path = os.path.join(shot_root_path, dept, "work", "maya", "scenes")
        maya_binary_path = os.path.join(work_path, f"{shot_num}_{dept}_v001.mb")

        cmds.file(new=True, force=True)
        cmds.file(rename=maya_binary_path)
        cmds.file(save=True, type="mayaBinary")

        if os.path.exists(maya_binary_path):
            cmds.file(maya_binary_path, open=True, force=True)
    usd_type_list = ["usd", "usda", "usdc"]
    if dept == "animation":
        for usd_type in usd_type_list:
            layout_pub_path = os.path.join(shot_root_path, "layout", "pub", "usd")
            layout_usd_filename = f"{shot_num}_layout.{usd_type}"
            usd_reference_path = os.path.join(layout_pub_path, layout_usd_filename)
        if os.path.exists(usd_reference_path):
            namespace = shot_num + "_layout"
            cmds.file(usd_reference_path, reference=True, namespace=namespace)
        else:
            print("layout 선수작업이 존재하지 않습니다.")

    elif dept == "light":
        for usd_type in usd_type_list:
            animation_pub_path = os.path.join(shot_root_path, "animation", "pub", "usd")
            animation_usd_filename = f"{shot_num}_animation.{usd_type}"
            usd_reference_path = os.path.join(animation_pub_path, animation_usd_filename)
        if os.path.exists(usd_reference_path):
            namespace = shot_num + "_animation"
            cmds.file(usd_reference_path, reference=True, namespace=namespace)
        else:
            print("animation 선수작업이 존재하지 않습니다.")
    else:
        print("해당 dept는 지원하지 않습니다.")


def load_work(project_name, task_name, task_type, dept, work_ver):
    """
    내가 작업하던 파일이 있다면 Open scene해주는 함수.
    """

    root_directory = '/nas/eval/show'
    asset_dept_type_list = ["model", "lookdev", "rig"]
    maya_type_list = ["mb", "ma"]
    if dept in asset_dept_type_list:
        for maya_type in maya_type_list:
            asset_work_path= os.path.join(root_directory, project_name, "assets", task_name, task_type, dept, "work", "maya", "scenes", f"{task_type}_{dept}_{work_ver}.{maya_type}")
            if os.path.exists(asset_work_path):
                cmds.file(asset_work_path, open=True, force=True)
                return
            else:
                print("maya file이 없습니다.")

    seq_dept_type_list = ["layout", "animation", "light"]
    if dept in seq_dept_type_list:
        for maya_type in maya_type_list:
            seq_work_path = os.path.join(root_directory, project_name, "seq", task_name, task_type, dept, "work", "maya", "scenes", f"{task_type}_{dept}_{work_ver}.{maya_type}")
            if os.path.exists(seq_work_path):
                cmds.file(seq_work_path, open=True, force=True)
                return
            else:
                print("maya file이 없습니다.")