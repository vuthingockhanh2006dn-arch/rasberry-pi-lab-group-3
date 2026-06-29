import time
from datetime import datetime
import sys

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
DHT_PIN = 20

LOG_FILENAME = "log.txt"

def read_sensor_data():
    """
    Đọc dữ liệu từ cảm biến DHT11 thật hoặc giả lập nếu chạy trên PC.
    Trả về: (nhiệt độ, độ ẩm)
    """
    if HAS_HARDWARE:

        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        return temperature, humidity
    else:
        temperature = random.randint(20, 35)
        humidity = random.randint(40, 80)
        # Giả lập thời gian đọc cảm biến khoảng 0.5s
        time.sleep(0.5)
        return temperature, humidity

def run_logger(interval_seconds=2):
    """
    Vòng lặp đọc dữ liệu liên tục và ghi vào file log.txt
    """
    print("=" * 60)
    if HAS_HARDWARE:
        print(f"Bắt đầu đọc cảm biến DHT11 thật trên chân GPIO {DHT_PIN}...")
    else:
        print("Không phát hiện phần cứng Raspberry Pi. Chạy ở chế độ GIẢ LẬP (Simulation Mode).")
    print(f"Dữ liệu ghi log sẽ được lưu vào file: {LOG_FILENAME}")
    print("Nhấn Ctrl+C để dừng chương trình.")
    print("=" * 60)

    try:
        while True:
            temp, humi = read_sensor_data()
            
            if temp is not None and humi is not None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                
                log_line = f"{timestamp} {int(temp)}oC {int(humi)}%"
                
                print(f"[LOGGED] {log_line}")
                
                # Ghi đè/Nối tiếp vào file log.txt
                with open(LOG_FILENAME, "a", encoding="utf-8") as file:
                    file.write(log_line + "\n")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Lỗi: Không thể đọc được dữ liệu từ cảm biến DHT11!")
            
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình ghi log.")

if __name__ == "__main__":
    # Khoảng cách giữa mỗi lần ghi log mặc định là 2 giây
    run_logger(interval_seconds=2)