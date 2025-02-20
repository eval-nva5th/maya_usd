from shotgun_api3 import Shotgun

class ShotGridManager:
    def __init__(self, server_url, script_name, api_key):
        """ShotGrid API 초기화"""
        self.sg = Shotgun(server_url, script_name, api_key)

    # 프로젝트 ID 가져오기
    def get_project_id(self, project_name):
        project_data = self.sg.find_one("Project", [["name", "is", project_name]], ["id"])
        return project_data["id"] if project_data else None
    
    # Project에 속한 Sequence 젠부 가져오기
    def get_all_sequence(self, project_id):
        sequences = self.sg.find(
            "Sequence",
            [["project", "is", {"type": "Project", "id": project_id}]],
            ["id", "code", "sg_status_list", "description", "cached_display_name"]
        )
        if sequences:
            print(f"프로젝트 ID {project_id}의 시퀀스 목록:")
            for sequence in sequences:
                print(f"시퀀스 NAME: {sequence['cached_display_name']} | 시퀀스 ID: {sequence['id']} | 코드: {sequence['code']} | 상태: {sequence['sg_status_list']} | 설명: {sequence.get('description', '없음')}")
                
        else:
            print(f"프로젝트 ID {project_id}에 속하는 시퀀스가 없습니다!")
        
        return sequences
    
    # shot 정보 따오기
    def get_all_shots(self, project_id):
        shots = self.sg.find(
            "Shot",  # Shot 엔티티에서 조회
            [["project", "is", {"type": "Project", "id": project_id}]],  
            ["id", "code", "sg_status_list", "description", "cached_display_name", "sg_sequence"]  
        )

        if shots:
            print(f"프로젝트 ID {project_id}의 Shot 목록:")
            for shot in shots:
                if "sg_sequence" in shot and shot["sg_sequence"]:
                    sequence_name = shot["sg_sequence"]["name"]
                else : 
                    sequence_name = None
                print(f"Shot NAME: {shot['cached_display_name']} | Shot ID: {shot['id']} | 코드: {shot['code']} | 상태: {shot['sg_status_list']} | 시퀀스: {sequence_name} | 설명: {shot.get('description', '없음')}")
        else:
            print(f"프로젝트 ID {project_id}에 속하는 Shot이 없습니다!")

        return shots
    
    # asset 정보 따오기
    def get_all_assets(self, project_id):
        assets = self.sg.find(
        "Asset", 
        [["project", "is", {"type": "Project", "id": project_id}]],  # 특정 프로젝트의 Asset 필터링
        ["id", "code", "sg_asset_type", "tasks"]  # Asset ID, 이름, 타입, 연결된 Task 조회
    )

        if assets:
            print(f"\n프로젝트 ID {project_id}의 Asset 목록:")
            for asset in assets:
                asset_id = asset["id"]
                asset_name = asset["code"]
                asset_type = asset.get("sg_asset_type", "None")  # Asset Type (Character, Prop 등)

                print(f"\nAsset: {asset_name} | ID: {asset_id} | 타입: {asset_type}")

                # 해당 Asset에 연결된 Task Type(Step) 조회
                tasks = self.sg.find(
                    "Task",
                    [["entity", "is", {"type": "Asset", "id": asset_id}]],
                    ["id", "content", "sg_status_list", "step"]  
                )

                if tasks:
                    print(f"연결된 Task 목록:")
                    for task in tasks:
                        task_name = task["content"]
                        task_status = task["sg_status_list"]
                        task_type = task["step"]["name"] if task.get("step") else "없음"  # Task Type 정보 가져오기
                        print(f"  -  Task: {task_name} | 상태: {task_status} | Task Type: {task_type}")
                else:
                    print("연결된 Task가 없습니다!")

        else:
            print(f"프로젝트 ID {project_id}에 속하는 Asset이 없습니다!")

        return assets

    def sequence_help(self):
        sequence_fields = sg_manager.sg.schema_field_read("Sequence")
        print("Sequence 엔티티의 사용 가능한 필드 목록:")
        for field_name, field_info in sequence_fields.items():
            print(f"필드 이름: {field_name} | 타입: {field_info['data_type']['value']}")

    def asset_help(self):
        sequence_fields = sg_manager.sg.schema_field_read("Asset")
        print("Asset 엔티티의 사용 가능한 필드 목록:")
        for field_name, field_info in sequence_fields.items():
            print(f"필드 이름: {field_name} | 타입: {field_info['data_type']['value']}")

    def task_help(self):
        task_fields = sg_manager.sg.schema_field_read("Task")
        print("Task 엔티티의 사용 가능한 필드 목록:")
        for field_name, field_info in task_fields.items():
            print(f"필드 이름: {field_name} | 타입: {field_info['data_type']['value']}")



if __name__ == "__main__":
    SHOTGRID_URL = "https://nashotgrid.shotgrid.autodesk.com/"
    SCRIPT_NAME = "Get_Worker_Name"
    API_KEY = "kiMncpgjfz-tqv3nfjelujlmm"

    sg_manager = ShotGridManager(SHOTGRID_URL, SCRIPT_NAME, API_KEY)

    PROJECT_ID = sg_manager.get_project_id("applestore")
    # sg_manager.get_all_sequence(PROJECT_ID)
    # sg_manager.get_all_shots(PROJECT_ID)
    sg_manager.get_all_assets(PROJECT_ID)
    # sg_manager.asset_help()
    # sg_manager.task_help()
    