from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView, QLabel, QLineEdit)
from PyQt5.QtCore import Qt
# Mock data for now, real implementation would query DB via DBManager

class DataViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        # Filter Bar
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Date Filter:"))
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        filter_layout.addWidget(self.date_input)
        
        filter_layout.addWidget(QLabel("Type:"))
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("normal/defect_nut/etc")
        filter_layout.addWidget(self.type_input)
        
        btn_search = QPushButton("Search")
        btn_search.setStyleSheet("background-color: #555555;")
        filter_layout.addWidget(btn_search)
        
        layout.addLayout(filter_layout)
        
        # Table View
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Filename", "Type", "Defect", "Created At"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget { gridline-color: #333333; } QHeaderView::section { background-color: #2d2d2d; padding: 4px; border: 1px solid #3e3e3e; }")
        
        layout.addWidget(self.table)
        
        # Pagination / Actions
        action_layout = QHBoxLayout()
        btn_export = QPushButton("Export to CSV")
        btn_export.setStyleSheet("background-color: #007acc;")
        action_layout.addWidget(btn_export)
        
        btn_delete = QPushButton("Delete Selected")
        btn_delete.setStyleSheet("background-color: #ff4444;")
        action_layout.addWidget(btn_delete)
        
        layout.addLayout(action_layout)
        
        # Load mock data
        self.load_mock_data()

    def load_mock_data(self):
        # In a real app, use self.db_manager.get_session()
        data = [
            (1, "img_001.png", "Original", "Normal", "2023-10-27 10:00:00"),
            (2, "img_002.png", "Original", "Defect_Nut", "2023-10-27 10:05:00"),
            (3, "gen_001.png", "Generated", "Defect_Crack", "2023-10-27 10:10:00"),
            (4, "gen_002.png", "Generated", "Defect_Hole", "2023-10-27 10:12:00"),
        ]
        
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
