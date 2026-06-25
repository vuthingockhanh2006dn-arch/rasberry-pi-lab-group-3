import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Moi ban noi...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="vi-VN")
    print("Ban vua noi:", text)

except sr.UnknownValueError:
    print("Khong nhan dang duoc")

except sr.RequestError:
    print("Loi ket noi internet")
