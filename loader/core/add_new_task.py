import os
import re
import maya.cmds as cmds
from pxr import Usd

root_directory = '/Volumes/TD_VFX/eval/show'
usd_type_list = ["usd", "usda", "usdc"]

def create_folders(base_path, dept):
    """
    공통적으로 필요한 폴더를 생성하는 함수
    """
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
        return
    
    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )

    create_folders(asset_root_path, dept)

    maya_ascii_file = f"{asset_name}_{dept}_v001.ma"
    maya_ascii_path = os.path.join(
        asset_root_path, dept, "work", "maya", "scenes", maya_ascii_file
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
    """layout같이 선수작업자가 없을 시에, 폴더(작업환경)를 생성해주고, 마야파일도 생성시켜준다."""
    if dept != "layout":
        print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")
        return

    shot_root_path = os.path.join(
        root_directory, project_name, "seq", shot_name, shot_num
    )

    create_folders(shot_root_path, dept)

    maya_ascii_file = f"{shot_num}_{dept}_v001.ma"
    maya_ascii_path = os.path.join(
        shot_root_path, dept, "work", "maya", "scenes", maya_ascii_file
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
    첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다. 또한 선수작업을 reference로 불러온다.
    ex) Ironman_lookdev_v001.mb 생성. Ironman_model.usd파일을 reference로 불러온다.
    """

    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )

    create_folders(asset_root_path, dept)

    maya_ascii_file = f"{asset_name}_{dept}_v001.ma"
    maya_ascii_path = os.path.join(
        asset_root_path, dept, "work", "maya", "scenes", maya_ascii_file
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
                    asset_root_path, "model", "pub", "usd", model_usd_filename
                )
                if os.path.exists(model_reference_path):
                    cmds.file(model_reference_path, reference=True, defaultNamespace=True)
                    break

        elif dept == "rig":
        # 애니메이션 작업자가 rig.ma로 작업해야 하므로, lookdev의 데이터가 필요함
        # 따라서 model.usd가 아니라 root_usd를 reference로 불러옴.
            for usd_type in usd_type_list:
                root_usd_file = f"{asset_name}.{usd_type}"
                root_usd_reference_path = os.path.join(asset_root_path, root_usd_file)
                if os.path.exists(root_usd_reference_path):
                    cmds.file(root_usd_reference_path, reference=True, defaultNamespace=True)
                    break
                    
    except Exception as e:
        print(f"오류: {e}")


def load_shot_reference(project_name, shot_name, shot_num, dept): 
    """
    첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다. 또한 선수작업을 reference로 불러온다.
    ex) OPN_0010_animation_v001.mb 생성. OPN_0010_layout.usd파일을 reference로 불러온다.
    """
    shot_root_path = os.path.join(
        root_directory, project_name, "seq", shot_name, shot_num
    )

    create_folders(shot_root_path, dept)
    maya_ascii_file = f"{shot_num}_{dept}_v001.ma"
    maya_ascii_path = os.path.join(
        shot_root_path, dept, "work", "maya", "scenes", maya_ascii_file
    )

    try:
        cmds.file(new=True, force=True)
        cmds.file(rename=maya_ascii_path)
        cmds.file(save=True, type="mayaAscii")
        cmds.file(maya_ascii_path, open=True, force=True)

        if dept == "animation":
            for usd_type in usd_type_list:
                layout_usd_file = f"{shot_num}_layout.{usd_type}"
                layout_usd_path = os.path.join(
                    shot_root_path, "layout", "pub", "usd", layout_usd_file
                )
                if os.path.exists(layout_usd_path):
                    proxy_node = cmds.createNode("mayaUsdProxyShape", name=f"{shot_num}_layout")
                    cmds.setAttr(f"{proxy_node}.filePath", layout_usd_path, type="string")
                    cmds.connectAttr("time1.outTime", f"{proxy_node}.time", force=True)

                    layout_stage = Usd.Stage.Open(layout_usd_path)
                    layout_prim = layout_stage.GetDefaultPrim()

                    prim_names = []
                    for prim in layout_prim.GetChildren():
                        prim_names.append(prim.GetName())

                    # layout은 rig가 되지 않은 usd파일을 사용했기 때문에, 이름과 동일한 rig.ma파일이 있다면 같이 불러와준다.
                    rig_files_list = []
                    assets_types = ["character", "environment", "prop", "vehicle"]
                    for asset_type in assets_types:
                        assets_path = os.path.join(
                            root_directory, project_name, "assets", asset_type
                        )
                        for asset_name in prim_names: 
                            assets_rig_path = os.path.join(
                                assets_path, asset_name, "rig", "pub", "maya", "scenes"
                            )
                            if not os.path.exists(assets_rig_path):
                                continue

                            #리그의 마지막 버전을 가지고 온다.
                            version_nums = []
                            assets_rig_paths = os.listdir(assets_rig_path)
                            for file_name in assets_rig_paths:
                                match = re.search(r"v(\d{3})", file_name)
                                if match:
                                    version_nums.append(int(match.group(1)))

                            last_version = max(version_nums)

                            if last_version > 0:
                                rig_last_file = os.path.join(
                                    assets_rig_path, f"{asset_name}_rig_v{last_version:03d}.ma"
                                )
                                rig_files_list.append(rig_last_file)

                    for rig_file in rig_files_list:
                        cmds.file(rig_file, reference=True, defaultNamespace=True) 

        elif dept == "light":
            for usd_type in usd_type_list:
                animation_usd_file = f"{shot_num}_animation.{usd_type}"
                animation_usd_path = os.path.join(
                    shot_root_path, "animation", "pub", "usd", animation_usd_file
                    )
                if os.path.exists(animation_usd_path):
                    cmds.file(animation_usd_path, reference=True, defaultNamespace=True)
                    break

    except Exception as e:
        print(f"오류: {e}")

def load_work(project_name, task_name, task_type, dept, work_ver):
    """
    작업하던 파일이 있다면 open scene해주는 함수.
    """
    maya_type_list = ["mb", "ma"]

    if dept in ["model", "lookdev", "rig"]:
        work_path= os.path.join(
            root_directory, project_name, "assets", task_name, task_type, dept,
            "work", "maya", "scenes"
            )

    elif dept in ["layout", "animation", "light"]:
        work_path = os.path.join(
            root_directory, project_name, "seq", task_name, task_type, dept,
            "work", "maya", "scenes"
            )

    for maya_type in maya_type_list:
        maya_path = os.path.join(
            work_path, f"{task_type}_{dept}_{work_ver}.{maya_type}"
        )
        if os.path.exists(maya_path):
            cmds.file(maya_path, open=True, force=True)
            print("기존 작업 환경을 불러왔습니다.")
