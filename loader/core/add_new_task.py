import maya.cmds as cmds
import os

root_directory = '/nas/eval/show'
usd_type_list = ["usd", "usda", "usdc"]

def create_folders(base_path, dept):
    """공통적으로 필요한 폴더를 생성하는 함수"""
    folders = [
        os.path.join(base_path, dept, "pub", "maya", "scenes"),
        os.path.join(base_path, dept, "pub", "usd"),
        os.path.join(base_path, dept, "work", "maya", "scenes"),
        os.path.join(base_path, dept, "work", "references"),
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def create_model_ma(project_name, asset_name, asset_type, dept): 
    """
    model같이 선수작업자가 없을 시에, 폴더(작업환경)를 생성해주고, 마야파일도 생성시켜준다.
    """
    if dept != "model":
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")

    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )
    create_folders(asset_root_path, dept)

    maya_ascii_path = os.path.join(
        asset_root_path, dept, "work", "maya", "scenes",
        f"{asset_name}_{dept}_v001.ma"
    )

    try:
        cmds.file(new=True, force=True)
        cmds.file(rename=maya_ascii_path)
        cmds.file(save=True, type="mayaAscii")
        cmds.file(maya_ascii_path, open=True, force=True)
        print("작업환경이 생성되었습니다.")
    except Exception as e:
        print(f"오류: {e}")

def create_layout_ma(project_name, shot_name, shot_num, dept): 
    """
    layout같이 선수작업자가 없을 시에, 폴더(작업환경)를 생성해주고, 마야파일도 생성시켜준다.
    """
    if dept != "layout":
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")

    shot_root_path = os.path.join(
        root_directory, project_name, "seq", shot_name, shot_num
    )
    create_folders(shot_root_path, dept)

    maya_ascii_path = os.path.join(
        shot_root_path, dept, "work", "maya", "scenes",
        f"{shot_num}_{dept}_v001.ma"
    )

    try:
        cmds.file(new=True, force=True)
        cmds.file(rename=maya_ascii_path)
        cmds.file(save=True, type="mayaAscii")
        cmds.file(maya_ascii_path, open=True, force=True)
        print("작업환경이 생성되었습니다.")

    except Exception as e:
        print(f"오류: {e}")

def load_model_reference(project_name, asset_name, asset_type, dept):
    """
    첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다.
    또한 선수작업을 reference로 불러온다.
    ex) Ironman_lookdev_v001.mb 생성. Ironman_model.usd파일을 reference로 불러온다.
    """

    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )
    create_folders(asset_root_path, dept)

    maya_ascii_path = os.path.join(
        asset_root_path, dept, "work", "maya", "scenes",
        f"{asset_name}_{dept}_v001.ma"
    )

    try:
        cmds.file(new=True, force=True)
        cmds.file(rename=maya_ascii_path)
        cmds.file(save=True, type="mayaAscii")
        cmds.file(maya_ascii_path, open=True, force=True)

        if dept == "lookdev":
            sourceimages_path = os.path.join(
                asset_root_path, dept, "work", "maya", "sourceimages"
            )
            os.makedirs(sourceimages_path, exist_ok=True)

            for usd_type in usd_type_list:
                model_usd_filename = f"{asset_name}_model.{usd_type}"
                model_reference_path = os.path.join(
                    asset_root_path,"model", "pub", "usd", model_usd_filename
                )
                if os.path.exists(model_reference_path):
                    namespace = asset_name + "_model"
                    cmds.file(model_reference_path, reference=True, namespace=namespace)
                    break

# rig 작업파일은 추후에 animation 작업자가 layout에서 넘어온 asset데이터들을 rig.ma파일로 변경시켜줘야 하기 때문에,
# rig에는 lookdev데이터도 포함이 되어있어야 한다.
# 그래서 rig는 Ironman_model.usd이 아닌, 루트스테이지 즉,Ironman.usd를 reference로 불러와서 작업을 한다.
        elif dept == "rig":
            for usd_type in usd_type_list:
                root_usd_filename = f"{asset_name}.{usd_type}"
                root_usd_reference_path = os.path.join(asset_root_path, root_usd_filename)
                if os.path.exists(root_usd_reference_path):
                    namespace = asset_name
                    cmds.file(root_usd_reference_path, reference=True, namespace=namespace)
                    break
    except Exception as e:
        print(f"오류: {e}")

def load_shot_reference(project_name, shot_name, shot_num, dept): 
    """
    첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다.
    또한 선수작업을 reference로 불러온다.
    ex) OPN_0010_animation_v001.mb 생성. OPN_0010_layout.usd파일을 reference로 불러온다.
    """
    shot_root_path = os.path.join(
        root_directory, project_name, "seq", shot_name, shot_num
    )
    create_folders(shot_root_path, dept)

    maya_ascii_path = os.path.join(
        shot_root_path, dept, "work", "maya", "scenes",
        f"{shot_num}_{dept}_v001.ma"
    )

    try:
        cmds.file(new=True, force=True)
        cmds.file(rename=maya_ascii_path)
        cmds.file(save=True, type="mayaAscii")
        cmds.file(maya_ascii_path, open=True, force=True)

        if dept == "animation":
            for usd_type in usd_type_list:
                layout_usd_filename = f"{shot_num}_layout.{usd_type}"
                usd_reference_path = os.path.join(
                    shot_root_path, "layout", "pub", "usd", layout_usd_filename
                )
                if os.path.exists(usd_reference_path):
                    namespace = shot_num + "_layout"
                    cmds.file(usd_reference_path, reference=True, namespace=namespace)
                    break

        #만약 dept가 light 경우, animation의 usd파일을 레퍼런스로 가져와야 한다.
        elif dept == "light":
            for usd_type in usd_type_list:
                animation_usd_filename = f"{shot_num}_animation.{usd_type}"
                usd_reference_path = os.path.join(
                    shot_root_path, "animation", "pub", "usd", animation_usd_filename
                )
                if os.path.exists(usd_reference_path):
                    namespace = shot_num + "_animation"
                    cmds.file(usd_reference_path, reference=True, namespace=namespace)
                    break
    except Exception as e:
        print(f"오류: {e}")

def load_work(project_name, task_name, task_type, dept, work_ver):
    """
    내가 작업하던 파일이 있다면 open scene해주는 함수.
    """
    maya_type_list = ["mb", "ma"]
    if dept in ["model", "lookdev", "rig"]:
        work_path= os.path.join(
            root_directory, project_name, "assets", task_name,
            task_type, dept, "work", "maya", "scenes"
        )
    
    elif dept in ["layout", "animation", "light"]:
        work_path = os.path.join(
            root_directory, project_name, "seq", task_name,
            task_type, dept, "work", "maya", "scenes"
        )

    for maya_type in maya_type_list:
            maya_file = os.path.join(
                work_path, f"{task_type}_{dept}_{work_ver}.{maya_type}"
            )
            if os.path.exists(maya_file):
                cmds.file(maya_file, open=True, force=True)
                print("기존 작업 환경을 불러왔습니다.")