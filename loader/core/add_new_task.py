import maya.cmds as cmds
from pxr import Usd, UsdGeom
import os, re

from DefaultConfig import DefaultConfig

default_config = DefaultConfig()
root_path = default_config.get_root_path()
root_directory = '/Users/junsu/Desktop'
root_directory = f"{root_path}/show"
usd_type_list = ["usd", "usda", "usdc"]

class UsdLoader : 
    
    @staticmethod
    def create_folders(base_path, dept): # shallow path를 의미함.
        """공통적으로 필요한 폴더를 생성하는 함수"""
        folders = [
            os.path.join(base_path, dept, "pub", "maya", "scenes"),
            os.path.join(base_path, dept,  "pub", "usd"),
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
        UsdLoader.open_new_file(base_path, dept, file_name, ext)
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
                    
        # except Exception as e:
        #     print(f"오류: {e}")

    @staticmethod
    def load_shot_reference(base_path, dept, file_name, ext, entity_name, project_name):
        UsdLoader.open_new_file(base_path, dept, file_name, ext)
        
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

                    layout_stage = Usd.Stage.Open(usd_reference_path)
                    layout_prim = layout_stage.GetDefaultPrim()
                    prim_names = []
                    for prim in layout_prim.GetChildren():
                        prim_names.append(prim.GetName())
                    # layout은 rig가 되지 않은 usd파일을 사용했기 때문에, 이름과 동일한 rig.ma파일이 있다면 같이 불러와준다.
                    rig_files_list = []
                    assets_types = ["character", "environment", "prop", "vehicle"]
                    for asset_type in assets_types:
                        assets_path = os.path.join(root_directory, project_name, "assets", asset_type) ####### 어이게뭐지시발좆됏다.
                        for asset_name in prim_names:
                            assets_rig_path = os.path.join(assets_path, asset_name, "rig", "pub", "maya", "scenes")
                            if not os.path.exists(assets_rig_path):
                                continue
                            version_nums = []
                            assets_rig_paths = os.listdir(assets_rig_path)
                            for file_name in assets_rig_paths:
                                match = re.search(r"v(\d{3})", file_name)
                                if match:
                                    version_nums.append(int(match.group(1)))
                    
                            last_version = max(version_nums)

                            if last_version > 0:
                                rig_last_file = os.path.join(assets_rig_path, f"{asset_name}_rig_v{last_version:03d}.ma")
                                rig_files_list.append(rig_last_file)
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
