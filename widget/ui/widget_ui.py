try :
    from PySide2.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QDialog, QLineEdit, QFrame, QToolButton
    from PySide2.QtGui import QPixmap, QBitmap, QPainter, QPainterPath, QPainterPath, QPainter, QPainterPath
    from PySide2.QtWidgets import QHeaderView, QAbstractItemView
    from PySide2.QtCore import Qt
    from shiboken2 import wrapInstance
except Exception :
    from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QDialog, QLineEdit, QFrame, QToolButton
    from PySide6.QtGui import QPixmap, QBitmap, QPainter, QPainterPath, QPainterPath, QPainter, QPainterPath
    from PySide6.QtWidgets import QHeaderView, QAbstractItemView
    from PySide6.QtCore import Qt
    from shiboken6 import wrapInstance
    
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import requests
from widget.event.widget_event_handler import clicked_get_asset_btn
from save_as.main import run as save_as_run
from publisher.main import run as publish_run

import os
import sys
from io import BytesIO
from systempath import SystemPath
from shotgridapi import ShotgridAPI

root_path = SystemPath().get_root_path()
sg = ShotgridAPI().shotgrid_connector()

#path = ""

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class CustomUI(QWidget):
    def __init__(self, path=None, ct=None):

        self.current_widget = None  

        if path !=None :
            self.path=path
        
        super().__init__()
        print("*"*30)
        self.setFixedWidth(350)
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
                self.status = ct.status
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

        taskinfo_label = QLabel("[TASK INFO]")
        taskinfo_label.setStyleSheet("font-size: 11pt; padding-bottom: 5px;")

        projectname_label = QLabel(f"Project : {self.project_name}")
        contentname_label = QLabel(f"Task : {self.content}")
        step_label = QLabel(f"Dept : {self.step}")
        h_line0 = QFrame() # 구분선0
        h_line0.setFrameShape(QFrame.HLine)
        h_line0.setFrameShadow(QFrame.Sunken)
        get_asset_label = QLabel("[ASSET LIBRARY]")
        get_asset_label.setStyleSheet("font-size: 11pt;padding-bottom: 5px;")
        get_asset_button = QPushButton("GET ASSETS")
        get_asset_button.setMaximumWidth(320)
        get_asset_button.clicked.connect(clicked_get_asset_btn)
        
        print(f"*** {self.entity_type}")
        if self.entity_type == "assets" :
            self.entity_type = "Asset"
            parent_label = QLabel(f"Asset type : {self.entity_parent}")
            child_label = QLabel(f"Asset : {self.entity_name}")

        elif self.entity_type == "seq" :
            self.entity_type = "Shot"
            parent_label = QLabel(f"Seq : {self.entity_parent}")
            child_label = QLabel(f"Shot : {self.entity_name}")
        else : 
            parent_label = QLabel(f"parent : {self.entity_parent}")
            child_label = QLabel(f"baby : {self.entity_name}")
            
        
        # ct 받아오기가 필요함
        self.toggle_button = QPushButton(self.status, self)
        self.toggle_button.setStyleSheet("right-padding: 5px;")
        self.toggle_button.setFixedSize(40, 20)
        self.toggle_button.setCheckable(True)  # 버튼을 체크 가능하게 설정
        self.toggle_button.setChecked(False)# 초기 상태를 False로 설정
        
        self.toggle_button_color()
        
        if self.status == "wtg" :
            self.change_status = "ip"
        elif self.status == "ip" :
            self.change_status = "wtg"
 
        # 토글 버튼이 눌리면 상태 변경
        self.toggle_button.toggled.connect(self.on_toggle)
        
        pb_layout = QHBoxLayout()
        pb_layout.addWidget(contentname_label)
        pb_layout.addWidget(self.toggle_button)
        
        h_line1 = QFrame() # 구분선1
        h_line1.setFrameShape(QFrame.HLine)
        h_line1.setFrameShadow(QFrame.Sunken)

        self.colleagueinfo_label = QLabel("[COLLEAGUE INFO]")
        self.colleagueinfo_label.setStyleSheet("font-size: 11pt; padding-bottom: 5px;")

        colleague_list = []
        colleague_list = self.get_colleague_info()

        colleague_layout = QGridLayout()
        
        for row, item in enumerate(colleague_list):
            thumb_label = QLabel(self)
            thumb_label.setFixedSize(30, 30)
            thumb_label.setScaledContents(True)
        
            pixmap = QPixmap()
            image_data = requests.get(item[3]).content if item[3] else None # url 이미지 유효성 확인. 아니면 None 리턴

            if image_data:
                pixmap.loadFromData(image_data)      
            else:
                pixmap = QPixmap(f"{root_path}/elements/no_assignee.png")
                if not pixmap.isNull():
                    pass
                else:
                    thumb_label = QLabel("")
                    thumb_label.setAlignment(Qt.AlignCenter)

            thumb_label.setPixmap(pixmap)
            #pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            #pixmap = pixmap.copy((pixmap.width()-20)//2, (pixmap.height()-20)//2, 20, 20)
            
            pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pixmap = self.circular_pixmap(pixmap, 30)

            thumb_label.setPixmap(pixmap) 
            thumb_label.setStyleSheet('padding-left : 5px')

            text_label = QLabel(f"{str(item[0])} : {str(item[1])}")

            colleague_layout.addWidget(thumb_label, row, 0)
            colleague_layout.addWidget(text_label, row, 1)

        h_line2 = QFrame() #구분선 2
        h_line2.setFrameShape(QFrame.HLine)
        h_line2.setFrameShadow(QFrame.Sunken)
        
        note_title, note_body, creator_kor_name, version_name, attachment_url = self.get_notes_infos()

        noteinfo_label = QLabel("[RECENT NOTE]")
        noteinfo_label.setStyleSheet("font-size: 11pt;")
        notedetail_layout = QVBoxLayout()
        creatorname_label = QLabel(f"Note from {creator_kor_name}")
        versionname_label = QLabel(f"version : {version_name}")
        notetitle_label = QLabel(f"title : {note_title}")
        notebody_label = QLabel(f"context : {note_body}")
        notebody_label.setWordWrap(True)
        notebody_label.setMaximumWidth(320)
        notedetail_layout.addWidget(creatorname_label)
        notedetail_layout.addWidget(versionname_label)
        notedetail_layout.addWidget(notetitle_label)
        notedetail_layout.addWidget(notebody_label)
        notebody_label.setStyleSheet("border-bottom:5px")
        
        # 세 번째 줄 (100x100 QPixmap)
        noteimage_label = QLabel()
        pixmap2 = self.load_pixmap_from_url(attachment_url)
        pixmap2 = pixmap2.scaled(320, 180, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        #noteimage_label.setStyleSheet('border-style: solid; border-width: 2px; border-color: white; padding-left : 5px') # stylesheet
        noteimage_label.setPixmap(pixmap2)
        
        # 메인 레이아웃
        note_layout = QVBoxLayout()
        # note_layout.addWidget(noteinfo_label)
        # note_layout.addWidget(creatorthumb_label)
        # note_layout.addWidget(creatorname_label)
        note_layout.addLayout(notedetail_layout)
        note_layout.addWidget(noteimage_label)

        h_line3 = QFrame() # 구분선 
        h_line3.setFrameShape(QFrame.HLine)
        h_line3.setFrameShadow(QFrame.Sunken)
        # h_line3.setStyleSheet("padding-bottom: 10px;")
        self.button1 = QPushButton("Save As")
        self.button2 = QPushButton("Publish")
        
        layout = QVBoxLayout()

        label_layout = QVBoxLayout()
        label_layout.addWidget(taskinfo_label)
        label_layout.addWidget(projectname_label)
        label_layout.addWidget(step_label)
        label_layout.addWidget(parent_label)
        label_layout.addWidget(child_label)
        label_layout.addLayout(pb_layout)
        label_layout.addWidget(h_line0)
        label_layout.addWidget(get_asset_label)
        label_layout.addWidget(get_asset_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        layout.addLayout(label_layout)
        layout.addWidget(h_line1)
        layout.addWidget(self.colleagueinfo_label)
        layout.addLayout(colleague_layout)
        layout.addWidget(h_line2)
        layout.addWidget(noteinfo_label)
        layout.addLayout(note_layout)
        #layout.addLayout(commentBox_layout)
        layout.addWidget(h_line3)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

        self.button1.clicked.connect(self.on_click_saveas)
        self.button2.clicked.connect(self.on_click_publish)

    def on_toggle(self, checked):
        if checked :
            self.toggle_button.setText(self.change_status)
            sg.update("Task", self.id, {"sg_status_list": self.change_status})
        else:
            self.toggle_button.setText(self.status)
            sg.update("Task", self.id, {"sg_status_list": self.status})
            
        self.toggle_button_color()
    
    def toggle_button_color(self) :
        if self.toggle_button.text() == "wtg" :
            self.toggle_button.setStyleSheet("color : skyblue;")
        elif self.toggle_button.text() == "ip" :
            self.toggle_button.setStyleSheet("color : pink;")
    
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
    
    def load_pixmap_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            return image
        except Exception as e:
            image = QPixmap(f"{root_path}/elements/no_image.jpg")
            # if type == "human" :
            #     image = QPixmap(f"{root_path}/elements/no_assignee.png")
            # elif type == "note" :
            #     image = QPixmap(f"{root_path}/elements/no_image.jpg")
            return image

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
    

    def get_notes_infos(self) :
        self.id  # task id 
        note = sg.find_one(
            "Note",
            [["tasks", "is", {"type": "Task", "id": self.id}]],
            ["id", "subject", "content", "created_by", "created_at", "note_links", "attachments"],
            order=[{"field_name": "created_at", "direction": "desc"}]
        )

        if not note :
            note_title = ""
            note_body = ""
            creator_kor_name = ""
            version_name = ""
            creator_thumb = ""
            attachment_url = ""

        else : 
            note_id = note['id']
            note_title = note['subject']
            note_body = note['content']
            #creator_name = note['created_by']['name']
            creator_id = note['created_by']['id']
            creator_kor_name = sg.find_one("HumanUser", [["id", "is", creator_id]], ["sg_korean_name"])['sg_korean_name']
            #creator_kor_name = creator_info['sg_korean_name']
            linked_infos = note['note_links']
            for link in linked_infos :
                if link['type'] == 'Version' :
                    version_id = link['id']
                    version_name = link['name']

            if note["attachments"]:
                for attachment in note["attachments"]:
                    attachment_id = attachment["id"]
                    
            attachment_data = sg.find_one(
                "Attachment",
                [["id", "is", attachment_id]],
                ["id", "this_file", "name"]
            )
            if attachment_data :
                attachment_url = attachment_data['this_file']['url']

        #print(f"note id : {note_id}\nnote_title : {note_title}\nnote_body : {note_body}\ncreator_kor_name : {creator_kor_name}\nversion_name = {version_name}\ncreator_thumb = {creator_thumb}\nattachment_url : {attachment_url}")

        return note_title, note_body, creator_kor_name, version_name, attachment_url
    
    def on_click_statuschange(self) :
        print("changechange")
        
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

    def on_click_saveas(self):
        save_as_run()

    def on_click_publish(self):
        publish_run()

def add_custom_ui_to_tab(path, ct=None):
    workspace_control_name = "CustomTabUIWorkspaceControl"
    
    if cmds.workspaceControl(workspace_control_name, query=True, exists=True):
        print(f"WorkspaceControl '{workspace_control_name}' already exists.")
        cmds.deleteUI(workspace_control_name) # 기존 패널 삭제
    else : 
        pass
    cmds.workspaceControl(workspace_control_name, label="Save / Publish", retain=False, dockToControl=("AttributeEditor", "right"), wp="fixed", width=200, collapse=True)
    control_ptr = omui.MQtUtil.findControl(workspace_control_name)
    control_widget = wrapInstance(int(control_ptr), QWidget)

    if "custom_ui" not in locals() or custom_ui is None:
        custom_ui = CustomUI(path, ct)
        control_widget.layout().addWidget(custom_ui)
        cmds.evalDeferred(lambda: cmds.workspaceControl(workspace_control_name, edit=True, collapse=False))
    else :
        if custom_ui.current_widget is not None:
            custom_ui.current_widget.close()
            custom_ui.current_widget.deleteLater()
            custom_ui.current_widget = None  

            custom_ui = CustomUI(path, ct)
            control_widget.layout().addWidget(custom_ui)

# Call the function to add the custom UI
#add_custom_ui_to_tab(path)