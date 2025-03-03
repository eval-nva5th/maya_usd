try :
    from PySide6.QtWidgets import QLineEdit, QPushButton, QDialog
    from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QToolButton
except ImportError:
    try:
        from PySide2.QtWidgets import QLineEdit, QPushButton, QDialog
        from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QToolButton
        import maya.cmds as cmds
    except ImportError:
        raise ImportError("PySide6와 PySide2가 모두 설치되지 않았습니다. 설치 후 다시 실행해주세요.")
from shotgrid_user_task import UserInfo, TaskInfo

class CustomDialog(QDialog):
    def __init__(self, full_path, file_name):
        super().__init__()
        sg_url = "https://hi.shotgrid.autodesk.com/"
        script_name = "Admin_SY"
        api_key = "kbuilvikxtf5v^bfrivDgqhxh"
        self.user = UserInfo(sg_url, script_name, api_key)
        self.user_name = ""
        self.task_info = TaskInfo(sg_url, script_name, api_key)
        self.prefix_path = "/nas/eval/show"

        self.task_data_dict = []
        
        super().__init__()
        self.setWindowTitle("EVAL_LOADER")
        self.center_window()

        self.login_window = self.login_ui()
        self.setCentralWidget(self.login_window)

        # Set up the dialog layout
        # Create two LineEdits
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(file_name)
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
        
        self.create_button.clicked.connect(lambda: self.on_click_create(full_path))
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

    def on_click_create(self, full_path):
        line_edit_text = self.line_edit.text()
        ext = self.switch.text()
        run_path = f"{full_path}/{line_edit_text}{ext}"
        print(run_path)
        self.dialog_flag = False
        self.accept()  # Close the dialog

    def on_click_exit(self) :
        print("종료")
        self.dialog_flag = False
        self.accept()