
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication
from PySide2.QtCore import Qt, QTimer
#from loader.core.video_player import VideoPlayer

try:
    import maya.utils
    IN_MAYA = True
except ImportError:
    IN_MAYA = False  # Maya가 아닌 환경에서는 False로 설정

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading...")
        self.setModal(True)
        self.setFixedSize(200, 200)
        self.setStyleSheet("background-color:black; color:white;")

        loading_mov = "/nas/eval/elements/loading.mp4"

        layout = QVBoxLayout()

        self.loading_text = QLabel("데이터 불러오는 중...")
        self.loading_text.setStyleSheet("font-size: 10px;")
        self.video_widget = VideoPlayer(loading_mov)
        self.video_widget.setScaledContents(True)  # QLabel 내부에서 비디오 크기 자동 조절

        layout.addWidget(self.video_widget, alignment=Qt.AlignCenter)
        layout.addWidget(self.loading_text, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def set_loading_text(self, text):

        if IN_MAYA:
            QTimer.singleShot(0, lambda: self.loading_text.clear())
            QTimer.singleShot(0, lambda: self.loading_text.setText(text))
            QTimer.singleShot(0, lambda: self.loading_text.repaint())
            QTimer.singleShot(0, lambda: self.loading_text.show())  # Maya에서 강제 UI 갱신
        else:
            self.loading_text.clear()
            self.loading_text.setText(text)
            self.loading_text.repaint()
            self.loading_text.show()
