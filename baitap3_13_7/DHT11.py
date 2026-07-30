import time
from datetime import datetime
import sys
import sqlite3  # <--- Đã tích hợp kết nối CSDL

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    import Adafruit_DHT
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False
    import random

DHT_SENSOR = None
if HAS_HARDWARE:
    DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

LOG_FILENAME = "log.txt"

def read_sensor_data():
    """
    Đọc dữ liệu từ cam bien DHT11 that hoac gia lap tren PC.
    """
    if HAS_HARDWARE:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        return temperature, humidity
    else:
        temperature = random.randint(20, 35)
        humidity = random.randint(40, 80)
        time.sleep(0.5)
        return temperature, humidity

# Hàm này đảm nhận việc mở hòm CSDL và cất dữ liệu vào
def luu_vao_csdl(temp, hum):
    try:
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO dht_data (temperature, humidity) VALUES (?, ?)', 
            (temp, hum)
        )
        conn.commit()
        conn.close()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã lưu vào CSDL: Temp={temp}°C, Hum={hum}%")
    except Exception as e:
        print("Lỗi khi ghi vào CSDL:", e)

# Vòng lặp chạy liên tục ngầm
if __name__ == "__main__":
    print("Bắt đầu chương trình đọc cảm biến và lưu CSDL...")
    print("Bấm Ctrl + C nếu muốn dừng lại.")
    
    while True:
        temp, hum = read_sensor_data()
        if temp is not None and hum is not None:
            luu_vao_csdl(temp, hum) # <--- Tự động gọi lưu sau khi đọc thành công
        else:
            print("Lỗi: Không đọc được dữ liệu từ cảm biến, đang thử lại...")
            
        time.sleep(10) # 10 giây lưu 1 lần
