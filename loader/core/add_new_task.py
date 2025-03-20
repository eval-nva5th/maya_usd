import os
import re
import maya.cmds as cmds
from pxr import Usd
from systempath import SystemPath
import maya.cmds as cmds
root_path = SystemPath().get_root_path()

root_directory = f'{root_path}/show'
usd_type_list = ["usd", "usda", "usdc"]

class UsdLoader : 
    @staticmethod
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
            
    @staticmethod
    def open_new_file(base_path, dept, file_name, ext) :
        maya_path = os.path.join(base_path, dept, "work", "maya","scenes", f"{file_name}{ext}")

        if ext == ".ma" :
            save_type = "mayaAscii"
        elif ext == ".mb" :
            save_type = "mayaBinary"

        try:
            cmds.file(new=True, force=True)
            cmds.file(rename=maya_path)
            cmds.file(save=True, type=save_type)
            cmds.file(maya_path, open=True, force=True)
            print("작업환경이 생성되었습니다.")

        except Exception as e:
            print(f"오류: {e}")

    @staticmethod
    def load_model_reference(base_path, dept, file_name, ext, entity_name):
            open_path = UsdLoader.open_new_file(base_path, dept, file_name, ext)
            """
            첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다. 또한 선수작업을 reference로 불러온다.
            ex) Ironman_lookdev_v001.mb 생성. Ironman_model.usd파일을 reference로 불러온다.
            """

            if dept == "model" :
                pass

            elif dept == "lookdev":
                sourceimages_path = os.path.join(base_path, dept, "work", "maya", "sourceimages")
                os.makedirs(sourceimages_path, exist_ok=True)
                for usd_type in usd_type_list:
                    model_usd_filename = f"{entity_name}_model.{usd_type}"
                    model_reference_path = os.path.join(base_path, "model", "pub", "usd", model_usd_filename)
                    if os.path.exists(model_reference_path):
                        cmds.file(model_reference_path, reference=True, defaultNamespace=True)
                        break

        # rig 작업파일은 추후에 animation 작업자가 layout에서 넘어온 asset데이터들을 rig.ma파일로 변경시켜줘야 하기 때문에,
        # rig에는 lookdev데이터도 포함이 되어있어야 한다.
        # 그래서 rig는 Ironman_model.usd이 아닌, 루트스테이지 즉,Ironman.usd를 reference로 불러와서 작업을 한다.

            elif dept == "rig":
                for usd_type in usd_type_list:
                    root_usd_filename = f"{entity_name}.{usd_type}"
                    root_usd_reference_path = os.path.join(base_path, root_usd_filename)
                    if os.path.exists(root_usd_reference_path):
                        cmds.file(root_usd_reference_path, reference=True, defaultNamespace=True)
                        break

            return open_path

    @staticmethod
    def load_shot_reference(base_path, dept, file_name, ext, entity_name, project_name):
        open_path = UsdLoader.open_new_file(base_path, dept, file_name, ext)

        """
        첫 작업 시, task의 할당된 directory들(작업 환경)을 만들어주고, Open scene해준다. 또한 선수작업을 reference로 불러온다.
        ex) OPN_0010_animation_v001.mb 생성. OPN_0010_layout.usd파일을 reference로 불러온다.
        """

        if dept == "animation":
            for usd_type in usd_type_list:
                usd_reference_path = os.path.join(base_path, "layout", "pub", "usd", f"{entity_name}_layout.{usd_type}")
                if os.path.exists(usd_reference_path):
                    proxy_node = cmds.createNode("mayaUsdProxyShape", name=f"{entity_name}_layout")
                    cmds.setAttr(f"{proxy_node}.filePath", usd_reference_path, type="string")
                    cmds.connectAttr("time1.outTime", f"{proxy_node}.time", force=True)
                    print("일단 켜지긴 불러는 왔음")

                    layout_stage = Usd.Stage.Open(usd_reference_path)
                    layout_prim = layout_stage.GetDefaultPrim()
                    prim_names = []
                    for prim in layout_prim.GetChildren():
                        prim_names.append(prim.GetName())
                    # layout은 rig가 되지 않은 usd파일을 사용했기 때문에, 이름과 동일한 rig.ma파일이 있다면 같이 불러와준다.
                    rig_files_list = []
                    assets_types = ["Character", "Environment", "Prop", "Vehicle"]
                    for asset_type in assets_types:
                        assets_path = os.path.join(root_directory, project_name, "assets", asset_type) 
                        print(f"에셋패스:{assets_path}")
                        for asset_name in prim_names:
                            print(f"에셋네임:{asset_name}")
                            assets_rig_path = os.path.join(assets_path, asset_name, "rig", "pub", "maya", "scenes")
                            if not os.path.exists(assets_rig_path):
                                print("해당 asset에 rig파일이 없습니다.")
                                continue
                            version_nums = []
                            assets_rig_paths = os.listdir(assets_rig_path)
                            for file_name in assets_rig_paths:
                                match = re.search(r"v(\d{3})", file_name)
                                if match:
                                    version_nums.append(int(match.group(1)))

                            last_version = max(version_nums)
                            maya_exr = ["ma", "mb"]
                            if last_version > 0:
                                for ext in maya_exr:
                                    rig_last_file = os.path.join(assets_rig_path, f"{asset_name}_rig_v{last_version:03d}.{ext}")
                                    if os.path.exists(rig_last_file) :
                                        rig_files_list.append(rig_last_file)
                                        break

                    for rig_file in rig_files_list:
                        cmds.file(rig_file, reference=True, defaultNamespace=True) 


        elif dept == "light":
            for usd_type in usd_type_list:
                animation_usd_filename = f"{entity_name}_animation.{usd_type}"
                usd_reference_path = os.path.join(base_path, "animation", "pub", "usd", animation_usd_filename)
                if os.path.exists(usd_reference_path):
                    cmds.file(usd_reference_path, reference=True, defaultNamespace=True)
                    break

        else :
            pass
        
        return open_path

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
