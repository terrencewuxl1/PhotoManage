import os
from PIL import Image
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt

def make_thumbnail(path, size=(150,150)):
    try:
        img = Image.open(path)
        img.thumbnail(size)
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap
    except Exception as e:
        print(f"Thumbnail error for {path}: {e}")
        return None

MEDIA_EXT = [".jpg", ".jpeg", ".png", ".heic", ".gif",
             ".mp4", ".mov", ".avi", ".mkv", ".wmv"]