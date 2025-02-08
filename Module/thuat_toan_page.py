
import os
import random
import datetime
import sqlite3

video_pool = os.listdir("./Video")

pages = ["pageA", "pageB", "pageC", "pageD", "pageE", "pageF", "pageG"]

DB_NAME = "posting_history.db"

def init_db():
    """Khởi tạo DB và bảng posting_history nếu chưa tồn tại."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posting_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            date TEXT NOT NULL,
            video TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_today():
    return datetime.date.today().isoformat()

def get_posted_videos(page, date):
    """Truy vấn DB để lấy danh sách video đã đăng của page vào ngày date."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT video FROM posting_history 
        WHERE page = ? AND date = ?
    """, (page, date))
    rows = cursor.fetchall()
    conn.close()
    # Trả về danh sách các video
    return [row[0] for row in rows]

def add_posting_history(page, date, videos):
    """Thêm thông tin các video đã đăng của page vào DB."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for video in videos:
        cursor.execute("""
            INSERT INTO posting_history (page, date, video)
            VALUES (?, ?, ?)
        """, (page, date, video))
    conn.commit()
    conn.close()

def distribute_videos(video_pool, pages, videos_per_page=3):
    today = get_today()
    schedule = {}

    for page in pages:
        # Lấy lịch sử đăng từ DB cho page hôm nay
        used_videos = get_posted_videos(page, today)
        
        # Lọc danh sách video chưa dùng cho page hôm nay
        available = [vid for vid in video_pool if vid not in used_videos]
        
        # Nếu không đủ số video cần chọn, reset lịch sử cho page đó (cho phép đăng lại)
        if len(available) < videos_per_page:
            available = video_pool.copy()
            # Trong trường hợp reset, bạn có thể xóa lịch sử cũ nếu muốn:
            # reset_history(page, today) -> hoặc chỉ cho phép đăng lại mà không xóa
            # Ở đây ta sẽ không xóa dữ liệu DB, nhưng lựa chọn available là toàn bộ video.
        
        # Chọn ngẫu nhiên videos_per_page video
        chosen = random.sample(available, videos_per_page)
        schedule[page] = chosen
        
        # Cập nhật lịch sử đăng trong DB
        add_posting_history(page, today, chosen)
    
    return schedule

if __name__=="__main__":
    init_db()
    
    # Phân bổ video cho các page
    schedule = distribute_videos(video_pool, pages)
    
    # In kết quả phân bổ
    for page, videos in schedule.items():
        print(f"Page {page} sẽ đăng: {videos}")



















