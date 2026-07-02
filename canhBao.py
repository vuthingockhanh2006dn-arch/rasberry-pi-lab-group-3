#!/usr/bin/python3

import time
from datetime import datetime

while True:
    a = int(input("Nhập ngưỡng a (cm): "))
    distance = float(input("Nhập khoảng cách đo được (cm): "))

    if distance < a:
        print(">>> CẢNH BÁO: Có vật cản!")

        with open("warning.log", "a") as f:
            f.write(f"{datetime.now()} - Distance: {distance:.2f} cm\n")

    time.sleep(1)
