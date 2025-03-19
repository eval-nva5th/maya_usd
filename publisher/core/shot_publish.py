import os
import re
import shutil
import maya.cmds as cmds
from publisher.core.publish_usd import ShotExportUSD
from systempath import SystemPath
root_path = SystemPath().get_root_path()

def shot_publish(project_name, seq, shot_num, dept):
    print(root_path)

    root_directory =  f"{root_path}/show"
    """shot publish 실행 함수"""

    # 해당 dept가 아니라면 함수 종료
    if dept not in ["layout", "animation", "light"]:
        return

    shot_root_path = os.path.join(
        root_directory, project_name, "seq", seq, shot_num
    )
    pub_dir = os.path.join(
        shot_root_path, dept, "pub", "usd"
    )
    usd_publish_path = os.path.join(
        pub_dir, f"{shot_num}_{dept}.usda"
    )

    # Maya USD플러그인이 없다면 실행
    if os.path.exists(pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

        exporter = ShotExportUSD(usd_publish_path, seq, shot_num)
        exporter.export()

    print("퍼블리시가 완료되었습니다!")