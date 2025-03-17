import shotgun_api3 

from shotgridapi import ShotgridAPI
sg = ShotgridAPI().shotgrid_connector()

# SHOTGRID_URL = "https://nashotgrid.shotgrid.autodesk.com/"
# SCRIPT_NAME = "test"
# API_KEY = "hetgdrcey?8coevsotrgwTnhv"

# # ShotGrid 연결
# sg = shotgun_api3.Shotgun(SHOTGRID_URL, SCRIPT_NAME, API_KEY)

# 프로젝트 정보 가져오기
#project = sg.find_one("Project", [["name", "is", "eval"]])

# 스토리지 목록 조회
storages = sg.find("LocalStorage", [], ["id", "code", "windows_path", "linux_path", "mac_path"])

# 스토리지 정보 출력
for storage in storages:
    print(f"Storage ID: {storage['id']}, Code: {storage['code']}, Paths: {storage['windows_path']}, {storage['linux_path']}, {storage['mac_path']}")

# # 로컬 파일 경로 설정 (여러 플랫폼 지원)
# local_path = "/nas/eval/show/eval/assets/vehicle/bike/modelling/work/maya/scenes/bike_modelling_v001.usd"

# # ShotGrid Published File 등록
# published_file_data = {
#     "project": project,
#     "code": "bike_modelling_v001.usd",  # 파일 이름
#     "description": "test test",
#     "published_file_type": {"type": "PublishedFileType", "name": "USD File"},
#     "path": {
#         "local_path": local_path,
#         "local_path_linux": local_path,  # ✅ 리눅스용 경로
#         "local_path_mac": local_path,    # ✅ 맥용 경로 (필요 시 수정)
#         "local_path_windows": "Z:\\eval\\show\\eval\\assets\\vehicle\\bike\\modelling\\work\\maya\\scenes\\bike_modelling_v001.usd"  # ✅ 윈도우용 경로 (필요 시 수정)
#     },
#     "task": {"type": "Task", "id": 5900},  # 연결할 Task ID
#     "entity": {"type": "Asset", "id": 1525},  # 연결할 Asset ID
# }

# # ShotGrid에 등록
# published_file = sg.create("PublishedFile", published_file_data)

# print(f"✅ ShotGrid Published File 생성 완료: {published_file}")
