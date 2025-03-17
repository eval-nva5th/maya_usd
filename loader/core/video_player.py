try :
    from PySide2.QtWidgets import QLabel
    from PySide2.QtCore import Qt, QThread, Signal, QTimer
    from PySide2.QtGui import QPixmap, QImage
except Exception :
    from PySide6.QtWidgets import QLabel
    from PySide6.QtCore import Qt, QThread, Signal, QTimer
    from PySide6.QtGui import QPixmap, QImage
    
import cv2

try:
    import maya.utils
    IN_MAYA = True
except ImportError:
    IN_MAYA = False  # Maya가 아닌 환경에서는 False로 설정

class VideoThread(QThread):
    """ 백그라운드에서 비디오 프레임을 가져오는 스레드 """
    frame_signal = Signal(QPixmap)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.running = True

    def run(self):
        """ 비디오 프레임을 계속 읽어서 UI에 전달 """
        while self.running:
            ret, frame = self.cap.read()  # 프레임 자동 증가 (CAP_PROP_POS_FRAMES 제거)
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상 끝나면 처음부터 다시 재생
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            if IN_MAYA:
                maya.utils.executeDeferred(lambda: self.frame_signal.emit(pixmap))  # executeDeferred 유지
            else:
                self.frame_signal.emit(pixmap)

            self.msleep(33)  # 30FPS로 유지

    def stop(self):
        """ 스레드 정지 및 리소스 해제 """
        self.running = False
        self.quit()
        self.wait()
        self.cap.release()

class VideoPlayer(QLabel):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.setAlignment(Qt.AlignCenter)
        self.setText("Loading Video...")

        # 백그라운드 스레드 실행
        self.video_thread = VideoThread(self.video_path)
        self.video_thread.frame_signal.connect(self.update_frame)
        self.video_thread.start()

        # Maya에서 UI 업데이트 속도를 맞추기 위해 QTimer 사용
        if IN_MAYA:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.force_update)
            self.timer.start(33)  # Maya 이벤트 루프와 동기화

    def update_frame(self, pixmap):
        """ 메인 스레드에서 비디오 프레임 업데이트 """
        self.setPixmap(pixmap)  # 프레임이 중복되는 조건 제거

    def force_update(self):
        """ Maya에서는 강제 업데이트 실행 """
        self.repaint()  # Maya에서 강제로 UI 갱신

    def set_new_mov_file(self, file_path):
        """ 새로운 비디오 파일을 열고 재생 """
        self.video_thread.stop()  # 기존 스레드 정지
        self.video_path = file_path
        self.video_thread = VideoThread(self.video_path)
        self.video_thread.frame_signal.connect(self.update_frame)
        self.video_thread.start()
