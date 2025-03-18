import os
from systempath import SystemPath
import maya.cmds as cmds
root_path = SystemPath().get_root_path()

prefix_path = f"{root_path}/show"
proj_name = "eval"
entity_type = "assets"

path_list = [proj_name, entity_type]
asset_list = []
asset_type_path = os.path.join(prefix_path, *path_list)

# Asset Library의 Load 버튼을 눌렀을때 선택된 asset들을 열려있는 MAYA로 load
# selected_cells example : [('bike', '/nas/eval/show/eval/assets/vehicle/bike/model/pub/maya/data/bike_model.jpg'), ... ]
def clicked_load_btn(ui_instance, selected_cells):
    for selected_cell in selected_cells:
        asset_name = selected_cell.asset_name
        usd_file_name = f"{asset_name}.usda"
        asset_type_list = ["character", "environment", "vehicle", "prop"]
        for asset_type in asset_type_list:
            # usd_file_paht example : "/nas/eval/show/eval/assets/character/Hyung/Hyung.usda"
            usd_file_path = os.path.join(prefix_path, proj_name, entity_type, asset_type, asset_name, usd_file_name)
            if os.path.exists(usd_file_path):    
                cmds.file(usd_file_path, reference=True, defaultNamespace=True)
    ui_instance.close()