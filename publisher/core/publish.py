from shotgun_api3 import Shotgun
import os
import sys
import socket
#import maya.cmds as cmds

maya_usd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../loader"))
print(f"maya_usd 경로: {maya_usd_path}")
sys.path.append(maya_usd_path)

from shotgrid_user_task import TaskInfo, UserInfo, ClickedTask

class Shotgrid:
    def __init__(self, sg_url, script_name, api_key):
        self.sg = Shotgun(sg_url, script_name, api_key)

class PublishManager(Shotgrid):
    def __init__(self, sg_url, script_name, api_key, clicked_task):
        super().__init__(sg_url, script_name, api_key)
        self.clicked_task = clicked_task
        self.project_id = clicked_task.proj_id
        self.task_id = clicked_task.id
        self.entity_id = clicked_task.entity_id
        self.entity_type = self.get_entity_type(clicked_task.entity_type)
        self.assignee = self.get_assignee()
        self.file_name = ""
        self.file_path = ""
        self.description = ""
        self.thumbnail_path = ""
        self.mov_path = ""

    def get_entity_type(self, entity_type):
        return "Shot" if entity_type == "seq" else "Asset"
    

    def get_internal_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))  
            internal_ip = s.getsockname()[0]
        except Exception:
            internal_ip = "127.0.0.1"
        finally:
            s.close()
        return internal_ip
    
    def get_assignee(self):
        # hostname = socket.gethostname()
        # internal_ip = socket.gethostbyname(hostname)
        internal_ip = self.get_internal_ip()
        last_ip = int(internal_ip.split(".")[-1])
        return self.sg.find_one("HumanUser", [["sg_ip", "is", last_ip]])
    
    def set_file_path(self,file_path):
        # file_path = cmds.file(q=True, sn=True)
        #file_path = "/nas/eval/show/eval/assets/vehicle/bike/model/pub/maya/scenes/bike_model_v001.usd"
        self.file_path = file_path

    def set_file_name(self, file_path):
        file_name = file_path.split("/")[-1]
        self.file_name = file_name

    def set_description(self, description):
        self.description = description

    def set_thumbnail_path(self, file_path, ext):
        thumb_path = os.path.abspath(os.path.join(file_path, f"../../data/{file_name}"))
        thumb_path = self.change_ext(thumb_path, ext)
        self.thumbnail_path = thumb_path
    
    def set_mov_path(self, file_path, ext):
        mov_path = os.path.abspath(os.path.join(file_path, f"../../data/{file_name}"))
        mov_path = self.change_ext(mov_path, ext)
        self.mov_path = mov_path

    def change_ext(self, file_path, ext):
        base_name, _ = os.path.splitext(file_path)
        return f"{base_name}.{ext}"
    
    def create_published_file(self):
        published_file_data = {
        "project": {'type': 'Project', 'id': self.project_id}, 
        "code": self.file_name, 
        "task": {'type': 'Task', 'id': self.task_id},
        "entity": {'type': self.entity_type, 'id': self.entity_id},
        "created_by": self.assignee,
        "sg_status_list": "pub",
        "description":self.description,
        "sg_local_path":self.file_path,
        "image" : self.thumbnail_path
        }

        published_file = self.sg.create("PublishedFile", published_file_data)
        print(published_file)
        return published_file

    def create_versions(self):
        version_data = {
            "project" : {'type': 'Project', 'id': self.project_id}, 
            "code" : self.file_name,
            "sg_task" : {'type': 'Task', 'id': self.task_id},
            "entity" : {'type': self.entity_type, 'id': self.entity_id},
            "user" : self.assignee,
            "sg_status_list" : "rev",
            "description" : self.description
        }
        created_version = self.sg.create("Version", version_data)
        self.sg.upload("Version", created_version["id"], self.mov_path, field_name="sg_uploaded_movie")
        return created_version
    
    def link_version_to_published_file(self, pub_id, version_id):
        self.sg.update("PublishedFile", pub_id, {"version":{"type":"Version", "id":version_id}})
        

if __name__ == "__main__":
    SHOTGRID_URL = "https://5thacademy.shotgrid.autodesk.com/"
    SCRIPT_NAME = "sy_key"
    SCRIPT_KEY = "vkcuovEbxhdoaqp9juqodux^x"

    # my_dict = {
    #     "proj_name" : "eval",
    #     "proj_id" : 123,
    #     "id" : 6084,
    #     "entity_id" : 1214,
    #     "entity_name" : "AAB_0010",
    #     "entity_type" : "seq",
    #     "entity_parent" : "AAB",
    #     "step": "Light"
    #     }
    my_dict = {
        "proj_name" : "eval",
        "proj_id" : 123,
        "id" : 5827,
        "entity_id" : 1431,
        "entity_name" : "bike",
        "entity_type" : "assets",
        "entity_parent" : "Vehicle",
        "step": "Model"
        }
    clicked_task = ClickedTask(my_dict)
    publish_manager = PublishManager(SHOTGRID_URL, SCRIPT_NAME, SCRIPT_KEY, clicked_task)

    # file_name = "AAB_0010_light_v001.usd"
    # local_path = "/nas/eval/show/eval/seq/AAB/AAB_0010/light/pub/maya/scenes/AAB_0010_light_v001.usd"
    # status = "pub"
    # description = "Final render for shot X" 
    # #thumbnail_path = "/nas/eval/show/eval/seq/AAB/AAB_0010/light/pub/maya/data/AAB_0010_light.jpg" 
    
    file_name = "bike_model_v001.usd"
    local_path = "/nas/eval/show/eval/assets/vehicle/bike/model/pub/maya/scenes/bike_model_v001.usd"
    status = "pub"
    description = "Bike model v001 publish" 
    #thumbnail_path = "/nas/eval/show/eval/assets/vehicle/bike/model/pub/maya/data/bike_model_v001.jpg" 
    
    publish_manager.set_file_name(file_name)
    publish_manager.set_file_path(local_path)
    publish_manager.set_file_name(local_path)
    publish_manager.set_description(description)
    publish_manager.set_thumbnail_path(local_path, "jpg")
    publish_manager.set_mov_path(local_path, "mov")

    created_version = publish_manager.create_versions()
    published_file = publish_manager.create_published_file()
    publish_manager.link_version_to_published_file(published_file["id"], created_version["id"])
    

