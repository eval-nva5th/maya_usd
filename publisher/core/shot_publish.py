import os
import re
import shutil
import maya.cmds as cmds
from publish_usd import ShotExportUSD

root_directory = '/Users/junsu/Desktop'

def shot_publish(project_name, seq, shot_num, dept):
    """shot publish 실행 함수"""

    # 해당 dept가 아니라면 함수 종료
    if dept not in ["layout", "animation", "light"]:
        print("해당 dept는 사용할 수 없습니다.")
        return

    # 파일 경로 설정
    shot_root_path = os.path.join(
        root_directory, project_name,"seq", seq, shot_num
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

        # 퍼블리시 경로 설정
        pub_path = os.path.join(
            shot_root_path, dept, "pub", "maya", "scenes"
        )
        work_path = os.path.join(
            shot_root_path, dept, "work", "maya", "scenes"
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
            work_path, f"{shot_num}_{dept}_v{last_version:03d}.ma"
        )
        maya_ascii_pub_path = os.path.join(
            pub_path, f"{shot_num}_{dept}_v{last_version:03d}.ma"
        )

        # Maya파일을 work path에 저장 후 pub path에 메타데이터 까지 전부 복사
        cmds.file(rename=maya_ascii_work_path)
        cmds.file(save=True, type="mayaAscii")
        shutil.copy2(maya_ascii_work_path, maya_ascii_pub_path)
    print("퍼블리시가 완료되었습니다!")