import sys
from PySide2.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout


class clickedTask:
    def __init__(self, name, file_path, data_list):
        self.name = name
        self.file_path = file_path
        self.data_list = data_list


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layouts
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Left table widget (name table)
        self.left_table = QTableWidget(5, 1)  # 5 rows, 1 column
        self.left_table.setHorizontalHeaderLabels(['Name'])
        self.left_table.setItem(0, 0, QTableWidgetItem('Task 1'))
        self.left_table.setItem(1, 0, QTableWidgetItem('Task 2'))
        self.left_table.setItem(2, 0, QTableWidgetItem('Task 3'))
        self.left_table.setItem(3, 0, QTableWidgetItem('Task 4'))
        self.left_table.setItem(4, 0, QTableWidgetItem('Task 5'))
        self.left_table.cellClicked.connect(self.on_left_table_clicked)

        left_layout.addWidget(self.left_table)

        # Right side small table widgets
        self.right_table_1 = QTableWidget(0, 3)  # Initially empty, 3 columns
        self.right_table_1.setHorizontalHeaderLabels(['Col A', 'Col B', 'Col C'])
        self.right_table_2 = QTableWidget(0, 3)
        self.right_table_2.setHorizontalHeaderLabels(['Col D', 'Col E', 'Col F'])

        self.right_table_1.cellClicked.connect(self.on_right_table_1_clicked)
        self.right_table_2.cellClicked.connect(self.on_right_table_2_clicked)

        right_layout.addWidget(self.right_table_1)
        right_layout.addWidget(self.right_table_2)

        # Adding layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Initial clickedTask object
        self.ct = None

    def on_left_table_clicked(self, row, column):
        # Create a new clickedTask object when a cell is clicked
        task_names = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']
        data_lists = [
            [['1a', '1b', '1c'], ['1d', '1e', '1f', '1g']],  # Example with 3 columns, different row sizes
            [['2a', '2b', '2c', '2x'], ['2d', '2e']],  # Example with different lengths
            [['3a', '3b', '3c'], ['3d']],
            [['4a', '4b'], ['4d', '4e', '4f']],
            [['5a', '5b', '5c', '5d'], ['5d', '5e', '5f']]
        ]

        name = task_names[row]
        file_path = f"/path/to/{name.lower().replace(' ', '_')}"
        data_list = data_lists[row]

        self.ct = clickedTask(name, file_path, data_list)

        # Populate the right tables with data from ct.data_list
        self.populate_right_tables()

    def populate_right_tables(self):
        if self.ct is None:
            return

        # Right table 1 - Dynamic row count based on the length of the first data list
        self.right_table_1.setRowCount(len(self.ct.data_list[0]))  # Flexible row count
        for row, data in enumerate(self.ct.data_list[0]):
            self.right_table_1.setColumnCount(len(data))  # Adjust column count to fit the data
            for col, value in enumerate(data):
                self.right_table_1.setItem(row, col, QTableWidgetItem(value))

        # Right table 2 - Dynamic row count based on the length of the second data list
        self.right_table_2.setRowCount(len(self.ct.data_list[1]))  # Flexible row count
        for row, data in enumerate(self.ct.data_list[1]):
            self.right_table_2.setColumnCount(len(data))  # Adjust column count to fit the data
            for col, value in enumerate(data):
                self.right_table_2.setItem(row, col, QTableWidgetItem(value))

    def on_right_table_1_clicked(self, row, column):
        if self.ct is not None:
            value = self.ct.data_list[0][row][column]
            print(f"Clicked on Right Table 1: {value}")

    def on_right_table_2_clicked(self, row, column):
        if self.ct is not None:
            value = self.ct.data_list[1][row][column]
            print(f"Clicked on Right Table 2: {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
