import json
import os
import re
import shutil
import maya.cmds as cmds
from pxr import Usd, UsdShade
from publish_usd import LookdevExportUSD

root_directory = '/Volumes/TD_VFX/eval/show'

def lookdev_publish(project_name, asset_name, asset_type, dept):
    """lookdev publish 실행 함수"""

    # 룩뎁이 아니라면 함수 종료
    if dept != "lookdev":
        print("해당 dept는 사용할 수 없습니다.")
        return

    # 파일 경로 설정
    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )
    lookdev_pub_dir = os.path.join(
        asset_root_path, dept, "pub", "usd"
    )
    lookdev_pub_path = os.path.join(
        lookdev_pub_dir, f"{asset_name}_{dept}.usda"
    )
    root_usd_path = os.path.join(
        asset_root_path, f"{asset_name}.usda"
    )
    relative_lookdev_pub_path= os.path.relpath(
        lookdev_pub_path, os.path.dirname(root_usd_path)
    )

    # Maya USD플러그인이 없다면 실행
    if os.path.exists(lookdev_pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

        exporter = LookdevExportUSD(lookdev_pub_path, asset_name, dept)
        exporter.export()

    # 루트 스테이지 실행 (없다면 생성)
    asset_stage = (
        Usd.Stage.Open(root_usd_path)
        if os.path.exists(root_usd_path)
        else Usd.Stage.CreateNew(root_usd_path)
    )

    # lookdev.usd를 reference로 추가.
    sub_prim_path = f"/{asset_name}/{asset_name}_{dept}"
    is_sub_prim = asset_stage.GetPrimAtPath(sub_prim_path)

    if not is_sub_prim:
        is_sub_prim = asset_stage.DefinePrim(sub_prim_path, "scope")
        is_sub_prim.GetReferences().AddReference(relative_lookdev_pub_path)

    # mesh와 material을 연결
    binding_material(lookdev_pub_dir, asset_name, root_usd_path)
    asset_stage.GetRootLayer().Save()

    # 퍼블리시 경로 설정
    pub_path = os.path.join(
        asset_root_path, dept, "pub", "maya", "scenes"
    )
    work_path = os.path.join(
        asset_root_path, dept, "work", "maya", "scenes"
    )

    # 최신 버전 확인
    version_nums = []
    work_files = os.listdir(work_path)
    for file_name in work_files:
        match = re.search(r"v(\d{3})", file_name)
        if match:
            version_nums.append(int(match.group(1)))

    last_version = max(version_nums, default=0) + 1

    maya_ascii_work_path = os.path.join(
        work_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
    )
    maya_ascii_pub_path = os.path.join(
        pub_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
    )

    # Maya파일을 work path에 저장 후 pub path에 메타데이터 까지 전부 복사
    cmds.file(rename=maya_ascii_work_path)
    cmds.file(save=True, type="mayaAscii")
    shutil.copy2(maya_ascii_work_path, maya_ascii_pub_path)
    print("퍼블리시가 완료되었습니다!")


def sg_mapping(lookdev_pub_dir, asset_name):
    """
    퍼블리시 전, 마야에 모든 쉐이딩 그룹을 가져와서,
    연결되어있는 mesh를 value, sg를 key값으로 json에 저장한다.
    """
    sg_mapping = {}

    # SG를 list 형식으로 모두 가져온 후, 불필요한 Dafult sg들을 필터링하여 거른다
    shadingEngines = cmds.ls(type="shadingEngine")
    for sg in shadingEngines:
        if sg in ["initialShadingGroup", "initialParticleSE"]:
            continue

        # 해당 SG와 연결되어있는 mesh를 찾는다
        meshes = cmds.sets(sg, query=True)
        if meshes:
            sg_mapping[sg] = meshes

    # 찾은 SG를 key, mesh를 value로 json파일에 저장한다.
    json_file = f"{asset_name}_sg_mapping.json"
    json_path = os.path.join(lookdev_pub_dir, json_file)
    if not os.path.exists(json_path):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(sg_mapping, f, indent=4)


def binding_material(lookdev_pub_dir, asset_name, root_usd_path):
    """
    json파일을 열어, usd 파일 내에 value와 동일한 mesh값이 있는지 확인.
    있다면 해당 prim의 정보를 가져오고, key값과 동일한 prim의 path를 가져와 연결해준다.
    """
    json_file = f"{asset_name}_sg_mapping.json"
    json_path = os.path.join(lookdev_pub_dir, json_file)

    # 루트 스테이지 실행
    asset_stage = Usd.Stage.Open(root_usd_path)

    with open(json_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    # asset의 rootstage를 돌며 prim이 Mesh라면 해당 prim의 name을 리스트에 추가
    # 그리고 json에 있는 mesh이름은 Shape이 붙기 때문에 json_mesh_name을 추가
    mesh_path_list = []
    for mesh_prim in asset_stage.Traverse():
        if mesh_prim.GetTypeName() == "Mesh":
            mesh_name = mesh_prim.GetName()
            json_mesh_name = f"{mesh_name}Shape"

            # json 파일에서 가져온 mesh 이름(json_mesh_name)이 
            # 현재 USD에서 찾은 mesh_name과 일치하면 해당 material의 이름(mtl_name)을 저장
            for k, v in mapping.items():
                if json_mesh_name in v:
                    mtl_name = k
                else:
                    pass

            # rootstage에서 현재 mesh_name과 동일한 prim을 찾아 해당 prim의 USD 경로(path)를 저장
            for prim in asset_stage.Traverse() :
                if mesh_name == prim.GetName() :
                    path = prim.GetPath()
            mesh_path_list.append([mesh_name, json_mesh_name, mtl_name, path])

    mtl_path_dict = {}

    # rootstage에서 lookdev의 primpath가 존재하는지 확인
    lookdev_prim_path = f"/{asset_name}/{asset_name}_lookdev"
    lookdev_prim = asset_stage.GetPrimAtPath(lookdev_prim_path)

    # 있다면 lookdev prim만 순회하며 json파일의 material(key값)과 동일한 prim의 name과 path를 가져온다.
    if lookdev_prim:
        for mtl_prim in Usd.PrimRange(lookdev_prim):
            if mtl_prim.GetTypeName() == "Material":
                mtl_key = mtl_prim.GetName()
                mtl_path = str(mtl_prim.GetPath())
                mtl_path_dict[mtl_key] = mtl_path

    # rootstage를 순회하며 리스트에 저장한 mesh의 정보들
    for mesh_name, json_mesh_name, mtl_name, mesh_path in mesh_path_list:
        if mtl_name not in mtl_path_dict:
            continue

        # 해당 path에 over prim을 생성 후 MaterialBindingAPI를 사용하여 material을 bind할 준비
        override_prim = asset_stage.OverridePrim(mesh_path)
        UsdShade.MaterialBindingAPI.Apply(override_prim)

        # rootstage에서 json 파일에서 찾은 Material 이름과 일치하는 prim이 존재하는지 확인
        material_prim = asset_stage.GetPrimAtPath(mtl_path_dict[mtl_name])
        if not material_prim:
            continue

        # material prim을 material로 지정해준 후 아까 생성해준 overprim에 bind
        material = UsdShade.Material(material_prim)
        binding_api = UsdShade.MaterialBindingAPI(override_prim)
        binding_api.Bind(material)
    
    asset_stage.GetRootLayer().Save()