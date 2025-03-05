from pxr import Usd
import maya.cmds as cmds
import os
import re
# from shotgun_api3 import Shotgun

# 테스크가 할당되었지만 선수작업자가 없어서 본인이 처음 작업일때 사용하는 클래스.
class AssetShotCreator:
    def __init__(self):
        self.root_directory = '/nas/eval/show'

    # 할당된 asset task가 존재할 때, task를 기반으로 local에 directory, dept usd파일을 생성해주는 함수.
    def create_asset_stage(self, project_name, asset_name, asset_type, dept): 
        if dept == "model":
            #혹시나 생길 공백 오류를 예외처리
            asset_name = asset_name.strip()
            # asset들이 들어있는 경로 패스
            asset_root_path = os.path.join(self.root_directory, project_name, "assets", asset_type, asset_name)
            # asset_name으로 된 파일 자동생성.
            os.makedirs(asset_root_path, exist_ok=True)
            # 현재 status의 상태, pub과 work파일을 만들어준다.
            workflows = ["pub", "work"]
            work_directory = None
            for status in workflows:
                status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
                os.makedirs(status_folder_path, exist_ok=True)
                usd_folder_path = os.path.join(asset_root_path, dept, status, "usd")
                os.makedirs(usd_folder_path, exist_ok=True)
                # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
                if status == "work":
                    work_directory = usd_folder_path

            # 해당 dept의 usda 파일을 만들어준다.
            usd_file_name = f"{asset_name}_{dept}_v001.usda"
            # 새로운 작업자이니, work파일 안에 생성.
            usd_file_path = os.path.join(work_directory, usd_file_name)

            # 만약 usd_file_name이 존재하지 않는다면, 생성
            if not os.path.exists(usd_file_path):
                usd_stage = Usd.Stage.CreateNew(usd_file_path)
                # usd file의 prim을 정해준다.
                usd_prim_type = usd_stage.DefinePrim(f"/{asset_name}_{dept}", "Xform")
                usd_stage.SetDefaultPrim(usd_prim_type)
                usd_stage.GetRootLayer().Save()
                print("sublayer가 생성되었습니다")
        else:
            print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")

        usd_nodes = cmds.ls(type="mayaUsdProxyShape")
        if not usd_nodes:
            # mayaUsdProxyShape노드 생성. (model.usd파일을 viewport와 outliner에 띄워주기 위한 수단.)
            proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
        else:
            # 만약 있다면 제일 첫번째 노드에 붙인다.
            proxy_node = usd_nodes[0]

        # USD 파일을 Stage Source로 설정
        cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")

# 할당된 shot task가 존재할 때, task를 기반으로 local에 directory, dept usd파일을 생성해주는 함수.
    def create_shot_stage(self, project_name, shot_name, shot_num, dept): 
        if dept == "layout":
            #혹시나 생길 공백 오류를 예외처리
            shot_name = shot_name.strip()
            # shot들이 들어있는 경로 패스
            shot_root_path = os.path.join(self.root_directory, project_name, "seq", shot_name, shot_num)
            # shot_name으로 된 파일 자동생성.
            os.makedirs(shot_root_path, exist_ok=True)
            # 현재 status의 상태, pub과 work파일을 만들어준다.
            workflows = ["pub", "work"]
            work_directory = None
            for status in workflows:
                status_folder_path = os.path.join(shot_root_path, dept, status, "maya", "scenes")
                os.makedirs(status_folder_path, exist_ok=True)
                usd_folder_path = os.path.join(shot_root_path, dept, status, "usd")
                os.makedirs(usd_folder_path, exist_ok=True)
                # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
                if status == "work":
                    work_directory = usd_folder_path

            # Root stage 안에 넣어줘야할 dept에 해당하는 usda파일 생성
            usd_file_name = f"{shot_num}_{dept}_v001.usda"
            # 새로운 작업자이니, work파일 안에 생성.
            usd_file_path = os.path.join(work_directory, usd_file_name)

            # 만약 usd_file_name이 존재하지 않는다면, 생성
            if not os.path.exists(usd_file_path):
                usd_stage = Usd.Stage.CreateNew(usd_file_path)
                usd_prim_type = usd_stage.DefinePrim(f"/{shot_name}_{dept}","Xform")
                usd_stage.SetDefaultPrim(usd_prim_type)
                usd_stage.GetRootLayer().Save()
                print("sublayer가 생성되었습니다")

        else:
            print("선수작업이 있는 dept 입니다. 생성할 수 없습니다.")

        usd_nodes = cmds.ls(type="mayaUsdProxyShape")
        if not usd_nodes:
            proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
        else:
            proxy_node = usd_nodes[0]
        cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")

class USDReferenceLoader:
    def __init__(self):
        #프로젝트의 루트 패스
        self.root_directory = '/nas/eval/show'

