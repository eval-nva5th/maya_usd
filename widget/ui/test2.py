from shotgun_api3 import Shotgun 
import requests
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import Qt  # 필수 임포트 추가
import sys

class ThumbnailWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShotGrid User Thumbnail")
        self.resize(200, 200)

        sg_url = "https://hi.shotgrid.autodesk.com/"
        script_name = "Admin_SY"
        api_key = "kbuilvikxtf5v^bfrivDgqhxh"

        # ShotGrid API 연결
        self.sg = Shotgun(sg_url, script_name, api_key)

        self.entity_type = "Shot"
        self.entity_id = 1253

        colleague_list = self.get_colleague_info()

        colleague_layout = QGridLayout()
        
        for row, item in enumerate(colleague_list):
            thumb_label = QLabel(self)
            thumb_label.setFixedSize(20, 20)
            thumb_label.setScaledContents(True)
           
            pixmap = QPixmap()
            image_data = requests.get(item[3]).content if item[3] else None

            if image_data:
                pixmap.loadFromData(image_data)
                
            else:
                pixmap = QPixmap("/nas/eval/elements/no_assignee.png")
# 이미지가 확실히 존재하는지 체크 후 설정
                if not pixmap.isNull():
                    pass
                else:
                    thumb_label = QLabel("")
                    thumb_label.setAlignment(Qt.AlignCenter)

            pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            pixmap = pixmap.copy((pixmap.width()-20)//2, (pixmap.height()-20)//2, 20, 20)
            thumb_label.setPixmap(pixmap)
                
            text_label = QLabel(f"{str(item[0])} : {str(item[1])}")

            colleague_layout.addWidget(thumb_label, row, 0)
            colleague_layout.addWidget(text_label, row, 1)

        self.setLayout(colleague_layout) 

    def get_colleague_info(self):
        colleague_list = []

        tasks = self.sg.find(
            "Task",
            [["entity", "is", {"type": self.entity_type, "id": self.entity_id}]], 
            ["id", "task_assignees", "step"]
        )

        # 결과 출력
        for task in tasks:
            task_type = task["step"]["name"]
            assignees = task["task_assignees"]

            if assignees :
                assignees_name = assignees[0]['name']
                assignees_id = assignees[0]['id']
                thumb_url = self.sg.find_one("HumanUser",
                        [['id', 'is', assignees_id]],
                        ["image"]).get('image')

            else:
                assignees_name = "None"
                assignees_id = 0
                thumb_url = ""
            each_list = [task_type, assignees_name, assignees_id, thumb_url]

            if len(each_list) == 4:
                colleague_list.append(each_list)


        return colleague_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThumbnailWindow()
    window.show()
    sys.exit(app.exec_())
