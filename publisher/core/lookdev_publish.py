import os, shutil, re
from pxr import Usd, UsdShade
import maya.cmds as cmds
from publish_usd import LookdevExportUSD

from systempath import SystemPath
root_path = SystemPath().get_root_path()
root_directory = f"{root_path}/show"

def lookdev_publish(project_name, asset_name, asset_type, dept) :
    """lookdev publish 실행 함수"""
    if dept != "lookdev":
        print("해당 dept는 사용할 수 없습니다.")
        return
    
    asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)
    lookdev_pub_dir = os.path.join(asset_root_path, dept, "pub", "usd")
    lookdev_pub_path = os.path.join(lookdev_pub_dir, f"{asset_name}_{dept}.usda")
    model_pub_path  = os.path.join(asset_root_path, "model", "pub", "usd", f"{asset_name}_model.usda")
    root_usd_path = os.path.join(asset_root_path, f"{asset_name}.usda")
    relative_lookdev_pub_path= os.path.relpath(lookdev_pub_path, os.path.dirname(root_usd_path))

    if os.path.exists(lookdev_pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

        exporter = LookdevExportUSD(lookdev_pub_path, asset_name, dept)
        exporter.export()

    if os.path.exists(root_usd_path):
        asset_stage = Usd.Stage.Open(root_usd_path)
    else:
        asset_stage = Usd.Stage.CreateNew(root_usd_path)

    sub_prim = asset_stage.GetPrimAtPath(f"/{asset_name}/{asset_name}_{dept}")
    if not sub_prim:
        sub_prim = asset_stage.DefinePrim(f"/{asset_name}/{asset_name}_{dept}", "Scope")
        sub_prim.GetReferences().AddReference(relative_lookdev_pub_path)

    mesh_prims = {}
    for mesh_prim in asset_stage.Traverse():
        if mesh_prim.GetTypeName() == "Mesh":
            mesh_name = mesh_prim.GetName()
            mesh_prims[mesh_name] = mesh_prim.GetPath().pathString

    material_prims = {}
    for material_prim in asset_stage.Traverse():
        if material_prim.GetTypeName() == "Material":
            material = material_prim.GetName().replace("_taxture", "")
            material_prims[material] = material_prim.GetPath().pathString

    for mesh_name, mesh_path in mesh_prims.items():
        if mesh_name in material_prims:  # 동일한 이름이 있으면 매칭
            material_path = material_prims[mesh_name]

            # Material Binding API 사용
            mesh_prim = asset_stage.GetPrimAtPath(mesh_path)
            material_prim = asset_stage.GetPrimAtPath(material_path)

            material = UsdShade.Material(material_prim)
            material_binding_api = UsdShade.MaterialBindingAPI(mesh_prim)
            material_binding_api.Bind(material)

    asset_stage.GetRootLayer().Save()

    pub_path = os.path.join(asset_root_path, dept, "pub", "maya", "scenes")
    work_path = os.path.join(asset_root_path, dept, "work", "maya", "scenes")

    version_nums = []
    work_files = os.listdir(work_path)
    for file_name in work_files:
        match = re.search(r"v(\d{3})", file_name)
        if match:
            version_nums.append(int(match.group(1)))

    last_version = max(version_nums, default=0) + 1

    maya_ascii_work_path = os.path.join(work_path, f"{asset_name}_{dept}_v{last_version:03d}.ma")
    maya_ascii_pub_path = os.path.join(pub_path, f"{asset_name}_{dept}_v{last_version:03d}.ma")

    cmds.file(rename=maya_ascii_work_path)
    cmds.file(save=True, type="mayaAscii")
    shutil.copy2(maya_ascii_work_path, maya_ascii_pub_path)
    print("퍼블리시가 완료되었습니다!")