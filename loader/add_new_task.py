# from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox, QMainWindow

from pxr import Usd, Sdf, Kind
import os

class Create_task:
    def __init__(self):
        self.local_path = '/nas/eval/show'

    def create_asset_root_stage(self, project_name , asset_name, asset_type, dept, payload=False):

        assets_path = f"{self.local_path}/{project_name}/assets/{asset_type}/{asset_name}"
        os.makedirs(assets_path, exist_ok=True)

        root_stage_path = os.path.join(assets_path, f"{asset_name}.usda")
        asset_usd_name = f"{asset_name}_{dept}_v001.usd"
        asset_usd_path = f"./{asset_usd_name}"
        asset_root_stage = Usd.Stage.CreateNew(root_stage_path)

        prim_type = input("타입을 선택해주세요: (Xform/Scope/Mesh/Material): ").strip()
        if prim_type not in ["Xform", "Scope", "Mesh", "Material"]:
            print("타입이 존재하지 않습니다. 기본은 Xform입니다.")
            prim_type = "Xform"

        root_prim = asset_root_stage.DefinePrim(f"/{asset_name}", prim_type)

        if payload:
            root_prim.GetPayloads().AddPayload(asset_usd_path)
        else:
            root_prim.GetReferences().AddReference(asset_usd_path)

        asset_root_stage.GetRootLayer().Save()

task = Create_task()
task.create_asset_root_stage("project1", "junsu", "character", "model", payload=True)