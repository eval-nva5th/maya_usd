import os
import maya.cmds as cmds
from pxr import Usd

def first_model_publish(project_name, asset_type, asset_name, dept):
    if dept == "model":
        # asset_root_path에 asset_name의 root stage usda파일 생성 
        root_directory = '/nas/eval/show'
        asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)
        create_asset_root_usd = os.path.join(asset_root_path, f"{asset_name}.usda")
        # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
        if os.path.exists(create_asset_root_usd):
            new_asset_root_stage = Usd.Stage.Open(create_asset_root_usd)
            print(f"{asset_name}.usda 가 존재합니다.")
        else:
            new_asset_root_stage = Usd.Stage.CreateNew(create_asset_root_usd)
        # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
        root_prim = new_asset_root_stage.DefinePrim(f"/{asset_name}", "Xform")
        new_asset_root_stage.SetDefaultPrim(root_prim)
        #Root stage 저장
        new_asset_root_stage.GetRootLayer().Save() 
        print(f"usd 파일 생성 완료: {create_asset_root_usd}")
        work_path = os.path.join(asset_root_path, "pub", "maya", "scenes")
        maya_ascii_path = os.path.join(work_path, f"{asset_name}_v001.ma")
        cmds.file(rename=maya_ascii_path)  # 파일명을 설정
        cmds.file(save=True, type="mayaAscii")  # ASCII (.ma) 파일로 저장
        cmds.file("/path/to/save_file.mb", save=True, type="mayaBinary")  # Binary (.mb) 파일로 저장
    else:
        print("해당 dept는 사용할 수 없습니다.")

first_model_publish("IronMan_4", "character", "IronMan", "model")

# #샷 루트 만드는거 (추후에 퍼블리셔에서 사용할거)
#     # shot_root_path에 asset_name의 root stage usda파일 생성 
#     create_shot_root_usd = os.path.join(shot_root_path, f"{shot_num}.usda")
#     # 기존 프로젝트 파일이 존재하면 로드, 없으면 새로 생성
#     if os.path.exists(create_shot_root_usd):
#         new_shot_root_stage = Usd.Stage.Open(create_shot_root_usd)
#         print(f"{shot_name}.usda 가 존재합니다. 기존 파일을 로드하겠습니다.")
#     else:
#         new_shot_root_stage = Usd.Stage.CreateNew(create_shot_root_usd) 



#     # root stage에 생성 될 prim의 타입을 선택하는 변수 (콤보박스로 선탁할 수 있게 하면 좋겠음)
#     root_prim_type = input("root stage에 생성 될 타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
#     #기본 값을 Xform으로 생성 후, 잘못된 선택을 했을 시에, 기본 값인 Xform으로 자동으로 선택
#     if root_prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
#         root_prim_type = "Xform"
#         print("root_prim이 생성되었습니다")

#     # 선택한 prim으로  Root stage에 생성이 됨. ex) def Xform "ironman"
#     root_prim = new_shot_root_stage.DefinePrim(f"/{default_prim}", root_prim_type)
    
#     #상대경로로 변환
#     relative_usd_file_path = os.path.relpath(usd_file_path, os.path.dirname(create_shot_root_usd))

#     # Rootstage 에 Payload 로 불러올지 Reference로 불러올지 정하기. (이것도 작업자가 선택할 수 있었으면 좋겠음)
#     if payload:
#         root_prim.GetPayloads().AddPayload(relative_usd_file_path)
#     else:
#         root_prim.GetReferences().AddReference(relative_usd_file_path)
#     #Root stage 저장
#     new_shot_root_stage.GetRootLayer().Save()
#     print(f"usd 파일 생성 완료: {create_shot_root_usd}")




# load_model_reference("Project_205","Hyung", "character", "lookdev")
# create_asset_path("snowman_3","snowman", "character", "model")

            # # 해당 dept의 usda 파일을 만들어준다.
            # usd_file_name = f"{asset_name}_{dept}_v001.usda"
            # # 새로운 작업자이니, work파일 안에 생성.
            # usd_file_path = os.path.join(work_directory, usd_file_name)

            # # 만약 usd_file_name이 존재하지 않는다면, 생성
            # if not os.path.exists(usd_file_path):
            #     usd_stage = Usd.Stage.CreateNew(usd_file_path)
            #     # usd file의 prim을 정해준다.
            #     usd_prim_type = usd_stage.DefinePrim(f"/{asset_name}_{dept}", "Xform")
            #     usd_stage.SetDefaultPrim(usd_prim_type)
            #     usd_stage.GetRootLayer().Save()
            #     print("sublayer가 생성되었습니다")


        # usd_nodes = cmds.ls(type="mayaUsdProxyShape")
        # if not usd_nodes:
        #     # mayaUsdProxyShape노드 생성. (model.usd파일을 viewport와 outliner에 띄워주기 위한 수단.)
        #     proxy_node = cmds.createNode("mayaUsdProxyShape", name="usdProxy")
        # else:
        #     # 만약 있다면 제일 첫번째 노드에 붙인다.
        #     proxy_node = usd_nodes[0]

        # # USD 파일을 Stage Source로 설정
        # cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")