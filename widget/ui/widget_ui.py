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
from widget.event.widget_event_handler import publish_playblast_run

import os
import sys
from io import BytesIO
from systempath import SystemPath
from shotgridapi import ShotgridAPI

root_path = SystemPath().get_root_path()
sg = ShotgridAPI().shotgrid_connector()

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class SideWidget(QWidget):
    
    def __init__(self, path=None, ct=None):
        '''
        사이드 위젯 UI 생성
        1. 태스크 정보 : 프로젝트 이름, 디파트먼트, ([에셋 타입, 에셋이름] || [시퀀스, 샷이름]),  태스크이름, status(실시간 변경 가능)
        2. 에셋 라이브러리
        3. Entity에 연관된 아티스트 정보 (이름, 디파트먼트, 이미지)
        4. 해당 Task에 붙은 최신 Note 정보 (제목, 내용, 작성자, 버전이름, 이미지) 
        '''

        if path !=None :
            self.path=path
        
        super().__init__()
        self.setFixedWidth(350)
        
        if ct is not None:
            '''
            ct : CustomTask 객체
            해당 객체가 파라미터로 잘 들어왔다면 이 객체의 속성을 이용하여 값을 구성한다. 
            '''
            if hasattr(ct, 'id') and hasattr(ct, 'entity_id'):
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
        
        h_line0 = QFrame()
        h_line0.setFrameShape(QFrame.HLine)
        h_line0.setFrameShadow(QFrame.Sunken)
        get_asset_label = QLabel("[ASSET LIBRARY]")
        get_asset_label.setStyleSheet("font-size: 11pt;padding-bottom: 5px;")
        get_asset_button = QPushButton("GET ASSETS")
        get_asset_button.setMaximumWidth(320)
        get_asset_button.clicked.connect(clicked_get_asset_btn)
        
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
            
        self.toggle_button = QPushButton(self.status, self)
        self.toggle_button.setFixedSize(40, 20)
        self.toggle_button.setCheckable(True)  
        self.toggle_button.setChecked(False)
        self.toggle_button.setEnabled(True)
        if self.toggle_button.text() == "fin" :
            self.toggle_button.setEnabled(False)
            
        self.toggle_button_color()
        
        if self.status == "wtg" :
            self.change_status = "ip"
        elif self.status == "ip" :
            self.change_status = "wtg"

        self.toggle_button.toggled.connect(self.on_toggle)
        
        pb_layout = QHBoxLayout()
        pb_layout.addWidget(contentname_label)
        pb_layout.addWidget(self.toggle_button)
        
        h_line1 = QFrame()
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
            pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pixmap = self.circular_pixmap(pixmap, 30) # 원형 이미지로 변환

            thumb_label.setPixmap(pixmap) 
            thumb_label.setStyleSheet('padding-left : 5px')

            text_label = QLabel(f"{str(item[0])} : {str(item[1])}")

            colleague_layout.addWidget(thumb_label, row, 0)
            colleague_layout.addWidget(text_label, row, 1)

        h_line2 = QFrame() #구분선 2
        h_line2.setFrameShape(QFrame.HLine)
        h_line2.setFrameShadow(QFrame.Sunken)
        
        # 노트의 정보를 가져옴
        note_title, note_body, creator_kor_name, version_name, attachment_url = self.get_notes_infos()

        noteinfo_label = QLabel("[RECENT NOTE]")
        noteinfo_label.setStyleSheet("font-size: 11pt;")
        notedetail_layout = QVBoxLayout()
        creatorname_label = QLabel(f"from {creator_kor_name}")
        versionname_label = QLabel(f"file info : {version_name}")
        notetitle_label = QLabel(f"<{note_title}>")
        notebody_label = QLabel(f"note : {note_body}")
        notebody_label.setWordWrap(True)
        notebody_label.setMaximumWidth(320)
        notedetail_layout.addWidget(creatorname_label)
        notedetail_layout.addWidget(versionname_label)
        notedetail_layout.addWidget(notetitle_label)
        notedetail_layout.addWidget(notebody_label)
        notebody_label.setStyleSheet("border-bottom:5px")
        
        noteimage_label = QLabel()
        pixmap2 = self.load_pixmap_from_url(attachment_url)
        pixmap2 = pixmap2.scaled(320, 180, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        noteimage_label.setPixmap(pixmap2)
        
        # 메인 레이아웃
        note_layout = QVBoxLayout()
        note_layout.addLayout(notedetail_layout)
        note_layout.addWidget(noteimage_label)

        h_line3 = QFrame() 
        h_line3.setFrameShape(QFrame.HLine)
        h_line3.setFrameShadow(QFrame.Sunken)
        
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
        layout.addWidget(h_line3)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

        self.button1.clicked.connect(self.on_click_saveas)
        self.button2.clicked.connect(self.on_click_publish)

    def on_toggle(self, checked):
        '''
        버튼 클릭시 status 실시간 변경기능. ip - wtg 대응
        '''
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
        # 이미지 원형으로 만들기
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
        '''
        샷그리드 내 이미지들을 받아올 때 사용하는 함수. url의 유효성을 검사 후 존재할 시 이미지 반환, 없을시 no_image 출력. 
        '''
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            return image
        except Exception as e:
            image = QPixmap(f"{root_path}/elements/no_image.jpg")
            return image

    def get_colleague_info(self) :
        '''
        SG 내 태스크에 할당된 아티스트 정보를 가져오는 함수
        리스트 형식으로 반환
        '''
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
        '''
        SG 내 태스크에 붙은 노트 정보를 가져오는 함수. 제일 최신순으로 하나를 가져옴.
        제목, 내용, 작성자, 버전이름, 이미지 url을 반환
        '''
        
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
            attachment_url = ""

        else : 
            note_id = note['id']
            note_title = note['subject']
            note_body = note['content']
            creator_id = note['created_by']['id']
            creator_kor_name = sg.find_one("HumanUser", [["id", "is", creator_id]], ["sg_korean_name"])['sg_korean_name']
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

        return note_title, note_body, creator_kor_name, version_name, attachment_url

    def on_click_saveas(self):
        # save_as 실행 함수
        save_as_run(self.ct)

    def on_click_publish(self):
        #playblast 실행 함수 -> 그 후 퍼블리시 진행
        publish_playblast_run(self, self.ct)

def add_widget_to_tab(path, ct=None):
    '''
    마야 내 탭 위젯 추가 실행 함수. 위치는 AttributeEditor 오른쪽에 고정
    로더에서 파일을 열면 관련 태스크 정보들이 붙은 위젯이 생성됨.
    파일을 열 때마다 탭 위젯이 생성되어, 기존에 있는지 탐색하고 있다면 삭제 후 새로 생성함.
    '''
    workspace_control_name = "CustomTabUIWorkspaceControl"
    
    if cmds.workspaceControl(workspace_control_name, query=True, exists=True):
        print(f"WorkspaceControl '{workspace_control_name}' 이미 존재함")
        cmds.deleteUI(workspace_control_name) # 기존 패널 삭제
    else : 
        pass
    cmds.workspaceControl(workspace_control_name, label="Save / Publish", retain=False, dockToControl=("AttributeEditor", "right"), wp="fixed", width=200, collapse=True)
    control_ptr = omui.MQtUtil.findControl(workspace_control_name)
    control_widget = wrapInstance(int(control_ptr), QWidget)

    if "side_widget" not in locals() or side_widget is None:
        side_widget = SideWidget(path, ct)
        control_widget.layout().addWidget(side_widget)
        cmds.evalDeferred(lambda: cmds.workspaceControl(workspace_control_name, edit=True, collapse=False))
    else :
        if side_widget.current_widget is not None:
            side_widget.current_widget.close()
            side_widget.current_widget.deleteLater()
            side_widget.current_widget = None  

            side_widget = SideWidget(path, ct)
            control_widget.layout().addWidget(side_widget)
