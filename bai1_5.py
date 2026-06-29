import subprocess
import socket

ten_may = socket.gethostname()

ip = subprocess.check_output("hostname -I", shell=True).decode().strip().split()[0]

print("Ten may:", ten_may)
print("Dia chi IP:", ip)





