from PySide2.QtWidgets import QToolButton, QLineEdit, QDialog, QPushButton, QHBoxLayout, QVBoxLayout
import maya.cmds as cmds
import os

class CustomDialog(QDialog):
    def __init__(self, path, is_dir, is_created, ct):
        super().__init__()

        self.is_dir = is_dir
        self.is_created = is_created
        #self.ct = ct
        self.file_name = ct.set_file_name()
        # Set up the dialog layout
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
        line_edit_text = self.line_edit.text()
        ext = self.switch.text()
        run_path = f"{path}/{line_edit_text}{ext}"
        print(run_path)

        if self.is_dir :
            pass
        else :
            os.makedirs(path)
            print(f"'{path}' 경로가 생성되었습니다.")
            self.is_dir = False
            
        cmds.file(rename=run_path)
        if ext == ".ma" :
            save_type = "mayaAscii"
        elif ext == ".mb" :
            save_type = "mayaBinary"

        cmds.file(save=True, type=save_type)
        print(f"씬 파일 '{run_path}'가 저장되었습니다.")
        self.is_created = True
        print(self.ct.entity_id, self.ct.task_id, self.ct.proj_id)

        cmds.file(run_path, open=True) #################################### 여는 방법 수정
        print(f"{run_path}가 열립니다.")
        self.dialog_flag = False
        self.accept()

    def on_click_exit(self) :
        print("종료")
        self.dialog_flag = False
        self.accept()