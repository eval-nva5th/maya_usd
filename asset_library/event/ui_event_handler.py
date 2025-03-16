import os
from DefaultConfig import DefaultConfig

default_config = DefaultConfig()
root_path = default_config.get_root_path()

prefix_path = f"{root_path}/show"
proj_name = "eval"
entity_type = "assets"

path_list = [proj_name, entity_type]
asset_list = []
asset_type_path = os.path.join(prefix_path, *path_list)

def clicked_load_btn(ui_instance, selected_cells):
    for selected_cell in selected_cells:
        image_path = selected_cell.image_path
        asset_name = selected_cell.asset_name

        relative_path = image_path.split("/eval/assets/")[-1]  # 'vehicle/bike/model/pub/maya/data/bike_model.jpg'
        asset_type = relative_path.split("/")[0] # vehicle

        jpg_file_name = relative_path.split("/")[-1]
        usd_file_name = change_ext(jpg_file_name, "usda")
        # /nas/eval/show/eval/assets/model/pub/usd/bike_model.usda
        usd_file_path = os.path.join(prefix_path, proj_name, entity_type, asset_type, "pub/usd", usd_file_name)
        print(usd_file_path)

        
        #print(asset_type, usd_file_name)
    ui_instance.close()

def change_ext(file_path, ext):
        base_name, _ = os.path.splitext(file_path)
        return f"{base_name}.{ext}"