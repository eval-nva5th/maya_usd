import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
import socketio
import os
import threading

try : 
    from shiboken2 import wrapInstance
    from PySide2 import QtWidgets, QtCore
except Exception :
    from shiboken6 import wrapInstance
    from PySide6 import QtWidgets, QtCore
    
import maya.cmds as cmds
import maya.OpenMayaUI as omui

workspace_control_name = "CustomTabUIWorkspaceControl"
new_workspace_name = "CustomTabUIforReload"

'''
mac의 경우 /Users/{username}/Library/Preferences/Autodesk/maya/scripts
에 해당 파일을 넣을 경우 원활하게 실행됩니다. 

'''
class ReloadUI(QtWidgets.QWidget):
    def __init__(self, message, local_path, parent=None):
        super(ReloadUI, self).__init__(parent)

        self.message = message
        self.local_path = local_path

        layout = QtWidgets.QVBoxLayout(self)
        
        self.label1 = QtWidgets.QLabel("New File Published!", self)
        layout.addWidget(self.label1)

        self.label2 = QtWidgets.QLabel(self.message)
        layout.addWidget(self.label2)
        
        self.button = QtWidgets.QPushButton("reload")
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_reload_clicked)

    def on_reload_clicked(self):
        self.reload_file()
        
    def reload_file(self):
        if not self.local_path:
            print("유효하지 않은 파일 경로입니다.")
            return
        
        references = cmds.ls(type='reference')
        for ref in references:
            try:
                ref_file = cmds.referenceQuery(ref, filename=True)
                if ref_file == self.file_path:
                    print(f"참조 파일을 리로드합니다: {self.file_path}")
                    cmds.file(self.file_path, loadReference=ref)
                    return
            except RuntimeError as e:
                print(e)
        
        print("해당 경로에 맞는 참조 파일을 찾을 수 없습니다.")

def create_workspace_with_ui(message, local_path):
    """ 메인 스레드에서 실행되도록 보장해야 함 """
    if not cmds.workspaceControl(workspace_control_name, query=True, exists=True):
        print(f"'{workspace_control_name}' 없음")
        return

    if not cmds.workspaceControl(new_workspace_name, query=True, exists=True):
        cmds.workspaceControl(
            new_workspace_name,
            label="RELOAD",
            retain=False,
            dockToControl=(workspace_control_name, "top"),
            uiScript="add_ui_to_workspace()"  # UI 추가 시 호출됨
        )
    
    add_ui_to_workspace(message, local_path)  # UI 추가 실행

def add_ui_to_workspace(message, local_path):
    ptr = omui.MQtUtil.findControl(new_workspace_name)
    
    if ptr:
        workspace_widget = wrapInstance(int(ptr), QtWidgets.QWidget)

        if not workspace_widget.layout():
            layout = QtWidgets.QVBoxLayout(workspace_widget)
        else:
            layout = workspace_widget.layout()
        
        ui = ReloadUI(message, local_path)
        layout.addWidget(ui)
    else:
        pass

sio = socketio.Client()

@sio.event
def connect():
    print("ShotGrid Webhook Server Connected")

@sio.event
def disconnect():
    print("ShotGrid Webhook Server Disonnected")

@sio.on("shotgrid_notification")
def on_notification(data):
   
    message_dict = data.get("message_dict", "Someone published")
    project_name = message_dict['project_name']
    published_file_name = message_dict['published_file_name']
    
    created_by = message_dict['created_by']
    created_at = message_dict['created_at']
    local_path = message_dict['local_path']
    
    message_text = f"{created_by} published {project_name} - {published_file_name} ({created_at})"

    os.system(f'notify-send "ShotGrid Notice" "{message_text}"')
    maya.utils.executeInMainThreadWithResult(create_workspace_with_ui, message_text, local_path)
    
def connect_to_server():
    print("Client Server Running")
    try:
        sio.connect("http://192.168.5.18:5000")
        sio.wait()
    except Exception as e:
        print(f"Server connect failed: {e}")

def run_client_in_thread():
    thread = threading.Thread(target=connect_to_server)
    thread.daemon = True
    thread.start()

run_client_in_thread()
