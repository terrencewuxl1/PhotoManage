import os
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QMessageBox, QLabel,
    QListWidgetItem, QStyle
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

from utils import MEDIA_EXT
from scan_worker import ScanWorker
from utils import make_thumbnail
from config import get_db_path
from db import MediaDatabase


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo & Video Organizer")
        self.resize(1200, 700)
        db_path = get_db_path()
        self.db = MediaDatabase(db_path)
        self.worker = None

        # Layout
        main_layout = QHBoxLayout()

        # --- Left panel ---
        left = QVBoxLayout()
        self.scan_btn = QPushButton("Scan Folder")
        self.scan_btn.clicked.connect(self.scan_folder)
        left.addWidget(self.scan_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_data)
        left.addWidget(self.clear_btn)  # or put it in a layout

        self.date_list = QListWidget()
        self.date_list.itemClicked.connect(self.load_media_for_date)
        left.addWidget(QLabel("Dates"))
        left.addWidget(self.date_list)

        # --- Right panel ---
        right = QVBoxLayout()
        right.addWidget(QLabel("Photos / Videos"))

        self.thumb_list = QListWidget()
        self.thumb_list.setViewMode(QListWidget.IconMode)
        self.thumb_list.setIconSize(QSize(150, 150))
        self.thumb_list.setResizeMode(QListWidget.Adjust)
        self.thumb_list.setMovement(QListWidget.Static)
        self.thumb_list.setSpacing(10)
        right.addWidget(self.thumb_list)

        main_layout.addLayout(left, 2)
        main_layout.addLayout(right, 6)
        self.setLayout(main_layout)

        self.load_dates()

    def scan_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if not folder:
            return

        self.scan_btn.setEnabled(False)
        self.worker = ScanWorker(folder, MEDIA_EXT)
        self.worker.progress.connect(self.on_scan_progress)
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.start()

    def on_scan_progress(self, _):
        # refresh every ~1 second
        self.load_dates()

    def on_scan_finished(self, count):
        QMessageBox.information(self, "Scan Complete", f"Indexed {count} new media files")
        self.load_dates()
        self.scan_btn.setEnabled(True)

    def load_dates(self):
        self.date_list.clear()
        for day, cnt in self.db.get_dates():
            item = QListWidgetItem(f"{day} ({cnt})")
            item.setData(Qt.UserRole, day)
            self.date_list.addItem(item)

    def load_media_for_date(self, item):
        date_str = item.data(Qt.UserRole)
        self.thumb_list.clear()
        media_files = self.db.get_media_by_date(date_str)

        for path, ext in media_files:
            lw_item = QListWidgetItem()
            lw_item.setText(os.path.basename(path))
            if ext.lower() in [".jpg", ".jpeg", ".png", ".heic", ".gif"]:
                pixmap = make_thumbnail(path)
                if pixmap:
                    lw_item.setIcon(QIcon(pixmap))
            else:
                lw_item.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            self.thumb_list.addItem(lw_item)

    def clear_data(self):
        # clear database
        self.db.clear_all()

        # clear UI
        self.date_list.clear()
        self.thumb_list.clear()
