import os
import re
import shutil
import maya.cmds as cmds
from publisher.core.publish_usd import ModelExportUSD
from pxr import Usd
from systempath import SystemPath 
root_path = SystemPath().get_root_path()

root_directory = f'{root_path}/show'

def model_publish(project_name, asset_name, asset_type, dept):
    """model publish 실행 함수"""

    # 모델러가 아니라면 함수 종료
    if dept != "model":
        print("해당 dept는 사용할 수 없습니다.")
        return

    # 파일 경로 설정
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
        is_sub_prim = asset_stage.GetGetPrimAtPath(sub_prim_path)
        if not is_sub_prim:
            is_sub_prim = asset_stage.DefinePrim(sub_prim_path, "Xform")
            is_sub_prim.GetReferences().AddReference(relative_model_pub_path)
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

