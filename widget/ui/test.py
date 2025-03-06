from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

import sys, os

# 절대 경로 추가
# publisher_ui_path = os.path.abspath("/home/rapa/gitkraken/maya_usd/publisher/ui")
# sys.path.append(publisher_ui_path)

# from main import show_ui  # 이제 main.py에서 show_ui 함수를 임포트할 수 있습니다

# 이후, 버튼 클릭 시 show_ui를 실행하는 로직

from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class TestUI(QWidget):
    def __init__(self):
        super().__init__()

        # 버튼 생성
        self.button = QPushButton("Show UI", self)
        self.button.clicked.connect(self.on_button_click)  # 버튼 클릭 시 핸들러 연결

def get_maya_main_window():
    """Returns the Maya main window as a QWidget."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CustomUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomUI, self).__init__(parent)
        
        self.task_name = "None"
        self.dept_name = "None"

        # Create Labels, LineEdits, and Buttons
        self.label1 = QtWidgets.QLabel(f"Task Name : {self.task_name}")
        self.label2 = QtWidgets.QLabel(f"Dept : {self.dept_name}")
        
        self.button1 = QtWidgets.QPushButton("Save As")
        self.button2 = QtWidgets.QPushButton("Publish")

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        # Horizontal layout for buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Set the fixed height of the UI to 100
        self.setFixedHeight(100)
        self.setFixedWidth(300)

        # Connect buttons to actions
        self.button1.clicked.connect(self.show_save_as_popup)
        self.button2.clicked.connect(self.show_publish_popup)

    def show_save_as_popup(self):
        """Displays the 'Save As' popup dialog."""
        save_as_dialog = SaveAsDialog(self)
        save_as_dialog.exec_()  # Show the dialog modally

    def show_publish_popup(self):
        """Displays the 'Publish' popup dialog."""
        publish_dialog = PublishDialog(self)
        publish_dialog.exec_()  # Show the dialog modally

class SaveAsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SaveAsDialog, self).__init__(parent)
        
        self.setWindowTitle("Save As")
        
        # Create Labels and LineEdits for Save As
        self.label1 = QtWidgets.QLabel("Save As Name 1:")
        self.line_edit1 = QtWidgets.QLineEdit()
        
        self.label2 = QtWidgets.QLabel("Save As Name 2:")
        self.line_edit2 = QtWidgets.QLineEdit()

        # Button
        self.save_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        
        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line_edit2)
        
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect buttons to actions
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.reject)

    def save(self):
        """Handle save button action."""
        name1 = self.line_edit1.text()
        name2 = self.line_edit2.text()
        print(f"Save As - Name 1: {name1}, Name 2: {name2}")
        self.accept()  # Close the dialog

class PublishDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PublishDialog, self).__init__(parent)
        
        self.setWindowTitle("Publish")
        
        # Create Labels and LineEdits for Publish
        self.label1 = QtWidgets.QLabel("Publish Name 1:")
        self.line_edit1 = QtWidgets.QLineEdit()
        
        self.label2 = QtWidgets.QLabel("Publish Name 2:")
        self.line_edit2 = QtWidgets.QLineEdit()

        # Button
        self.publish_button = QtWidgets.QPushButton("Publish")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        
        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line_edit2)
        
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.publish_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect buttons to actions
        self.publish_button.clicked.connect(self.publish)
        self.cancel_button.clicked.connect(self.reject)

    def publish(self):
        """Handle publish button action."""
        name1 = self.line_edit1.text()
        name2 = self.line_edit2.text()
        print(f"Publish - Name 1: {name1}, Name 2: {name2}")
        #show_ui()
        self.accept()  # Close the dialog

# Create and add custom UI to Maya's right-side tab
def add_custom_ui_to_tab():
    workspace_control_name = "CustomTabUIWorkspaceControl"
    
    if not cmds.workspaceControl(workspace_control_name, q=True, exists=True):
        # Create a workspace control (dockable UI)
        cmds.workspaceControl(workspace_control_name, label="Save / Publish", retain=False, dockToControl=("AttributeEditor", "right"))

    # Get the pointer for the workspace control and wrap it
    control_ptr = omui.MQtUtil.findControl(workspace_control_name)
    control_widget = wrapInstance(int(control_ptr), QtWidgets.QWidget)

    # Create an instance of CustomUI and add it to the workspace control
    custom_ui = CustomUI()
    control_widget.layout().addWidget(custom_ui)

# Call the function to add the custom UI
add_custom_ui_to_tab()