import time
import sqlite3
import random

DB_FILE = 'sensor_data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dht_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
            temperature REAL,
            humidity REAL,
            led_status INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_data(temp, hum, led_stat):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dht_data (temperature, humidity, led_status)
            VALUES (?, ?, ?)
        ''', (temp, hum, led_stat))
        conn.commit()
        conn.close()
        print(f"[CÂU 2 SUCCESS] -> Nhiệt độ: {temp}°C | Độ ẩm: {hum}% | LED: {led_stat}")
    except Exception as e:
        print(f"[LỖI CSDL]: {e}")

def main():
    init_db()
    print("=== ĐANG CHẠY GIẢ LẬP ĐỌC DHT11 VÀ GHI CSDL ===")
    while True:
        # Giả lập dữ liệu nhiệt độ từ 25-30 độ, độ ẩm từ 50-70%
        temp = round(random.uniform(25.0, 30.0), 1)
        hum = round(random.uniform(50.0, 70.0), 1)
        led_stat = 0
        
        save_data(temp, hum, led_stat)
        time.sleep(2)

if __name__ == '__main__':
    main()
