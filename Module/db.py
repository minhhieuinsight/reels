import sqlite3
import datetime

class Database:
    def __init__(self):
        # Kết nối SQLite với check_same_thread=False để tránh lỗi khi dùng đa luồng
        self.conn = sqlite3.connect("videos.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Tạo bảng nếu chưa tồn tại
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                id TEXT PRIMARY KEY, 
                name TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS page_video_dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                page_id TEXT, 
                video_id INTEGER, 
                date TEXT,
                UNIQUE(page_id, video_id, date),
                FOREIGN KEY (page_id) REFERENCES pages(id),
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        """)
        self.conn.commit()  # Đảm bảo thay đổi được lưu
    
    def get_or_create_id(self, table, name, id_field="id"):
        self.cursor.execute(f"SELECT {id_field} FROM {table} WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        self.cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
        self.conn.commit()  # Thêm commit để tránh database bị lock
        return self.cursor.lastrowid

    def check_data(self, page_id, page_name, date):
        self.cursor.execute("""
            SELECT v.name FROM page_video_dates pvd
            JOIN videos v ON pvd.video_id = v.id
            WHERE pvd.page_id = ? AND pvd.date = ?
        """, (page_id, date))
        
        existing_videos = {row[0] for row in self.cursor.fetchall()}
        
        return len(existing_videos) >= 3

    def insert_videos(self, page_id, page_name, date, videos):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO pages (id, name) VALUES (?, ?)", (page_id, page_name))
            self.cursor.execute("""
                SELECT v.name FROM page_video_dates pvd
                JOIN videos v ON pvd.video_id = v.id
                WHERE pvd.page_id = ? AND pvd.date = ?
            """, (page_id, date))
            
            existing_videos = {row[0] for row in self.cursor.fetchall()}

            for video in videos:
                if video in existing_videos:
                    print(f"Video: {video} đã tồn tại -> Pass")
                    continue
                video_id = self.get_or_create_id("videos", video)
                self.cursor.execute("INSERT OR IGNORE INTO page_video_dates (page_id, video_id, date) VALUES (?, ?, ?)", (page_id, video_id, date))

            self.conn.commit()  # Ghi vào database để tránh lock
            return True
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Database lock error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()
