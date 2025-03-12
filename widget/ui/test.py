
#ct.entity_id: 1254

import shotgun_api3

sg_url = "https://hi.shotgrid.autodesk.com/"
script_name = "Admin_SY"
api_key = "kbuilvikxtf5v^bfrivDgqhxh"

# ShotGrid API 연결
sg = shotgun_api3.Shotgun(sg_url, script_name, api_key)

# 특정 엔티티 ID (예: Asset ID)
entity_id = 1254  # 조회할 엔티티의 ID 입력
entity_type = "Shot"  # 엔티티 타입 (예: "Asset", "Shot")'
file_name = "human_rig_v001.usd"

# colleague_list = []
# # 테스크 조회
# tasks = sg.find(
#     "Task",
#     [["entity", "is", {"type": entity_type, "id": entity_id}]], 
#     ["id", "task_assignees", "step"]
# )

# # 결과 출력
# for task in tasks:
#     task_type = task["step"]["name"]
#     assignees = task["task_assignees"]  # 리스트 형식으로 반환됨

#     if assignees :
#         assignees_name = assignees[0]['name']
#         assignees_id = assignees[0]['id']

#     else:
#         assignees_name = "None"
#         assignees_id = 0
#     each_list = [task_type, assignees_name, assignees_id]
#     if len(each_list) == 3:
#         colleague_list.append(each_list)

# print(colleague_list)

file_name = "human_rig_v001.usd"

filters = [["code", "is", "human_rig_v001.usd"]]
fields = ["id", "code", "versions"]  # versions 필드를 가져옴

published_files = sg.find("PublishedFile", filters, fields)

# 결과 출력
for pf in published_files:
    print(f"Published File: {pf['code']} (ID: {pf['id']})")
    if pf["versions"]:
        version_id = pf["versions"]["id"]
        version_data = sg.find_one("Version", [["id", "is", version_id]], ["code", "sg_status_list"])
        print(f"Linked Version: {version_data['code']} (Status: {version_data['sg_status_list']})")
    else:
        print("No linked version.")


        import shotgun_api3