# asset 선수 작업자가 있다면, 그 usd를 reference로 불러오는 함수. ex)ironman_rig라면 ironman_model.usd 파일을 reference로 불러오기.
    def load_model_reference(self, project_name, asset_name, asset_type, dept):
        #혹시나 생길 공백 오류를 예외처리
        asset_name = asset_name.strip()
        # asset들이 들어있는 경로 패스
        asset_root_path = os.path.join(self.root_directory, project_name, "assets", asset_type, asset_name)
        # asset_name으로 된 파일 자동생성.
        os.makedirs(asset_root_path, exist_ok=True)
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        workflows = ["pub", "work"]
        work_directory = None
        for status in workflows:
            status_folder_path = os.path.join(asset_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(asset_root_path, dept, status, "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
            # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
            if status == "work":
                work_directory = usd_folder_path

        exr_list = ["usd", "usda", "usdc"]
        # 해당 dept의 usda 파일을 만들어준다.
        usd_file_name = f"{asset_name}_{dept}_v001.usda"
        # 새로운 작업자이니, work파일 안에 생성.
        usd_file_path = os.path.join(work_directory, usd_file_name)

        # 만약 usd_file_name이 존재하지 않는다면, 생성
        if not os.path.exists(usd_file_path):
            usd_stage = Usd.Stage.CreateNew(usd_file_path)
            # prim을 정해준다.
            usd_prim_type = usd_stage.DefinePrim(f"/{asset_name}_{dept}", "Xform")
            usd_stage.SetDefaultPrim(usd_prim_type)
            usd_stage.GetRootLayer().Save()
            print(f"{usd_file_name}가 생성되었습니다")

        # 만약 dept가 lookdev이거나 rig라면 기존의 modeling파일을 불러온다.
        if dept in ["lookdev", "rig"]:
            model_pub_path = os.path.join(asset_root_path, "model", "pub", "usd")
            if os.path.exists(model_pub_path):
                published_models = []
                for filename in os.listdir(model_pub_path):
                    match = re.search(rf"{asset_name}_model_v(\d{{3}})\.{exr_list}", filename)
                    if match:
                        version_number = int(match.group(1))
                        #만약 있다면, 그 파일순서와 파일 이름을 list에 넣어준다. sorted를 사용하기 위해 튜플로 가두었다.
                        published_models.append((version_number, filename))
                if published_models:
                    # list의 값들을 reverse sorted한다. 그리고 첫번째 값을 가져온다.
                    last_model_version = sorted(published_models, key= lambda x:x[0],reverse=True)[0]
                    # 그리고 람다를 사용해서 1, ~~usd로 되어있기 때문에, 두번째 값을 가져와야한다.
                    usd_reference_path = os.path.join(model_pub_path, last_model_version[1])
                    # 상대경로로 바꾼다.
                    relative_usd_reference_path = os.path.relpath(usd_reference_path, os.path.dirname(usd_file_path))
                    # lookdev or rig의 usd를 열어준다.
                    department_usd_stage = Usd.Stage.Open(usd_file_path)
                    # reference usd파일의 prim type을 그대로 가져온다.
                    department_prim = department_usd_stage.GetPrimAtPath(f"/{asset_name}_{dept}")
                    # 만약 Prim type이 없으면 생성
                    if not department_prim:
                        department_prim = department_usd_stage.DefinePrim(f"/{asset_name}_{dept}", "Xform")
                    department_prim.GetReferences().AddReference(relative_usd_reference_path)
                    department_usd_stage.GetRootLayer().Save()
                    print(f"{department_usd_stage}을 reference로 불러왔으며, {department_prim}로 추가하였습니다.")

                    usd_nodes = cmds.ls(type="mayaUsdProxyShape")
                    if not usd_nodes:
                        proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
                    else:
                        proxy_node = usd_nodes[0]
                    cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")

        else:
            print("해당 dept는 지원하지 않습니다.")

    # shot 선수 작업자가 있다면, 그 usd를 reference로 불러오는 함수.
    def load_shot_reference(self, project_name, shot_name, shot_num, dept): 
        #혹시나 생길 공백 오류를 예외처리
        shot_name = shot_name.strip()
        # shot들이 들어있는 경로 패스
        shot_root_path = os.path.join(self.root_directory, project_name, "seq", shot_name, shot_num)
        # shot_name으로 된 파일 자동생성.
        os.makedirs(shot_root_path, exist_ok=True)
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        workflows = ["pub", "work"]
        work_directory = None
        for status in workflows:
            status_folder_path = os.path.join(shot_root_path, dept, status, "maya", "scenes")
            os.makedirs(status_folder_path, exist_ok=True)
            usd_folder_path = os.path.join(shot_root_path, dept, status, "usd")
            os.makedirs(usd_folder_path, exist_ok=True)
            # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
            if status == "work":
                work_directory = usd_folder_path
        exr_list = ["usd", "usda", "usdc"]
        # 해당 dept의 usda 파일을 만들어준다.
        usd_file_name = f"{shot_num}_{dept}_v001.usda"
        # 새로운 작업자이니, work파일 안에 생성.
        usd_file_path = os.path.join(work_directory, usd_file_name)
        # 만약 usd_file_name이 존재하지 않는다면, 생성
        if not os.path.exists(usd_file_path):
            usd_stage = Usd.Stage.CreateNew(usd_file_path)
            #서브레이어의 prim을 정해준다.
            usd_prim_type = usd_stage.DefinePrim(f"/{shot_num}_{dept}", "Xform")
            # Defaultprim을 설정해준다.
            usd_stage.SetDefaultPrim(usd_prim_type)
            usd_stage.GetRootLayer().Save()
            print(f"{usd_stage}을 생성하였으며, {usd_prim_type}로 추가하였습니다.")

        department_usd_stage = Usd.Stage.Open(usd_file_path)

        #만약 dept가 animation일 경우, layout의 usd파일을 레퍼런스로 가져와야 한다.
        if dept == "animation":
            layout_pub_path = os.path.join(shot_root_path, "layout", "pub", "usd")
            published_layouts = []
            for filename in os.listdir(layout_pub_path):
                match = re.search(rf"{shot_num}_layout_v(\d{{3}})\.{exr_list}", filename)
                if match:
                    version_number = int(match.group(1))
                    published_layouts.append((version_number,filename))

            if  published_layouts:
                last_version = sorted(published_layouts, key=lambda x:x[0], reverse=True)[0]
                layout_referenced_usd_filepath = os.path.join(layout_pub_path, last_version[1])
                relative_layout_reference_path = os.path.relpath(layout_referenced_usd_filepath, os.path.dirname(usd_file_path))
                department_prim = department_usd_stage.GetPrimAtPath(f"/{shot_num}_{dept}")
                if not department_prim.IsValid():
                    department_prim = department_usd_stage.DefinePrim(f"/{shot_num}_{dept}", "Xform")
                department_prim.GetReferences().AddReference(relative_layout_reference_path)
                department_usd_stage.GetRootLayer().Save()
                print(f"{department_usd_stage}을 reference로 불러왔으며, {department_prim}로 추가하였습니다.")

                if not cmds.about(batch=True):
                    usd_nodes = cmds.ls(type="mayaUsdProxyShape")
                    if not usd_nodes:
                        # 없다면 새 노드 생성 (새 USD Stage 생성)
                        proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
                    else:
                        proxy_node = usd_nodes[0]

                    # USD 파일을 Stage Source로 설정
                    cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")
            else:
                print("layout 선수작업이 존재하지 않습니다.")
        else:
            print("해당 dept는 지원하지 않습니다.")

        #만약 dept가 light 경우, animation의 usd파일을 레퍼런스로 가져와야 한다.
        if dept == "light":
            animation_pub_path = os.path.join(shot_root_path, "animation", "pub", "usd")
            published_animations = []
            for filename in os.listdir(animation_pub_path):
                match = re.search(rf"{shot_num}_animation_v(\d{{3}})\.{exr_list}", filename)
                if match:
                    version_number = int(match.group(1))
                    published_animations.append((version_number,filename))
                else:
                    print("animation의 선수작업이 존재하지 않습니다.")
            if  published_animations:
                last_version = sorted(published_animations, key=lambda x:x[0], reverse=True)[0]
                animation_referenced_usd_filepath = os.path.join(animation_pub_path, last_version[1])
                relative_animation_reference_path = os.path.relpath(animation_referenced_usd_filepath, os.path.dirname(usd_file_path))
                department_prim = department_usd_stage.GetPrimAtPath(f"/{shot_num}_{dept}")
                if not department_prim.IsValid():
                    department_prim = department_usd_stage.DefinePrim(f"/{shot_num}_{dept}", "Xform")
                department_prim.GetReferences().AddReference(relative_animation_reference_path)
                department_usd_stage.GetRootLayer().Save()
                print(f"{department_usd_stage}을 reference로 불러왔으며, {department_prim}로 추가하였습니다.")
                if not cmds.about(batch=True):
                    usd_nodes = cmds.ls(type="mayaUsdProxyShape")
                    if not usd_nodes:
                        proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
                    else:
                        proxy_node = usd_nodes[0]
                    cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")
        else:
            print("해당 dept는 지원하지 않습니다.")

class LoadWork:
    def __init__(self):
        #프로젝트의 루트 패스
        self.root_directory = '/nas/eval/show'

    def load_work(self, project_name, asset_name, asset_type, dept, work_ver):
        work_path = os.path.join(self.root_directory, project_name, "assets", asset_type, asset_name, dept, "work", "maya", "scenes", f"{work_ver}.mb")
        usd_folder_path = os.path.join(self.root_directory, project_name, "assets", asset_type, asset_name, dept, "work", "usd", f"{work_ver}.usda")
        
        if cmds.file(work_path, query=True, exists=True):
            cmds.file(work_path, open=True, force=True)
            if not cmds.about(batch=True):
                usd_nodes = cmds.ls(type="mayaUsdProxyShape")
                if not usd_nodes:
                    proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
                else:
                    proxy_node = usd_nodes[0]
                cmds.setAttr(f"{proxy_node}.filePath", usd_folder_path, type="string")
        else:
            print("maya file이 없습니다.")