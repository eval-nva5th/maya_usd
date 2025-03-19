import os
import re
import shutil
import maya.cmds as cmds
from publisher.core.publish_usd import ModelExportUSD
from pxr import Usd
from systempath import SystemPath 
root_path = SystemPath().get_root_path()

def model_publish(project_name, asset_type, asset_name, dept):
    """model publish 실행 함수"""
    
    # 모델러가 아니라면 함수 종료
    if dept != "model":
        print(f"여기에 리턴이 찍힘 {dept}")
        return
    
    print(project_name, asset_name, asset_type, dept)
    # 파일 경로 설정
    root_directory =  f"{root_path}/show"

    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )
    model_pub_dir = os.path.join(
        asset_root_path, dept, "pub", "usd"
    )
    model_publish_path = os.path.join(
        model_pub_dir, f"{asset_name}_{dept}.usda"
    )
    root_usd_path = os.path.join(
        asset_root_path, f"{asset_name}.usda"
    )
    relative_model_pub_path = os.path.relpath(
        model_publish_path, os.path.dirname(root_usd_path)
    )

    # Maya USD플러그인이 없다면 실행
    if os.path.exists(model_pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

        exporter = ModelExportUSD(model_publish_path, asset_name, dept)
        exporter.export()

    # 루트 스테이지 실행 (없다면 생성)
    asset_stage = (
    Usd.Stage.Open(root_usd_path)
    if os.path.exists(root_usd_path)
    else Usd.Stage.CreateNew(root_usd_path)
    )

    # 루트스테이지 defaultprim 설정 후 model.usd를 reference로 추가.
    if os.path.exists(root_usd_path):
        root_prim = asset_stage.DefinePrim(f"/{asset_name}", "Xform")
        asset_stage.SetDefaultPrim(root_prim)

        sub_prim_path = f"/{asset_name}/{asset_name}_{dept}"
        is_sub_prim = asset_stage.GetPrimAtPath(sub_prim_path)
        if not is_sub_prim:
            is_sub_prim = asset_stage.DefinePrim(sub_prim_path, "Xform")
            is_sub_prim.GetReferences().AddReference(relative_model_pub_path)
    asset_stage.GetRootLayer().Save()
    print("퍼블리시가 완료되었습니다.")