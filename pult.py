from mcrcon import MCRcon
import time
import tkinter as tk
import argparse

# Настройки сервера и RCON
HOST = "146.59.53.122"      # IP сервера
PORT = 26003                # RCON порт
PASSWORD = "12345454545455454"  # RCON пароль

signals = {
    "E1": "e1-ln3",
    "E2": "e2-ln4",
}

def send_command(cmd):
    try:
        # Подключаемся через RCON, передаем порт явно
        with MCRcon(HOST, PASSWORD, port=PORT) as mcr:
            response = mcr.command(cmd)
            return response
    except Exception as e:
        return f"Ошибка подключения: {e}"

def handle_signal(sig_name, line_code, lamp):
    # Отправляем ULX команду для открытия сигнала
    send_command(f"ulx sopen {line_code}")
    time.sleep(0.3)
    # Запрашиваем состояние сигнала
    response = send_command(f"!sigstate {sig_name}")
    update_lamp(response, lamp)

def update_lamp(response, lamp):
    green_words = ["зел", "жёл", "разреш", "бел", "жел"]
    response_lower = response.lower()
    if any(word in response_lower for word in green_words):
        lamp.config(bg="green")
    else:
        lamp.config(bg="red")

root = tk.Tk()
root.title("Metrostroi Пульт")
root.geometry("320x400")

for sig_name, line_code in signals.items():
    frame = tk.Frame(root)
    frame.pack(pady=10)

    lamp = tk.Label(frame, text=sig_name, bg="gray", width=10, height=2, font=("Arial", 12))
    lamp.pack(side=tk.LEFT, padx=10)

    btn = tk.Button(
        frame,
        text=f"Открыть {sig_name}",
        font=("Arial", 10),
        command=lambda sn=sig_name, lc=line_code, lbl=lamp: handle_signal(sn, lc, lbl)
    )
    btn.pack(side=tk.LEFT)

root.mainloop()
