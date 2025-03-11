from shotgun_api3 import Shotgun
import os
import sys

#import maya.cmds as cmds

maya_usd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../loader"))
print(f"maya_usd 경로: {maya_usd_path}")
sys.path.append(maya_usd_path)

from shotgrid_user_task import TaskInfo, UserInfo, ClickedTask

class Shotgrid:
    def __init__(self, sg_url, script_name, api_key):
        self.sg = Shotgun(sg_url, script_name, api_key)

class PublishManager(Shotgrid):
    def __init__(self, sg_url, script_name, api_key):
        super().__init__(sg_url, script_name, api_key)