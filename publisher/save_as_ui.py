from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtWidgets import QVBoxLayout, QLabel, QLineEdit
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QComboBox

import sys

class SaveAsDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save As")
        self.setGeometry(100, 100, 650, 200)

        self.center_window()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 파일명 Label + LineEdit
        filename_container = QHBoxLayout()
        self.filename_label = QLabel("File name:", self)
        self.filename_input = QLineEdit("file_name_input_v001",self)

        # 파일 경로 Label + LineEdit
        filepath_container = QHBoxLayout()
        self.filepath_label = QLabel("File path:", self)
        self.filepath_input = QLineEdit("/nas/eval/", self)
        self.browse_btn = QPushButton("Browse", self)

        # 파일 타입 
        filetype_container = QHBoxLayout()
        self.filetype_label = QLabel("File of type:", self)
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["Maya Binary", "Maya ASCII"])  # 옵션 추가
        self.format_combo.setCurrentText("Maya Binary")  # 기본값 설정

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

        # 이벤트 처리
        self.browse_btn.clicked.connect(self.open_file_browser)
        self.save_as_btn.clicked.connect(self.save_file_as)
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

        filetype_container.addWidget(self.filetype_label)
        filetype_container.addWidget(self.format_combo)

        layout.addLayout(filepath_container)
        layout.addLayout(filename_container)
        layout.addLayout(filetype_container)
        layout.addLayout(button_container)
        central_widget.setLayout(layout)

    def open_file_browser(self):
        default_filename = self.filename_input.text().strip()
        default_filepath = self.filepath_input.text() if self.filepath_input.text() else "/nas/eval/"

        filepath, _ = QFileDialog.getSaveFileName(self, "Select File Path", f"{default_filepath}{default_filename}", "All Files (*)")
        if filepath:
            self.filepath_input.setText(filepath)

    def save_file_as(self):
        filename = self.filename_input.text().strip()
        filepath = self.filepath_input.text().strip()
        
        if not filename or not filepath:
            QMessageBox.critical(self, "Error", "File name or File path does not exist", QMessageBox.Ok)
            return          

        full_path = f"{filepath}{filename}"
        
        # 파일 저장 및 버전업 로직 작성
        try:
            print(f"{full_path}에 파일 저장 시도")
            self.close()
        except FileNotFoundError:
            print("File path does not exist")
        except PermissionError:
            print("You do not have permission to save the file")
        except Exception as e:
            print(f"An unexpected error : {e}")

    # def resizeEvent(self, event):
    #     self.center_window()
    #     super().resizeEvent(event)

    
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
    #app = QApplication()
    save_dialog = SaveAsDialog()
    save_dialog.show()
    #sys.exit(app.exec())