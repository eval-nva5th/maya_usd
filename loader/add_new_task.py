# from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox, QMainWindow

from pxr import Usd, Sdf, Kind
import os
from shotgun_api3 import Shotgun

class Create_task:
    def __init__(self):
        self.local_path = '/nas/eval/show'

    # 할당된 asset task가 존재할 때, task를 기반으로 local에 directory, root usd, dept usd파일을 생성해주는 함수.
    def create_asset_root_stage(self, project_name, asset_name, asset_type, dept, payload=False): 
        #혹시나 생길 공백 오류를 예외처리
        asset_name = asset_name.strip()
        # asset들이 들어있는 경로 패스
        self.assets_path = os.path.join(self.local_path, project_name, "assets", asset_type, asset_name)
        # asset_name으로 된 파일 자동생성.
        os.makedirs(self.assets_path, exist_ok=True)
        # self.assets_path에 asset_name의 root stage usda파일 생성 
        create_asset_root_usd = os.path.join(self.assets_path, f"{asset_name}.usda")
        # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
        if os.path.exists(create_asset_root_usd):
            new_asset_root_stage = Usd.Stage.Open(create_asset_root_usd)
            print(f"{asset_name}.usda 가 존재합니다. 기존 파일을 로드하겠습니다.")
        else:
            new_asset_root_stage = Usd.Stage.CreateNew(create_asset_root_usd)
        
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        statuses = ["pub", "work"]
        work_path = None
        for status in statuses:
            status_path = os.path.join(self.assets_path, dept, status, "maya", "scenes")
            os.makedirs(status_path, exist_ok=True)
            # 폴더 이름이  "work"라면 work_path를 따로 지정해준다.
            if status == "work":
                work_path = status_path

        # defaultPrim을 설정해주기
        defaultPrim = f"{asset_name}_{dept}"
        
        # Root stage 안에 넣어줘야할 dept에 해당하는 usda파일 생성
        sublayer_usd_file = f"{asset_name}_{dept}_v001.usda"
        # 새로운 작업자이니, work파일 안에 생성.
        sublayer_usd_path = os.path.join(work_path, sublayer_usd_file)

        # 만약 sublayer_usd_file이 존재하지 않는다면, 생성
        if not os.path.exists(sublayer_usd_path):
            sublayer_stage = Usd.Stage.CreateNew(sublayer_usd_path)
            sublayer_prim = input("sublayer에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
            if sublayer_prim not in ["Xform", "Scope", "Mesh", "Material"]:
                sublayer_prim = "Xform"
            sublayer_prim = sublayer_stage.DefinePrim(f"/{defaultPrim}", sublayer_prim)
            sublayer_stage.SetDefaultPrim(sublayer_prim)
            sublayer_stage.GetRootLayer().Save()
            print("sublayer가 생성되었습니다")

        # root stage에 생성 될 prim의 타입을 선택하는 변수 (콤보박스로 선탁할 수 있게 하면 좋겠음)
        root_prim_type = input("root stage에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
        if root_prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
            root_prim_type = "Xform"
            print("root prim이 생성되었습니다")

        # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
        root_prim = new_asset_root_stage.DefinePrim(f"/{defaultPrim}", root_prim_type)
        
        #상대경로로 변환
        relative_sublayer_usd_path = os.path.relpath(sublayer_usd_path, os.path.dirname(create_asset_root_usd))

        # Rootstage 에 Payload 로 불러올지 Reference로 불러올지 정하는 변수. (이것도 작업자가 선택할 수 있었으면 좋겠음)
        if payload:
            root_prim.GetPayloads().AddPayload(relative_sublayer_usd_path)
        else:
            root_prim.GetReferences().AddReference(relative_sublayer_usd_path)
        #Root stage 저장
        new_asset_root_stage.GetRootLayer().Save()
        print(f"usd 파일 생성 완료: {create_asset_root_usd}")

    # 할당된 shot task가 존재할 때, task를 기반으로 local에 directory, root usd, dept usd파일을 생성해주는 함수.
    def create_shot_root_stage(self, project_name, shot_name, shot_num, dept, payload=False): 
        #혹시나 생길 공백 오류를 예외처리
        shot_name = shot_name.strip()
        # shot들이 들어있는 경로 패스
        self.shot_path = os.path.join(self.local_path, project_name, "seq", shot_name, shot_num)
        # shot_name으로 된 파일 자동생성.
        os.makedirs(self.shot_path, exist_ok=True)
        # self.shot_path에 asset_name의 root stage usda파일 생성 
        create_shot_root_usd = os.path.join(self.shot_path, f"{shot_num}.usda")
        # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
        if os.path.exists(create_shot_root_usd):
            new_shot_root_stage = Usd.Stage.Open(create_shot_root_usd)
            print(f"{shot_name}.usda 가 존재합니다. 기존 파일을 로드하겠습니다.")
        else:
            new_shot_root_stage = Usd.Stage.CreateNew(create_shot_root_usd) 
        
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        statuses = ["pub", "work"]
        work_path = None
        for status in statuses:
            status_path = os.path.join(self.shot_path, dept, status, "maya", "scenes")
            os.makedirs(status_path, exist_ok=True)
            # 폴더 이름이  "work"라면 work_path를 따로 지정해준다.
            if status == "work":
                work_path = status_path

        # defaultPrim을 설정해주기
        defaultPrim = f"{shot_num}_{dept}"
        
        # Root stage 안에 넣어줘야할 dept에 해당하는 usda파일 생성
        sublayer_usd_file = f"{shot_num}_{dept}_v001.usda"
        # 새로운 작업자이니, work파일 안에 생성.
        sublayer_usd_path = os.path.join(work_path, sublayer_usd_file)

        # 만약 sublayer_usd_file이 존재하지 않는다면, 생성
        if not os.path.exists(sublayer_usd_path):
            sublayer_stage = Usd.Stage.CreateNew(sublayer_usd_path)
            sublayer_prim = input("sublayer에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
            if sublayer_prim not in ["Xform", "Scope", "Mesh", "Material"]:
                sublayer_prim = "Xform"
            sublayer_prim = sublayer_stage.DefinePrim(f"/{defaultPrim}", sublayer_prim)
            sublayer_stage.SetDefaultPrim(sublayer_prim)
            sublayer_stage.GetRootLayer().Save()
            print("sublayer가 생성되었습니다")

        # root stage에 생성 될 prim의 타입을 선택하는 변수 (콤보박스로 선탁할 수 있게 하면 좋겠음)
        root_prim_type = input("root stage에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
        if root_prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
            root_prim_type = "Xform"
            print("root_prim이 생성되었습니다")

        # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
        root_prim = new_shot_root_stage.DefinePrim(f"/{defaultPrim}", root_prim_type)
        
        #상대경로로 변환
        relative_sublayer_usd_path = os.path.relpath(sublayer_usd_path, os.path.dirname(create_shot_root_usd))

        # Rootstage 에 Payload 로 불러올지 Reference로 불러올지 정하기. (이것도 작업자가 선택할 수 있었으면 좋겠음)
        if payload:
            root_prim.GetPayloads().AddPayload(relative_sublayer_usd_path)
        else:
            root_prim.GetReferences().AddReference(relative_sublayer_usd_path)
        #Root stage 저장
        new_shot_root_stage.GetRootLayer().Save()
        print(f"usd 파일 생성 완료: {create_shot_root_usd}")

class Get_front_task:
    def __init__(self):
        #프로젝트의 루트 패스
        self.local_path = '/nas/eval/show'

    def create_dept_usd(self, project_name, asset_name, asset_type, dept, payload=False): 
        #혹시나 생길 공백 오류를 예외처리
        asset_name = asset_name.strip()
        # asset들이 들어있는 경로 패스
        self.assets_path = os.path.join(self.local_path, project_name, "assets", asset_type, asset_name)
        # asset_name으로 된 파일 자동생성.
        os.makedirs(self.assets_path, exist_ok=True)
        # self.assets_path에 asset_name의 root stage usda파일 생성 
        create_asset_root_usd = os.path.join(self.assets_path, f"{asset_name}.usda")
        # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
        if os.path.exists(create_asset_root_usd):
            new_asset_root_stage = Usd.Stage.Open(create_asset_root_usd)
            print(f"{asset_name}.usda 가 존재합니다. 기존 파일을 로드하겠습니다.")
        else:
            new_asset_root_stage = Usd.Stage.CreateNew(create_asset_root_usd)
        
        # 현재 status의 상태, pub과 work파일을 만들어준다.
        statuses = ["pub", "work"]
        work_path = None
        for status in statuses:
            status_path = os.path.join(self.assets_path, dept, status, "maya", "scenes")
            os.makedirs(status_path, exist_ok=True)
            # 폴더 이름이  "work"라면 work_path를 따로 지정해준다.
            if status == "work":
                work_path = status_path

        # defaultPrim을 설정해주기
        defaultPrim = f"{asset_name}_{dept}"
        
        # Root stage 안에 넣어줘야할 dept에 해당하는 usda파일 생성
        sublayer_usd_file = f"{asset_name}_{dept}_v001.usda"
        # 새로운 작업자이니, work파일 안에 생성.
        sublayer_usd_path = os.path.join(work_path, sublayer_usd_file)

        # 만약 sublayer_usd_file이 존재하지 않는다면, 생성
        if not os.path.exists(sublayer_usd_path):
            sublayer_stage = Usd.Stage.CreateNew(sublayer_usd_path)
            sublayer_prim = input("sublayer에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
            if sublayer_prim not in ["Xform", "Scope", "Mesh", "Material"]:
                sublayer_prim = "Xform"
            sublayer_prim = sublayer_stage.DefinePrim(f"/{defaultPrim}", sublayer_prim)
            sublayer_stage.SetDefaultPrim(sublayer_prim)
            sublayer_stage.GetRootLayer().Save()
            print("sublayer가 생성되었습니다")

        # root stage에 생성 될 prim의 타입을 선택하는 변수 (콤보박스로 선탁할 수 있게 하면 좋겠음)
        root_prim_type = input("root stage에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
        if root_prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
            root_prim_type = "Xform"
            print("root prim이 생성되었습니다")

        # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
        root_prim = new_asset_root_stage.DefinePrim(f"/{defaultPrim}", root_prim_type)
        
        #상대경로로 변환
        relative_sublayer_usd_path = os.path.relpath(sublayer_usd_path, os.path.dirname(create_asset_root_usd))

        # Rootstage 에 Payload 로 불러올지 Reference로 불러올지 정하는 변수. (이것도 작업자가 선택할 수 있었으면 좋겠음)
        if payload:
            root_prim.GetPayloads().AddPayload(relative_sublayer_usd_path)
        else:
            root_prim.GetReferences().AddReference(relative_sublayer_usd_path)

        # 만약 dept가 lookdev이거나 rig라면 기존의 modeling파일을 불러온다.
        if dept in ["lookdev", "rig"]:
            model_usd_file = f"{asset_name}_model_v001.usda"
            model_usd_path = os.path.join(self.assets_path, "model", "pub", "maya", "scenes", model_usd_file)

            if os.path.exists(model_usd_path):
                relative_model_usd_path = os.path.relpath(model_usd_path, os.path.dirname(sublayer_usd_path))
                # Lookdev 또는 Rig의 USD에 Model 파일을 Reference로 추가
                dept_stage = Usd.Stage.Open(sublayer_usd_path)
                dept_prim = dept_stage.DefinePrim(f"/{defaultPrim}", "Xform")
                dept_prim.GetReferences().AddReference(relative_model_usd_path)
                dept_stage.GetRootLayer().Save()
        #Root stage 저장
        new_asset_root_stage.GetRootLayer().Save()
        print(f"usd 파일 생성 완료: {create_asset_root_usd}")


# create_task = Create_task()
# create_task.create_asset_root_stage("IronMan_4", "IronMan", "character", "model", payload=False)
# create_task.create_asset_root_stage("IronMan_4", "IronMan", "character", "lookdev", payload=False)
# create_task.create_shot_root_stage("IronMan_4", "OPN", "OPN_0010", "layout", payload=False)

get_front_task = Get_front_task()
get_front_task.create_dept_usd("IronMan_4", "IronMan", "character", "rig", payload=False)
