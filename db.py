import os, sqlite3
from datetime import datetime

class MediaDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            filename TEXT,
            extension TEXT,
            size INTEGER,
            modified DATETIME
        )""")
        self.conn.commit()

    def insert_file(self, filepath):
        stat = os.stat(filepath)
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()
        modified = datetime.fromtimestamp(stat.st_mtime)
        self.conn.execute("""INSERT OR IGNORE INTO media
            (path, filename, extension, size, modified)
            VALUES (?, ?, ?, ?, ?)""",
            (filepath, filename, ext, stat.st_size, modified))
        self.conn.commit()

    def get_dates(self):
        cur = self.conn.execute("""SELECT DATE(modified), COUNT(*)
                                   FROM media
                                   GROUP BY DATE(modified)
                                   ORDER BY DATE(modified) DESC""")
        return cur.fetchall()

    def get_media_by_date(self, date_str):
        cur = self.conn.execute("SELECT path, extension FROM media WHERE DATE(modified)=? ORDER BY modified", (date_str,))
        return cur.fetchall()

    def clear_all(self):
        self.conn.execute("DELETE FROM media")
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
