# from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox, QMainWindow

from pxr import Usd, Sdf, Kind
import os
import re
from shotgun_api3 import Shotgun

# 테스크가 할당되었지만 선수작업자가 없어서 본인이 처음 작업일때 사용하는 클래스.
class AssetShotCreator:
    def __init__(self):
        self.root_directory = '/nas/eval/show'

    # 할당된 asset task가 존재할 때, task를 기반으로 local에 directory, dept usd파일을 생성해주는 함수.
    def create_asset_stage(self, project_name, asset_name, asset_type, dept): 
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
            # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
            if status == "work":
                work_directory = status_folder_path

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

# 할당된 shot task가 존재할 때, task를 기반으로 local에 directory, dept usd파일을 생성해주는 함수.
    def create_shot_stage(self, project_name, shot_name, shot_num, dept): 
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
            # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
            if status == "work":
                work_directory = status_folder_path

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
            # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
            if status == "work":
                work_directory = status_folder_path

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
            print("sublayer가 생성되었습니다")

        # 만약 dept가 lookdev이거나 rig라면 기존의 modeling파일을 불러온다.
        if dept in ["lookdev", "rig"]:
            model_pub_path = os.path.join(asset_root_path, "model", "pub", "maya", "scenes")
            if os.path.exists(model_pub_path):
                published_models = []
                for filename in os.listdir(model_pub_path):
                    match = re.search(rf"{asset_name}_model_v(\d{{3}})\.usda", filename)
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
                    # lookdev or rig의 usd에 model 파일을 Reference로 추가
                    department_usd_stage = Usd.Stage.Open(usd_file_path)
                    department_prim = department_usd_stage.GetPrimAtPath(f"/{asset_name}_{dept}")
                    # Prim이 없으면 생성
                    if not department_prim:
                        department_prim = department_usd_stage.DefinePrim(f"/{asset_name}_{dept}", "Xform")
                    department_prim.GetReferences().AddReference(relative_usd_reference_path)
                    department_usd_stage.GetRootLayer().Save()

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
            # 폴더 이름이  "work"라면 work_directory를 따로 지정해준다.
            if status == "work":
                work_directory = status_folder_path

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

        department_usd_stage = Usd.Stage.Open(usd_file_path)

        #만약 dept가 animation일 경우, layout의 usd파일을 레퍼런스로 가져와야 한다.
        if dept == "animation":
            layout_pub_path = os.path.join(shot_root_path, "layout", "pub", "maya", "scenes")
            published_layouts = []
            for filename in os.listdir(layout_pub_path):
                match = re.search(rf"{shot_num}_layout_v(\d{{3}})\.usda", filename)
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

        #만약 dept가 light 경우, animation의 usd파일을 레퍼런스로 가져와야 한다.
        if dept == "light":
            animation_pub_path = os.path.join(shot_root_path, "animation", "pub", "maya", "scenes")
            published_animations = []
            for filename in os.listdir(animation_pub_path):
                match = re.search(rf"{shot_num}_animation_v(\d{{3}})\.usda", filename)
                if match:
                    version_number = int(match.group(1))
                    published_animations.append((version_number,filename))
            if  published_animations:
                last_version = sorted(published_animations, key=lambda x:x[0], reverse=True)[0]
                animation_referenced_usd_filepath = os.path.join(animation_pub_path, last_version[1])
                relative_animation_reference_path = os.path.relpath(animation_referenced_usd_filepath, os.path.dirname(usd_file_path))
                department_prim = department_usd_stage.GetPrimAtPath(f"/{shot_num}_{dept}")
                if not department_prim.IsValid():
                    department_prim = department_usd_stage.DefinePrim(f"/{shot_num}_{dept}", "Xform")
                department_prim.GetReferences().AddReference(relative_animation_reference_path)
                department_usd_stage.GetRootLayer().Save()



#create_task = AssetShotCreator()
# create_task.create_asset_stage("IronMan_4", "IronMan", "character", "model")

