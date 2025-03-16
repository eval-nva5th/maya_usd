from PySide2.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QGridLayout, QScrollArea
from PySide2.QtWidgets import QHBoxLayout, QWidget, QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
import sys, os
from asset_library.event.ui_event_handler import clicked_load_btn

class AssetLibUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.asset_list = self.get_asset_info()
        print(self.asset_list)
        self.setWindowTitle("Asset Library")
        self.setFixedSize(710, 850)

        self.center_window()

        self.selected_num = 0
        self.selected_cells = []  
        self.last_selected_cell = None 

        central_widget = QWidget(self)
        main_layout = QVBoxLayout()
        self.setCentralWidget(central_widget)

        # Selected num
        self.selected_asset_num = QLabel(f"Selected Asset : {self.selected_num}")
        main_layout.addWidget(self.selected_asset_num)
        self.selected_asset_num.setStyleSheet("font-size: 20px;")

        # QScrollArea
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_area.setWidgetResizable(True)

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(10)
        self.grid_layout.setRowStretch(len(self.asset_list) // 3 + 1, 1) # 상단 정렬

        self.add_cell_to_grid(self.asset_list)

        # ScrollArea에 배치
        scroll_content.setLayout(self.grid_layout)
        scroll_area.setWidget(scroll_content)

        # Buttons
        cancel_btn = QPushButton("Cancel")
        load_btn = QPushButton("Load Assets")
        button_container = QHBoxLayout()
        button_container.addWidget(cancel_btn)
        button_container.addWidget(load_btn)
        
        cancel_btn.clicked.connect(self.close)
        load_btn.clicked.connect(lambda : clicked_load_btn(self, self.selected_cells))

        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_container)
        central_widget.setLayout(main_layout)

    def add_cell_to_grid(self, asset_list):
        self.cell_widgets = []
        for index, (asset_name, image_path) in enumerate(asset_list):
            row = index // 3
            col = index % 3

            cell_widget = ClickableWidget(asset_name, self, index, image_path)
            cell_layout = QVBoxLayout()
            cell_layout.setAlignment(Qt.AlignTop)
            cell_layout.setSpacing(0)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setFixedSize(210, 180)

            # 이미지 QLabel
            image_label = QLabel()
            image_label.setFixedSize(210, 130)
            pixmap = QPixmap(image_path).scaled(210, 130, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            # 파일명 QLabel
            text_label = QLabel(asset_name)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("font-size: 14px;")

            # 레이아웃에 추가
            cell_layout.addWidget(image_label)
            cell_layout.addWidget(text_label)
            cell_widget.setLayout(cell_layout)

            # QGridLayout에 추가
            self.grid_layout.addWidget(cell_widget, row, col)
            self.cell_widgets.append(cell_widget)
            cell_widget.setStyleSheet("border : 2px solid transparent;")

    def select_cell(self, cell_widget):
        if cell_widget in self.selected_cells:
            self.remove_from_selection(cell_widget)
        else:
            self.add_to_selection(cell_widget)

        self.selected_num = len(self.selected_cells)
        self.selected_asset_num.setText(f"Selected Asset : {self.selected_num}")

    def add_to_selection(self, cell_widget):
        if cell_widget not in self.selected_cells:
            self.selected_cells.append(cell_widget)
            cell_widget.setStyleSheet("background-color: #5386A6;border : 2px solid #5386A6;")

    def remove_from_selection(self, cell_widget):
        if cell_widget in self.selected_cells:
            self.selected_cells.remove(cell_widget)
            cell_widget.setStyleSheet("background-color: none;border : 2px solid transparent")

    def get_asset_info(self):
        prefix_path = "/nas/eval/show"
        proj_name = "eval"
        entity_type = "assets"

        path_list = [proj_name, entity_type]
        asset_list = []

        asset_type_path = os.path.join(prefix_path, *path_list) # /nas/eval/show/eval/assets
        asset_type_list = os.listdir(asset_type_path) # [character, environment, vehicle, props]

        for asset_type in asset_type_list:
            asset_name_path = os.path.join(asset_type_path, asset_type)
            asset_name_list = os.listdir(asset_name_path)

            for asset_name in asset_name_list:
                task_path = os.path.join(asset_name_path, asset_name)
                task_list = os.listdir(task_path)

                jpg_file_name = "/nas/eval/elements/null.png"
                for task in task_list:
                    if task in ["lookdev", "model"]:
                        jpg_path = os.path.join(task_path, task, "pub/maya/data")
                        jpg_full_path = os.path.join(jpg_path, f"{asset_name}_{task}.jpg")
                        if os.path.exists(jpg_full_path):
                            jpg_file_name = jpg_full_path
                            if task == "lookdev":
                                break
                    
                asset_list.append((asset_name, jpg_file_name))
        return asset_list
    
    def center_window(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.frameGeometry()
        center_x = screen_geometry.width() // 2 - window_geometry.width() // 2
        center_y = screen_geometry.height() // 2 - window_geometry.height() // 2
        self.setGeometry(center_x, center_y, window_geometry.width(), window_geometry.height())        
        self.move(center_x, center_y)


class ClickableWidget(QWidget):
    def __init__(self, asset_name, parent_window, index, image_path):
        super().__init__()
        self.asset_name = asset_name
        self.image_path = image_path
        self.parent_window = parent_window
        self.index = index
        
    def mousePressEvent(self, event):
        self.parent_window.select_cell(self)

    def enterEvent(self, event):
        if self in self.parent_window.selected_cells:
            return
        self.setStyleSheet("background-color: #5386A6;border : 2px solid #5386A6;")

    def leaveEvent(self, event):
        if self in self.parent_window.selected_cells:
            return 
        self.setStyleSheet("background-color: none;border : 2px solid transparent") 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssetLibUI()
    window.show()
    sys.exit(app.exec_())
