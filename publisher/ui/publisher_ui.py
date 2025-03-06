try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit
    from PySide6.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
    from PySide6.QtWidgets import QMessageBox, QPlainTextEdit
    from PySide6.QtWidgets import QComboBox
except:
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
    from PySide2.QtWidgets import QVBoxLayout, QLabel, QLineEdit
    from PySide2.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
    from PySide2.QtWidgets import QMessageBox, QPlainTextEdit
    from PySide2.QtWidgets import QComboBox
import sys
from core.play_blast import PlayblastManager
from event.event_handler import publish

class PublisherDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Publish")
        self.setGeometry(100, 100, 650, 1000)

        self.center_window()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 파일명 Label + LineEdit
        filename_container = QHBoxLayout()
        filename_label = QLabel("File name:")
        self.filename_input = QLineEdit("file_name_input_v001")

        # 파일 경로 Label + LineEdit
        filepath_container = QHBoxLayout()
        filepath_label = QLabel("File path:")
        self.filepath_input = QLineEdit("/nas/eval/")

        # 파일 타입 
        filetype_container = QHBoxLayout()
        filetype_label = QLabel("File of type:")
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["Maya Binary", "Maya ASCII"])  # 옵션 추가
        self.format_combo.setCurrentText("Maya Binary")  # 기본값 설정

        # Comment
        comment_container = QVBoxLayout()   
        comment_label = QLabel("Comment")
        self.plain_text_edit = QPlainTextEdit()
        self.plain_text_edit.setPlaceholderText("Write your comment here ......")

        # Preview
        preview_container = QVBoxLayout()
        preview_label = QLabel("Preview")
        self.preview_frame = QLabel()

        # pub or not
        button_container = QHBoxLayout()
        cancel_btn = QPushButton("Cancel", self)
        publish_btn = QPushButton("Publish", self)

        # Style Sheet
        filepath_label.setFixedWidth(80)
        filename_label.setFixedWidth(80)
        filetype_label.setFixedWidth(80)
        comment_label.setFixedHeight(30)
        self.plain_text_edit.setFixedHeight(250)
        preview_label.setFixedHeight(30)
        self.preview_frame.setFixedHeight(350)
        self.preview_frame.setStyleSheet("border:1px solid black;")
        cancel_btn.setFixedHeight(30)
        publish_btn.setFixedHeight(30)


        # Event Handle
        cancel_btn.clicked.connect(self.close)
        publish_btn.clicked.connect(lambda: publish(self))

        # layout
        filepath_container.addWidget(filepath_label)
        filepath_container.addWidget(self.filepath_input)

        filename_container.addWidget(filename_label)
        filename_container.addWidget(self.filename_input)

        filetype_container.addWidget(filetype_label)
        filetype_container.addWidget(self.format_combo)

        comment_container.addWidget(comment_label)
        comment_container.addWidget(self.plain_text_edit)

        preview_container.addWidget(preview_label)
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

if __name__ == "__main__":
    app = QApplication()
    save_dialog = PublisherDialog()
    save_dialog.show()
    sys.exit(app.exec())