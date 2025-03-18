import maya.cmds as cmds
from abc import ABC, abstractmethod

class USDExporter(ABC):
    """usd export시 필요한 옵션들을 받아오는 클래스"""
    def __init__(self, usd_publish_path, task_name, dept):
        super().__init__()
        self.usd_publish_path = usd_publish_path
        self.task_name = task_name
        self.dept = dept

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
    """model export 시 필요한 옵션들"""
    def get_export_options(self):
        return{
            "selection": True,
            "defaultUSDFormat":"usda",
            "rootPrimType": "Xform",
            "exportVisibility": 1,
            "mergeTransformAndShape":0,
            "defaultMeshScheme": "catmullClark",
            "shadingMode": "none",
            "exportInstances": 0,
            "exportBlendShapes": 0,
            "exportSkels": "none",
            "exportSkin": "none",
            "excludeExportTypes": ["Cameras", "Lights"],
        }

    def export(self):
        options = self.get_export_options()
        cmds.mayaUSDExport(
            file=self.usd_publish_path,
            **options
        )

class LookdevExportUSD(USDExporter):
    """lookdev export 시 필요한 옵션들"""
    def get_export_options(self):
        return{
            "selection": True,
            "defaultUSDFormat":"usda",
            "defaultPrim" : f"{self.task_name}_{self.dept}",
            "rootPrimType": "scope",
            "defaultMeshScheme": "catmullClark",
            "exportVisibility": 0,
            "exportUVs": 1,
            "exportDisplayColor": 0,
            "exportBlendShapes": 0,
            "exportMaterialCollections": 1,
            "exportAssignedMaterials":1,
            "excludeExportTypes": ["Meshes", "Cameras", "Lights"],
            "convertMaterialsTo":["UsdPreviewSurface", "MaterialX"],
            "exportInstances": 1,
            "exportSkels": "none",
            "exportSkin": "none"
        }

    def export(self):
        options = self.get_export_options()
        cmds.mayaUSDExport(
            file=self.usd_publish_path,
            **options
        )

class ShotExportUSD(USDExporter):
    """shot 작업자들 export 시 필요한 옵션들"""
    def get_export_options(self):
        return{
            "selection": True,
            "defaultUSDFormat":"usda",
            "rootPrimType": "scope",
            "defaultMeshScheme": "catmullClark",
            "exportVisibility": 1,
            "exportUVs": 1,
            "exportLights": 1,
            "exportDisplayColor": 1,
            "exportBlendShapes": 1,
            "exportMaterialCollections": 1,
            "exportAssignedMaterials":1,
            "convertMaterialsTo":["UsdPreviewSurface", "MaterialX"],
            "exportInstances": 1,
            "exportSkels": "auto",
            "exportSkin": "auto",
            "mergeTransformAndShape":1,
            "frameRange": (
                cmds.playbackOptions(q=True, minTime=True),
                cmds.playbackOptions(q=True, maxTime=True)
            ),
            "frameStride":1.0
        }

    def export(self):
        options = self.get_export_options()
        cmds.mayaUSDExport(
            file=self.usd_publish_path,
            **options
        )