import os, shutil, re
import maya.cmds as cmds
from DefaultConfig import DefaultConfig

default_config = DefaultConfig()
root_path = default_config.get_root_path()

root_directory = '/Users/junsu/Desktop' ##### 수정 필요

def rig_publish(project_name, asset_name, asset_type, dept):
    """rig publish 실행 함수"""
    if dept != "rig":
        print("해당 dept는 사용할 수 없습니다.")
        return
    
    asset_root_path = os.path.join(root_directory, project_name, "assets", asset_type, asset_name)

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