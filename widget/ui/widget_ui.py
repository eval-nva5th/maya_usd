from PySide2.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QDialog, QLineEdit, QFrame
from PySide2.QtGui import QPixmap, QBitmap, QPainter, QPainterPath, QPainterPath, QPainter, QPainterPath
from PySide2.QtWidgets import QHeaderView, QAbstractItemView
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import requests

import sys
import os

from importlib import reload

publisher_ui_path = os.path.abspath("/home/rapa/gitkraken/maya_usd/save_as")
sys.path.append(publisher_ui_path)

import main   # 이제 main.py에서 show_ui 함수를 임포트할 수 있습니다

import shotgun_api3

# ShotGrid 서버 정보
sg_url = "https://hi.shotgrid.autodesk.com/"
script_name = "Admin_SY"
api_key = "kbuilvikxtf5v^bfrivDgqhxh"

# ShotGrid API 연결
sg = shotgun_api3.Shotgun(sg_url, script_name, api_key)

path = ""

def get_maya_main_window():
    """Returns the Maya main window as a QWidget."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class CustomUI(QWidget):
    def __init__(self, path=None, ct=None):
        if path !=None :
            self.path=path
        
        super().__init__()
        print("*"*30)

        print("여기서부터 custom UI 생성을 드가자")
        if ct is not None:
            if hasattr(ct, 'id') and hasattr(ct, 'entity_id'):
                print(f"ct.id: {ct.id}, ct.entity_id: {ct.entity_id}, ct.proj_name = {ct.project_name}, {ct.content}, {ct.entity_type}, {ct.entity_name}")
                self.id = ct.id
                self.entity_id = ct.entity_id
                self.project_name = ct.project_name
                self.content = ct.content
                self.entity_type = ct.entity_type
                self.entity_name = ct.entity_name
                self.entity_parent = ct.entity_parent
                self.step = ct.step
            else:
                print("ct attribute issues")
        else:
            print("ct가 nonetype임")
            self.project_name = ""
            self.content = ""
            self.entity_type = ""
            self.entity_name = ""
            self.entity_parent = ""
            self.step = ""

        self.label0 = QLabel("TASK INFO")
        self.label0.setStyleSheet("font-size: 11pt;")
        # Create Labels, LineEdits, and Buttons
        self.label1 = QLabel(f"Project : {self.project_name}")
        self.label2 = QLabel(f"Task : {self.content}")
        self.label3 = QLabel(f"Dept : {self.step}")

        if self.entity_type == "assets" :
            self.entity_type = "Asset"
            self.label4 = QLabel(f"Asset type : {self.entity_parent}")
            self.label5 = QLabel(f"Asset : {self.entity_name}")

        if self.entity_type == "seq" :
            self.entity_type = "Shot"
            self.label4 = QLabel(f"Seq : {self.entity_parent}")
            self.label5 = QLabel(f"Shot : {self.entity_name}")

        else : 
            self.label4 = QLabel(f"parent : {self.entity_parent}")
            self.label5 = QLabel(f"baby : {self.entity_name}")

        h_line1 = QFrame()
        h_line1.setFrameShape(QFrame.HLine)
        h_line1.setFrameShadow(QFrame.Sunken)

        self.colleagueLabel = QLabel("COLLEAGUE INFO")
        self.colleagueLabel.setStyleSheet("font-size: 11pt;")

        colleague_list = []
        colleague_list = self.get_colleague_info()
        print(colleague_list)

        colleague_layout = QGridLayout()
        
        for row, item in enumerate(colleague_list):
            thumb_label = QLabel(self)
            thumb_label.setFixedSize(30, 30)
            thumb_label.setScaledContents(True)
           
            pixmap = QPixmap()
            image_data = requests.get(item[3]).content if item[3] else None

            if image_data:
                pixmap.loadFromData(image_data)
                
            else:
                pixmap = QPixmap("/nas/eval/elements/no_assignee.png")
                if not pixmap.isNull():
                    pass
                else:
                    thumb_label = QLabel("")
                    thumb_label.setAlignment(Qt.AlignCenter)

            thumb_label.setPixmap(pixmap)
            # pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            # pixmap = pixmap.copy((pixmap.width()-30)//2, (pixmap.height()-30)//2, 30, 30)
            pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pixmap = self.circular_pixmap(pixmap, 30)
            thumb_label.setPixmap(pixmap)  # 기존 thumb_label 사용해야 함!
            thumb_label.setStyleSheet('border-radius: 15px; border: white;')

# 간단하게 원형 마스크 적용하기
            # region = QRegion(pixmap.rect(), QRegion.Ellipse)
            # thumb_label.setMask(region)

            text_label = QLabel(f"{str(item[0])} : {str(item[1])}")

            colleague_layout.addWidget(thumb_label, row, 0)
            colleague_layout.addWidget(text_label, row, 1)

        h_line2 = QFrame()
        h_line2.setFrameShape(QFrame.HLine)
        h_line2.setFrameShadow(QFrame.Sunken)
        
        self.label6 = QLabel("MessageBox :")
        self.label6.setStyleSheet("font-size: 11pt;")
        
        self.commentBox = QLabel("Lorem Ipsum")
        self.commentBox.setStyleSheet("border: 1px solid white;")
        self.commentBox.setFixedHeight(300)
        #self.commentBox.setFixedWidth(300)

        h_line3 = QFrame()
        h_line3.setFrameShape(QFrame.HLine)
        h_line3.setFrameShadow(QFrame.Sunken)

        #self.commentBox = QTextEdit()
        #self.commentBox.setFixedHeight(100)
        self.button1 = QPushButton("Save As")
        self.button2 = QPushButton("Publish")
        
        layout = QVBoxLayout()
        # Layout
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.label0)
        label_layout.addWidget(self.label1)
        label_layout.addWidget(self.label2)
        label_layout.addWidget(self.label3)
        label_layout.addWidget(self.label4)
        label_layout.addWidget(self.label5)

        commentBox_layout = QVBoxLayout()
        commentBox_layout.addWidget(self.label6)
        commentBox_layout.addWidget(self.commentBox)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        layout.addLayout(label_layout)
        layout.addWidget(h_line1)
        layout.addWidget(self.colleagueLabel)
        layout.addLayout(colleague_layout)
        layout.addWidget(h_line2)
        layout.addLayout(commentBox_layout)
        layout.addWidget(h_line3)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

        self.button1.clicked.connect(self.show_save_as_popup)
        self.button2.clicked.connect(self.show_publish_popup)

    def circular_pixmap(self, pixmap, size):
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        masked_pixmap = QPixmap(size, size)
        masked_pixmap.fill(Qt.transparent)

        painter = QPainter(masked_pixmap)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return masked_pixmap

    def get_colleague_info(self) :

        colleague_list = []
        if self.entity_type == "seq" :
            self.entity_type = "Shot"
        elif self.entity_type == "assets" :
            self.entity_type = "Asset"

        tasks = sg.find(
            "Task",
            [["entity", "is", {"type": self.entity_type, "id": self.entity_id}]], 
            ["id", "task_assignees", "step"]
        )

        for task in tasks:
            task_type = task["step"]["name"]
            assignees = task["task_assignees"]

            if assignees :
                assignees_id = assignees[0]['id']
                user_infos = sg.find_one("HumanUser",
                        [['id', 'is', assignees_id]],
                        ["image", "sg_korean_name"])
                kor_name = user_infos.get('sg_korean_name')
                thumb_url = user_infos.get('image')

            else:
                kor_name = "None"
                assignees_id = 0
                thumb_url = ""
            each_list = [task_type, kor_name, assignees_id, thumb_url]
            if len(each_list) == 4:
                colleague_list.append(each_list)

        return colleague_list

    def getClickedTaskObject(self, ct) :
        self.ct = ct
        return self.ct
    
    def update(self) :
        ct = self.ct
        if hasattr(ct, 'id') and hasattr(ct, 'entity_id'):
            print(f"ct.id: {ct.id}, ct.entity_id: {ct.entity_id}, ct.proj_name = {ct.project_name}, {ct.content}, {ct.entity_type}, {ct.entity_name}")
            self.project_name = ct.project_name
            self.content = ct.content
            self.entity_type = ct.entity_type
            self.entity_name = ct.entity_name
            self.entity_parent = ct.entity_parent
            self.step = ct.step

    def show_save_as_popup(self):
        """Displays the 'Save As' popup dialog."""
        # main.save_dialog = SaveAsDialog()
        # main.save_dialog.show()
        
    def show_publish_popup(self):
        """Displays the 'Publish' popup dialog."""
        publish_dialog = PublishDialog(self)
        publish_dialog.exec_()  # Show the dialog modally

class PublishDialog(QDialog):
    def __init__(self, parent=None):
        super(PublishDialog, self).__init__(parent)
        
        self.setWindowTitle("Publish")
        
        # Create Labels and LineEdits for Publish
        self.label1 = QLabel("Publish Name 1:")
        self.line_edit1 = QLineEdit()
        
        self.label2 = QLabel("Publish Name 2:")
        self.line_edit2 = QLineEdit()

        # Button
        self.publish_button = QPushButton("Publish")
        self.cancel_button = QPushButton("Cancel")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line_edit2)
        
        # Button layout
        button_layout = QHBoxLayout()
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
        self.accept()  # Close the dialog

# Create and add custom UI to Maya's right-side tab
def add_custom_ui_to_tab(path, ct=None):
    workspace_control_name = "CustomTabUIWorkspaceControl"
    
    if not cmds.workspaceControl(workspace_control_name, q=True, exists=True):
        # Create a workspace control (dockable UI)
        cmds.workspaceControl(workspace_control_name, label="Save / Publish", retain=False, dockToControl=("AttributeEditor", "right"))

    # Get the pointer for the workspace control and wrap it
    control_ptr = omui.MQtUtil.findControl(workspace_control_name)
    control_widget = wrapInstance(int(control_ptr), QWidget)

    # Create an instance of CustomUI and add it to the workspace control
    custom_ui = CustomUI(path, ct)
    control_widget.layout().addWidget(custom_ui)

# Call the function to add the custom UI
#add_custom_ui_to_tab(path)