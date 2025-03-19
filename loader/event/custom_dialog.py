try :
    from PySide2.QtWidgets import QToolButton, QLineEdit, QDialog, QPushButton, QHBoxLayout, QVBoxLayout
except Exception :
    from PySide6.QtWidgets import QToolButton, QLineEdit, QDialog, QPushButton, QHBoxLayout, QVBoxLayout
import maya.cmds as cmds
import os, sys
from loader.core.add_new_task import UsdLoader
from widget.ui.widget_ui import add_custom_ui_to_tab

class CustomDialog(QDialog):
    def __init__(self, path, is_dir, is_created, ct):
        super().__init__()

        self.is_dir = is_dir
        self.is_created = is_created
        self.ct = ct
        self.entity_type = ct.entity_type
        self.entity_name = ct.entity_name
        self.base_path = ct.set_base_path()
        self.file_name = ct.set_file_name()
        self.project_name = ct.project_name
        self.dept = ct.step
        # Create two LineEdits
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(self.file_name)
        self.line_edit.setFixedWidth(300)
        self.switch = QToolButton(self)
        self.switch.setCheckable(True)

        self.switch.setText(".mb")
        self.switch.setStyleSheet("""
            QToolButton {
                background-color: #ccc;
                border-radius: 10px;
                padding: 5px;
                color: white;
                background-color : #a47864;
                            
            }
            QToolButton:checked {
                background-color: #6667AB;
            }
            QToolButton:!checked {
                background-color: #a47864;
            }
        """)

        self.switch.clicked.connect(self.on_toggle)

        self.create_button = QPushButton("Create", self)
        self.exit_button = QPushButton("Exit", self)
        
        self.create_button.clicked.connect(lambda: self.on_click_create(path))
        self.exit_button.clicked.connect(self.on_click_exit)

        text_layout = QHBoxLayout()
        text_layout.addWidget(self.line_edit)
        text_layout.addWidget(self.switch)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.exit_button)

        full_layout = QVBoxLayout()
        full_layout.addLayout(text_layout)
        full_layout.addLayout(button_layout)

        self.setLayout(full_layout)
        self.setWindowTitle("create new work file")
        
    def on_toggle(self):
        if self.switch.isChecked():
            self.switch.setText(".ma")
        else:
            self.switch.setText(".mb")

    def on_click_create(self, path):
        self.file_name = self.line_edit.text()
        ext = self.switch.text()
        

        if self.is_dir :
            pass
        
        else :
            open_path = UsdLoader.create_folders(self.base_path, self.dept) 
            self.is_dir = True
            add_custom_ui_to_tab(open_path, self.ct)
        
        if self.entity_type == "assets" :
            open_path = UsdLoader.load_model_reference(self.base_path, self.dept, self.file_name, ext, self.entity_name)
            add_custom_ui_to_tab(open_path, self.ct)
            
        elif self.entity_type == "seq" :
            open_path = UsdLoader.load_shot_reference(self.base_path, self.dept, self.file_name, ext, self.entity_name, self.project_name)
            add_custom_ui_to_tab(open_path, self.ct)
            
        else :
            print(f"SOMETHING WENT WRONG {self.entity_type}")
            

        self.dialog_flag = False # 필수
        self.accept() # 필수
        
        ######## main window 창도 꺼져야함.

    def on_click_exit(self) :
        print("종료")
        self.dialog_flag = False
        self.accept()