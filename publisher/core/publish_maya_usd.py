import os, shutil, re
import maya.cmds as cmds
from pxr import Usd
from abc import ABC, abstractmethod
from DefaultConfig import DefaultConfig

default_config = DefaultConfig()
root_path = default_config.get_root_path()

class USDExporter(ABC):
    def __init__(self, usd_publish_path):
        super().__init__()
        self.usd_publish_path = usd_publish_path

    @abstractmethod
    def get_export_options(self):
        pass

    @abstractmethod
    def export(self):
        options = self.get_export_options()
        cmds.mayaUSDExport(
            file=self.usd_publish_path,
            **options
        )

class ModelExportUSD(USDExporter):
    def get_export_options(self):
        return{
            "selection": True,
            "exportUVs": True,
            "exportDisplayColor": True,
            "exportMaterialCollections": True,
            "defaultMeshScheme": "catmullClark",
            "exportInstances": True,
            "exportBlendShapes": True,
            "exportSkels": "auto",
            "exportSkin": "auto",
        }

class LookdevExportUSD(USDExporter):
    def get_export_options(self):
        return{
            "selection": True,
            # "exportReferencesAsPayloads":False,
            "exportUVs": True,
            "exportDisplayColor": True,
            "exportMaterialCollections": True,
            "defaultMeshScheme": "catmullClark",
            "exportInstances": True,
            "exportBlendShapes": False,
            "exportSkels": "none",
            "exportSkin": "none",
        }


root_directory = f'{root_path}/show'

def publish_model(project_name, asset_name, asset_type, dept):
    if dept != "model":
        print("해당 dept는 사용할 수 없습니다.")

    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )
    model_pub_dir = os.path.join(
        asset_root_path, dept, "pub", "usd"
    )

    if os.path.exists(model_pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")
        usd_publish_path = os.path.join(model_pub_dir, f"{asset_name}_{dept}.usda")
        exporter = ModelExportUSD(usd_publish_path)
        exporter.export

        root_usd_path = os.path.join(
            asset_root_path, f"{asset_name}.usda"
        )
        relative_usd_file_path = os.path.relpath(
            usd_publish_path, os.path.dirname(root_usd_path)
        )
        if os.path.exists(root_usd_path):
            asset_stage = Usd.Stage.Open(root_usd_path)
        root_prim = asset_stage.DefinePrim(f"/{asset_name}", "Xform")
        asset_stage.SetDefaultPrim(root_prim)
        root_prim.GetReferences().AddReference(relative_usd_file_path)
        asset_stage.GetRootLayer().Save()

        pub_path = os.path.join(
            asset_root_path, dept, "pub", "maya", "scenes"
        )
        work_path = os.path.join(
            asset_root_path, dept, "work", "maya", "scenes"
        )

        version_nums = []
        work_files = os.listdir(work_path)
        for file_name in work_files:
            match = re.search(r"v(\d{3})", file_name)
            if match:
                version_nums.append(int(match.group(1)))

        if version_nums:
            last_version = max(version_nums)+1
        else:
            last_version = 1 

        maya_ascii_work_path = os.path.join(
            work_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
        )
        maya_ascii_pub_path = os.path.join(
            pub_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
        )
        cmds.file(rename=maya_ascii_work_path)
        cmds.file(save=True, type="mayaAscii")
        shutil.copy2(maya_ascii_work_path, maya_ascii_pub_path)

def publish_lookdev(project_name, asset_name, asset_type, dept):
    if dept != "lookdev":
        print("해당 dept는 사용할 수 없습니다.")

    asset_root_path = os.path.join(
        root_directory, project_name, "assets", asset_type, asset_name
    )
    lookdev_pub_dir = os.path.join(
        asset_root_path, dept, "pub", "usd"
    )

    if os.path.exists(lookdev_pub_dir):
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")
        usd_publish_path = os.path.join(
            lookdev_pub_dir, f"{asset_name}_{dept}.usda"
        )
        shading_usd_path = os.path.join(
            lookdev_pub_dir, f"{asset_name}_{dept}_shading.usda"
        )

        exporter = LookdevExportUSD(shading_usd_path)
        exporter.export

        root_usd_path = os.path.join(
            asset_root_path, f"{asset_name}.usda"
        )
        relative_usd_file_path = os.path.relpath(
            usd_publish_path, os.path.dirname(root_usd_path)
        )
        if os.path.exists(root_usd_path):
            asset_stage = Usd.Stage.Open(root_usd_path)
        root_prim = asset_stage.DefinePrim(f"/{asset_name}", "Xform")
        asset_stage.SetDefaultPrim(root_prim)
        root_prim.GetReferences().AddReference(relative_usd_file_path)
        asset_stage.GetRootLayer().Save()

        pub_path = os.path.join(
            asset_root_path, dept, "pub", "maya", "scenes"
        )
        work_path = os.path.join(
            asset_root_path, dept, "work", "maya", "scenes"
        )

        version_nums = []
        work_files = os.listdir(work_path)
        for file_name in work_files:
            match = re.search(r"v(\d{3})", file_name)
            if match:
                version_nums.append(int(match.group(1)))

        if version_nums:
            last_version = max(version_nums)+1
        else:
            last_version = 1 

        maya_ascii_work_path = os.path.join(
            work_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
        )
        maya_ascii_pub_path = os.path.join(
            pub_path, f"{asset_name}_{dept}_v{last_version:03d}.ma"
        )
        cmds.file(rename=maya_ascii_work_path)
        cmds.file(save=True, type="mayaAscii")
        shutil.copy2(maya_ascii_work_path, maya_ascii_pub_path)