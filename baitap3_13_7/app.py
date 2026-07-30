import os
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- CẤU HÌNH PHẦN CỨNG LED CHO RASPBERRY PI 5 ---
HAS_LED_HARDWARE = False
led_hardware = None
led_status_mock = 0

try:
    from gpiozero import LED
    # Khoi tao truc tiep LED tai GPIO 17 (Pin 11)
    led_hardware = LED(17)
    HAS_LED_HARDWARE = True
    print("-> Da ket noi thanh cong voi phan cung LED (GPIO 17)!")
except Exception as e:
    HAS_LED_HARDWARE = False
    print(f"-> Khong the khoi tao LED. Loi: {e}")

# Hàm lấy 20 bản ghi mới nhất từ CSDL để vẽ lên biểu đồ
def get_latest_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    # Lấy 20 dòng mới nhất, sắp xếp theo ID giảm dần
    cursor.execute('SELECT timestamp, temperature, humidity FROM dht_data ORDER BY id DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1] # Đảo ngược lại để dữ liệu cũ đứng trước, mới đứng sau trên biểu đồ

# 1. Định nghĩa Trang chủ của Web
@app.route('/')
def index():
    # Kiểm tra xem LED thực tế đang bật hay tắt để báo cho giao diện web biết
    if HAS_LED_HARDWARE and led_hardware is not None:
        current_status = led_hardware.value
    else:
        current_status = led_status_mock
        
    return render_template('index.html', led_status=current_status)

# 2. API: Trả dữ liệu nhiệt độ, độ ẩm mới nhất (Dạng JSON) cho biểu đồ tự vẽ
@app.route('/api/data')
def api_get_data():
    rows = get_latest_data()
    data = []
    for row in rows:
        data.append({
            'timestamp': row[0],
            'temperature': row[1],
            'humidity': row[2]
        })
    return jsonify(data)

# 3. API: Nhận lệnh click chuột từ giao diện Web để Bật/Tắt đèn LED
@app.route('/api/led', methods=['POST'])
def api_control_led():
    global led_status_mock
    req_data = request.get_json()
    action = req_data.get('action') # Nhận lệnh 'on' hoặc 'off' từ Web
    
    if action == 'on':
        if HAS_LED_HARDWARE and led_hardware is not None:
            led_hardware.on() # Bật LED thật trên Pi 5
        else:
            led_status_mock = 1 # Bật LED giả lập
        return jsonify({'status': 'success', 'led_status': 1})
        
    elif action == 'off':
        if HAS_LED_HARDWARE and led_hardware is not None:
            led_hardware.off() # Tắt LED thật trên Pi 5
        else:
            led_status_mock = 0 # Tắt LED giả lập
        return jsonify({'status': 'success', 'led_status': 0})
        
    return jsonify({'status': 'error', 'message': 'Hành động không hợp lệ'}), 400

# --- KHỞI CHẠY WEB SERVER ---
if __name__ == '__main__':
    # Chạy trên host 0.0.0.0, cổng 5000, tắt reloader để chống lỗi GPIO busy hoàn toàn
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
