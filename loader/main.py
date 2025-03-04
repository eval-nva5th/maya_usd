from PySide6.QtWidgets import QApplication
from ui.loader_ui import UI

if __name__ == "__main__":
    app = QApplication([])
    print ("UI 인스턴스 생성 시작")
    ui = UI() 
    print ("UI 인스턴스 생성 완료")
    ui.show() 
    app.exec()