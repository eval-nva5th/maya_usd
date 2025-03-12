from PySide2.QtWidgets import QMainWindow, QWidget, QPushButton, QToolButton
from PySide2.QtWidgets import QVBoxLayout, QLabel, QLineEdit
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QComboBox
from PySide2.QtCore import Qt

import maya.cmds as cmds
import sys, os, re
from save_as.event.event_handler import open_file_browser, save_file_as, on_version_click

class SaveAsDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save As")
        self.setGeometry(100, 100, 650, 200)

        self.center_window()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        file_path = cmds.file(q=True, sceneName=True) # maya에서 open한 모델 파일 패스.
        folder_path = os.path.dirname(file_path) # 이름 제외
        print ("folder_path", folder_path)

        file_name_with_ext = os.path.basename(file_path)  # "IronMan_model_v005.ma"
        file_name, _ = os.path.splitext(file_name_with_ext)  # 확장자 제거하여 "IronMan_model_v005"
        print ("filename", file_name)

        # 파일명 Label + LineEdit
        filename_container = QHBoxLayout()
        self.filename_label = QLabel("File name:", self)
        self.filename_input = QLineEdit(file_name,self)
        self.version_btn = QToolButton(self)
        self.version_btn.setCheckable(True)
        self.version_btn.setText("version up")
        self.version_btn.setFixedSize(100, 30)
        self.filename_input.setDisabled(True)

        # 파일 경로 Label + LineEdit
        filepath_container = QHBoxLayout()
        self.filepath_label = QLabel("File path:", self)
        self.filepath_input = QLineEdit(folder_path, self)
        self.browse_btn = QPushButton("Browse", self)
        self.filepath_input.setDisabled(True)

        # 파일 타입 
        filetype_container = QHBoxLayout()
        self.filetype_label = QLabel("File of type:", self)
        self.format_combo = QComboBox(self)
        self.format_combo.addItems([".mb", ".ma"])  # 옵션 추가
        self.format_combo.setCurrentText(".mb")  # 기본값 설정

        # 저장 여부 버튼
        button_container = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel", self)
        self.save_as_btn = QPushButton("Save As", self)

        # Style Sheet
        self.filepath_label.setFixedWidth(80)
        self.filename_label.setFixedWidth(80)
        self.filetype_label.setFixedWidth(80)

        self.browse_btn.setFixedSize(100, 30)
        self.save_as_btn.setFixedSize(100, 30)
        self.cancel_btn.setFixedSize(100, 30)

        style = """
            color: black;  /* 글씨를 검정색으로 유지 */
            background-color: #F0F0F0;  /* 배경색 변경 (비활성화된 느낌 최소화) */
        """
        self.filename_input.setStyleSheet(style)
        self.filepath_input.setStyleSheet(style)

        # 이벤트 처리
        self.browse_btn.clicked.connect(lambda: open_file_browser(self))
        self.save_as_btn.clicked.connect(lambda: save_file_as(self))
        self.version_btn.clicked.connect(lambda: on_version_click(self, file_name))
        self.cancel_btn.clicked.connect(self.close)

        # 레이아웃에 위젯 추가
        button_container.addStretch()
        button_container.addWidget(self.cancel_btn)
        button_container.addWidget(self.save_as_btn)

        filepath_container.addWidget(self.filepath_label)
        filepath_container.addWidget(self.filepath_input)
        filepath_container.addWidget(self.browse_btn)

        filename_container.addWidget(self.filename_label)
        filename_container.addWidget(self.filename_input)
        filename_container.addWidget(self.version_btn)

        filetype_container.addWidget(self.filetype_label)
        filetype_container.addWidget(self.format_combo)

        layout.addLayout(filepath_container)
        layout.addLayout(filename_container)
        layout.addLayout(filetype_container)
        layout.addLayout(button_container)
        central_widget.setLayout(layout)
    
    def center_window(self):
        screen_geometry = self.screen().geometry()  # 현재 창이 표시되는 화면의 전체 크기
        window_geometry = self.frameGeometry()  # 현재 창의 크기 정보

        # 화면 중앙 좌표 계산
        center_x = screen_geometry.width() // 2 - window_geometry.width() // 2
        center_y = screen_geometry.height() // 2 - window_geometry.height() // 2
        print(center_x, center_y)
        # 창 이동
        self.setGeometry(center_x, center_y, window_geometry.width(), window_geometry.height())        
        self.move(center_x, center_y)