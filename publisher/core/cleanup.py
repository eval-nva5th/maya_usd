import maya.cmds as cmds

def remove_unused_shaders():
    cmds.hyperShade(removeUnusedShaders=True)

def clean_unused_nodes():
    cmds.delete(cmds.ls(type="unknown"))
    cmds.delete(cmds.ls(type="displayLayer"))
    cmds.delete(cmds.ls(type="objectSet"))

def prepare_scene_for_export():
    all_nodes = cmds.ls(dag=True)
    export_nodes = cmds.ls(selection=True)
    
    # Export 대상이 아닌 노드 삭제
    for node in all_nodes:
        if node not in export_nodes:
            cmds.delete(node)

