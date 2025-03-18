import os
import re
import maya.cmds as cmds
<<<<<<< HEAD

def save_as(project_name, asset_name, asset_type, dept):
    root_directory = '/nas/eval/show'
=======
from systempath import SystemPath
from shotgridapi import ShotgridAPI

root_path = SystemPath().get_root_path()
sg = ShotgridAPI().shotgrid_connector()

def save_as(project_name, asset_name, asset_type, dept):
    root_directory = f'{root_path}/show'
>>>>>>> 5a6ae0e1741dd843f1d46a06403a97460a5dfad1
    asset_root_path = os.path.join(
    root_directory, project_name, "assets", asset_type, asset_name
    )
    work_path = os.path.join(
        asset_root_path, dept, "work", "maya", "scenes"
    )

    version_nums = []
    work_files = os.listdir(work_path)
    for file_name in work_files:
        match = re.search(r"v(\d{3})", file_name)
        if match:
            version_nums.append(int(match.group(1)))

    if version_nums:
        last_version = max(version_nums)+1
    else:
        last_version = 1 

    maya_ascii_work_path = os.path.join(
        work_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
    )
    cmds.file(rename=maya_ascii_work_path)
    cmds.file(save=True, type="mayaAscii")