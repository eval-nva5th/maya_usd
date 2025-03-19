try :
    from PySide2.QtCore import QThread, Signal
except Exception :
    from PySide6.QtCore import QThread, Signal
from asset_library.run_asset_library import run

import time, os
import maya.cmds as cmds
from publisher.core.play_blast import PlayblastManager
from publisher.ui.publisher_ui import PublisherDialog

def clicked_get_asset_btn():
    run()

def publish_playblast_run(self, ct):
    file_path = cmds.file(q=True, sceneName=True)
    file_name_with_ext = os.path.basename(file_path)
    file_name, _ = os.path.splitext(file_name_with_ext)

    output_file = PlayblastManager(file_path, file_name).run_playblast()
    print ("생성된 파일", output_file)

    self.worker = PlayblastChecker(output_file)
    self.worker.file_found.connect(lambda: show_publish_ui(self, output_file, ct))
    self.worker.start()

def show_publish_ui(self, video_path, ct):
    print(f"Playblast 완료! 파일 경로: {video_path}")
    self.publish_dialog = PublisherDialog(video_path, ct)  # 파일 경로를 전달
    self.publish_dialog.show()

class PlayblastChecker(QThread): # 플레이 블라스트 체크 클래스.
    file_found = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.output_file = file_path
    def run(self):
        while not os.path.exists(self.output_file):
            time.sleep(0.5) # 0.5초마다 확인

        self.file_found.emit(self.output_file)