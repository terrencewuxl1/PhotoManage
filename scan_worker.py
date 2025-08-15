import os

from PySide6.QtCore import QThread, Signal

from db import MediaDatabase
from config import get_db_path

class ScanWorker(QThread):
    progress = Signal(str)
    finished = Signal(int)

    def __init__(self, folder, media_ext):
        super().__init__()
        self.folder = folder
        self.media_ext = media_ext

    def run(self):
        # open a fresh db connection in this thread
        db = MediaDatabase(get_db_path())
        count = 0
        for root, _, files in os.walk(self.folder):
            for f in files:
                if os.path.splitext(f)[1].lower() in self.media_ext:
                    full_path = os.path.join(root, f)
                    db.insert_file(full_path)
                    count += 1
                    self.progress.emit(full_path)
                    self.msleep(10)
        db.close()
        self.finished.emit(count)
