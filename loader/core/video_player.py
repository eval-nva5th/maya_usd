try:
    from PySide6.QtWidgets import QLabel
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QPixmap, QImage
except ImportError:
    from PySide2.QtWidgets import QLabel
    from PySide2.QtCore import Qt, QTimer
    from PySide2.QtGui import QPixmap, QImage
import cv2

# .mov file 재생을 위한 Class 
class VideoPlayer(QLabel):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

        self.setAlignment(Qt.AlignCenter)
        self.setText("Loading Video...")

        self.cap = cv2.VideoCapture(self.video_path)  # OpenCV 비디오 캡처 객체
        if not self.cap.isOpened():
            self.setText("Error: Cannot open video")
            return

        self.timer = QTimer(self)  # QTimer 사용
        self.timer.timeout.connect(self.frame_convert)  # 30ms마다 실행
        self.timer.start(30)
        
    def frame_convert(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상 끝나면 처음부터 다시 재생
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR -> Qt는 RGB 변환 필요
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        self.setPixmap(pixmap)

    def set_new_mov_file(self, file_path):
        # 기존 캡쳐 객체 해제
        if self.cap.isOpened():
            self.cap.release()

        # 새로운 비디오 파일을 열기
        self.video_path = file_path
        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            self.setText("Error: Cannot open video")
            return

        # 타이머가 중복 연결되지 않도록 기존 연결 해제
        self.timer.stop()
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.frame_convert)
        
        # 새 영상 재생 시작
        self.timer.start(30)
        self.frame_convert()  # 첫 번째 프레임을 즉시 표시