#create_task.create_shot_stage("IronMan_4", "OPN", "OPN_0010", "layout")

get_front_task = USDReferenceLoader()
# get_front_task.load_model_reference("IronMan_4", "IronMan", "character", "lookdev")
# get_front_task.load_model_reference("IronMan_4", "IronMan", "character", "rig")
get_front_task.load_shot_reference("IronMan_4", "OPN", "OPN_0010", "light")




#-----------------------------------------------------------------------------------------------
#에셋 루트 만드는거 (추후에 퍼블리셔에서 사용할거)
        # # asset_root_path에 asset_name의 root stage usda파일 생성 
        # create_asset_root_usd = os.path.join(asset_root_path, f"{asset_name}.usda")
        # # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
        # if os.path.exists(create_asset_root_usd):
        #     new_asset_root_stage = Usd.Stage.Open(create_asset_root_usd)
        #     print(f"{asset_name}.usda 가 존재합니다. 기존 파일을 로드하겠습니다.")
        # else:
        #     new_asset_root_stage = Usd.Stage.CreateNew(create_asset_root_usd)

        # # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
        # root_prim = new_asset_root_stage.DefinePrim(f"/{default_prim}", root_prim_type)
        
        # #상대경로로 변환
        # relative_usd_file_path = os.path.relpath(usd_file_path, os.path.dirname(create_asset_root_usd))



        # # Rootstage 에 Payload 로 불러올지 Reference로 불러올지 정하는 변수. (이것도 작업자가 선택할 수 있었으면 좋겠음)
        # if payload:
        #     root_prim.GetPayloads().AddPayload(relative_usd_file_path)
        # else:
        #     root_prim.GetReferences().AddReference(relative_usd_file_path)
        # #Root stage 저장
        # new_asset_root_stage.GetRootLayer().Save()
        # print(f"usd 파일 생성 완료: {create_asset_root_usd}")


        # # root stage에 생성 될 prim의 타입을 선택하는 변수 (콤보박스로 선탁할 수 있게 하면 좋겠음)
        # root_prim_type = input("root stage에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        # #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
        # if root_prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
        #     root_prim_type = "Xform"
        #     print("root prim이 생성되었습니다")


#샷 루트 만드는거 (추후에 퍼블리셔에서 사용할거)
        # # shot_root_path에 asset_name의 root stage usda파일 생성 
        # create_shot_root_usd = os.path.join(shot_root_path, f"{shot_num}.usda")
        # # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
        # if os.path.exists(create_shot_root_usd):
        #     new_shot_root_stage = Usd.Stage.Open(create_shot_root_usd)
        #     print(f"{shot_name}.usda 가 존재합니다. 기존 파일을 로드하겠습니다.")
        # else:
        #     new_shot_root_stage = Usd.Stage.CreateNew(create_shot_root_usd) 



        # # root stage에 생성 될 prim의 타입을 선택하는 변수 (콤보박스로 선탁할 수 있게 하면 좋겠음)
        # root_prim_type = input("root stage에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        # #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
        # if root_prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
        #     root_prim_type = "Xform"
        #     print("root_prim이 생성되었습니다")

        # # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
        # root_prim = new_shot_root_stage.DefinePrim(f"/{default_prim}", root_prim_type)
        
        # #상대경로로 변환
        # relative_usd_file_path = os.path.relpath(usd_file_path, os.path.dirname(create_shot_root_usd))

        # # Rootstage 에 Payload 로 불러올지 Reference로 불러올지 정하기. (이것도 작업자가 선택할 수 있었으면 좋겠음)
        # if payload:
        #     root_prim.GetPayloads().AddPayload(relative_usd_file_path)
        # else:
        #     root_prim.GetReferences().AddReference(relative_usd_file_path)
        # #Root stage 저장
        # new_shot_root_stage.GetRootLayer().Save()
        # print(f"usd 파일 생성 완료: {create_shot_root_usd}")