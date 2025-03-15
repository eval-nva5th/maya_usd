import os, shutil, re
import maya.cmds as cmds
from publish_usd import LayoutExportUSD

root_directory = '/Users/junsu/Desktop'

def layout_publish(project_name, seq, shot_num, dept):
    """layout publish 실행 함수"""
    if dept != "layout":
        print("해당 dept는 사용할 수 없습니다.")
        return
    
    shot_root_path = os.path.join(root_directory, project_name,"seq", seq, shot_num)
    layout_pub_dir = os.path.join(shot_root_path, dept, "pub", "usd")
    usd_publish_path = os.path.join(layout_pub_dir, f"{shot_num}_{dept}.usda")

    if os.path.exists(layout_pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")
        exporter = LayoutExportUSD(usd_publish_path, seq, shot_num)
        exporter.export()

        pub_path = os.path.join(shot_root_path, dept, "pub", "maya", "scenes")
        work_path = os.path.join(shot_root_path, dept, "work", "maya", "scenes")

        version_nums = []
        work_files = os.listdir(work_path)
        for file_name in work_files:
            match = re.search(r"v(\d{3})", file_name)
            if match:
                version_nums.append(int(match.group(1)))

        last_version = max(version_nums, default=0) + 1

        maya_ascii_work_path = os.path.join(work_path, f"{shot_num}_{dept}_v{last_version:03d}.ma")
        maya_ascii_pub_path = os.path.join(pub_path, f"{shot_num}_{dept}_v{last_version:03d}.ma")
        cmds.file(rename=maya_ascii_work_path)
        cmds.file(save=True, type="mayaAscii")
        shutil.copy2(maya_ascii_work_path, maya_ascii_pub_path)
    print("퍼블리시가 완료되었습니다!")