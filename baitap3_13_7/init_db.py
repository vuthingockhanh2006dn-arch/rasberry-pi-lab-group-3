import sqlite3

def init_database():
    print("Vui lòng đợi, đang khởi tạo cấu trúc Cơ sở dữ liệu...")
    # Kết nối (hoặc tự tạo nếu chưa có) file CSDL
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    
    # Lệnh tạo bảng dht_data chuẩn cho hệ thống
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dht_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Chúc mừng! Đã tạo bảng 'dht_data' thành công trong file sensor_data.db.")

if __name__ == "__main__":
    init_database()
