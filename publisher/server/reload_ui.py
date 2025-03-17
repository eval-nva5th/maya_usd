
# import maya.cmds as cmds
# from shiboken2 import wrapInstance
# from PySide2 import QtWidgets, QtCore
# import maya.OpenMayaUI as omui

# workspace_control_name = "CustomTabUIWorkspaceControl"
# new_workspace_name = "CustomTabUIforReload"

# class ReloadUI(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(ReloadUI, self).__init__(parent)

#         # 레이아웃 생성
#         layout = QtWidgets.QVBoxLayout(self)

#         # 라벨 1
#         self.label1 = QtWidgets.QLabel("updated task : ", self)
#         layout.addWidget(self.label1)

#         # 라벨 2
#         self.label2 = QtWidgets.QLabel("updated pub file : ", self)
#         layout.addWidget(self.label2)

#         # 버튼
#         self.button = QtWidgets.QPushButton("reload")
#         layout.addWidget(self.button)

#         # 버튼 클릭 시 라벨 1, 2의 텍스트 변경
#         self.button.clicked.connect(self.update_labels)

#     def update_labels(self):
#         self.label1.setText("라벨 1: 변경됨!")
#         self.label2.setText("라벨 2: 업데이트 완료!")

# def create_workspace_with_ui():
#     """ CustomTabUIforReload 워크스페이스에 UI 추가 """
#     if cmds.workspaceControl(workspace_control_name, query=True, exists=True):
#         print(f"WorkspaceControl '{workspace_control_name}' already exists.")

#         # 새로운 워크스페이스를 기존 컨트롤 위쪽에 추가
#         if not cmds.workspaceControl(new_workspace_name, query=True, exists=True):
#             cmds.workspaceControl(
#                 new_workspace_name,
#                 label="RELOADreload",
#                 retain=False,
#                 dockToControl=(workspace_control_name, "top")
#             )

#         # MQtUtil을 사용하여 workspaceControl의 PySide2 위젯 가져오기
#         ptr = omui.MQtUtil.findControl(new_workspace_name)
#         if ptr:
#             workspace_widget = wrapInstance(int(ptr), QtWidgets.QWidget)

#             # PySide2 UI 추가
#             ui = ReloadUI()
#             ui.setParent(workspace_widget)
#             ui.setWindowFlags(QtCore.Qt.Widget)

#             # 레이아웃 설정
#             layout = QtWidgets.QVBoxLayout(workspace_widget)
#             layout.addWidget(ui)

#             print("✅ PySide2 UI가 'CustomTabUIforReload' workspaceControl에 추가되었습니다!")

# # 실행
# create_workspace_with_ui()