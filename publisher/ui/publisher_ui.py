try : 
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QToolButton
    from PySide2.QtWidgets import QVBoxLayout, QLabel, QLineEdit
    from PySide2.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
    from PySide2.QtWidgets import QMessageBox, QPlainTextEdit
    from PySide2.QtWidgets import QComboBox
    from PySide2 import QtCore
except Exception :
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QToolButton
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit
    from PySide6.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
    from PySide6.QtWidgets import QMessageBox, QPlainTextEdit
    from PySide6.QtWidgets import QComboBox
    from PySide6 import QtCore

import sys, os
import maya.cmds as cmds
from publisher.core.play_blast import PlayblastManager
from publisher.event.event_handler import publish
from save_as.event.event_handler import open_file_browser, save_file_as, on_version_click
from loader.core.video_player import VideoPlayer

class PublisherDialog(QMainWindow):
    playblast_done = QtCore.Signal(str) # Playblast 작업이 완료되었을 때 해당 시그널을 방출

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Publish")
        self.setGeometry(100, 100, 650, 1000)

        self.center_window()
        self.playblast_done.connect(self.play_video)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # maya open파일경로, 폴더이름, 파일이름
        file_path = cmds.file(q=True, sceneName=True) 
        folder_path = os.path.dirname(file_path)
        file_name_with_ext = os.path.basename(file_path)
        file_name, _ = os.path.splitext(file_name_with_ext)

        # 파일명 Label + LineEdit
        filename_container = QHBoxLayout()
        filename_label = QLabel("File name:")
        self.filename_input = QLineEdit(file_name)
        self.filename_input.setDisabled(True)
        self.version_btn = QToolButton()
        self.version_btn.setCheckable(True)
        self.version_btn.setText("version up")
        self.version_btn.setFixedSize(100, 30)

        # 파일 경로 Label + LineEdit
        filepath_container = QHBoxLayout()
        filepath_label = QLabel("File path:")
        self.filepath_input = QLineEdit(folder_path)
        self.filepath_input.setDisabled(True)
        #self.filepath_input = QLineEdit("/nas/eval/show")

        # 파일 타입 
        filetype_container = QHBoxLayout()
        filetype_label = QLabel("File of type:")
        self.format_combo = QComboBox()
        self.format_combo.addItems([".mb", ".ma"])  # 옵션 추가
        self.format_combo.setCurrentText(".mb")  # 기본값 설정
        self.usd_format_combo = QComboBox()
        self.usd_format_combo.addItems([".usd"])

        # Comment
        comment_container = QVBoxLayout()   
        comment_label = QLabel("Comment")
        self.plain_text_edit = QPlainTextEdit()
        self.plain_text_edit.setPlaceholderText("Write your comment here ......")

        # Preview
        preview_container = QVBoxLayout()
        preview_h_container = QHBoxLayout()
        self.preview_label = QLabel("Preview")
        self.preview_btn = QPushButton("Show")
        self.preview_frame = VideoPlayer("")

        # pub or not
        button_container = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        publish_btn = QPushButton("Publish")

        # Style Sheet
        filepath_label.setFixedWidth(80)
        filename_label.setFixedWidth(80)
        filetype_label.setFixedWidth(80)
        comment_label.setFixedHeight(30)
        self.plain_text_edit.setFixedHeight(250)
        self.preview_label.setFixedHeight(30)
        self.preview_frame.setFixedHeight(350)
        self.preview_frame.setStyleSheet("border:1px solid black;")
        cancel_btn.setFixedHeight(30)
        publish_btn.setFixedHeight(30)

        style = """
            color: white;  /* 글씨를 검정색으로 유지 */
            background-color:rgb(93, 93, 93);  /* 배경색 변경 (비활성화된 느낌 최소화) */
        """
        self.filename_input.setStyleSheet(style)
        self.filepath_input.setStyleSheet(style)

        # Event Handle
        cancel_btn.clicked.connect(self.close)
        publish_btn.clicked.connect(lambda: publish(self))
        self.preview_btn.clicked.connect(lambda : self.run_playblast(file_path, file_name))
        self.version_btn.clicked.connect(lambda: on_version_click(self, file_name))
        publish_btn.clicked.connect(lambda: save_file_as(self))
        publish_btn.clicked.connect(lambda: PlayblastManager(file_path, file_name).save_playblast_files())

        # layout
        filepath_container.addWidget(filepath_label)
        filepath_container.addWidget(self.filepath_input)

        filename_container.addWidget(filename_label)
        filename_container.addWidget(self.filename_input)
        filename_container.addWidget(self.version_btn)

        filetype_container.addWidget(filetype_label)
        filetype_container.addWidget(self.format_combo)
        filetype_container.addWidget(self.usd_format_combo)

        comment_container.addWidget(comment_label)
        comment_container.addWidget(self.plain_text_edit)

        preview_h_container.addWidget(self.preview_label)
        preview_h_container.addWidget(self.preview_btn)
        preview_container.addLayout(preview_h_container)
        preview_container.addWidget(self.preview_frame)

        button_container.addWidget(cancel_btn)
        button_container.addWidget(publish_btn)

        layout.addLayout(filepath_container)
        layout.addLayout(filename_container)
        layout.addLayout(filetype_container)
        layout.addLayout(comment_container)
        layout.addLayout(preview_container)
        layout.addLayout(button_container)
        central_widget.setLayout(layout)

    def run_playblast(self, file_path, file_name):
        # PlayblastManager(file_path, file_name).run_playblast()
        print ("쇼 버튼이 눌리고 있음.")
        output_file = PlayblastManager(file_path, file_name).run_playblast()
        print ("생성된 파일", output_file)

        print ("생성되었는지 안되었는지 파일 확인 중")
        self.worker = PlayblastChecker(output_file)
        self.worker.file_found.connect(lambda: self.play_video(output_file))  # file_found 시그널이 발생하면 play_video() 실행하도록 설정
        self.worker.start()

    def play_video(self, output_file):
        """ 기존 VideoPlayer 객체를 유지하면서 새로운 파일을 로드 """
        print(f"비디오 로딩 시작: {output_file}")
        if isinstance(self.preview_frame, VideoPlayer):
            # 기존 VideoPlayer 객체가 있으면 새로운 파일만 로드
            self.preview_frame.set_new_mov_file(output_file)
        else:
            # VideoPlayer가 아니면 새로 생성
            print("새로운 VideoPlayer 객체 생성")
            self.preview_frame = VideoPlayer(output_file)
            self.preview_frame.setFixedHeight(350)
            self.preview_frame.setStyleSheet("border:1px solid black;")

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

class PlayblastChecker(QtCore.QThread): # 플레이 블라스트 체크 클래스.
    file_found = QtCore.Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.output_file = file_path
    def run(self):
        while not os.path.exists(self.output_file):
            QtCore.QThread.msleep(500)  # 0.5초마다 확인

        self.file_found.emit(self.output_file)