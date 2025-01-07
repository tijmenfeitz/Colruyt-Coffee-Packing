import time
# from periphery import GPIO
import tkinter as tk
from PIL import Image, ImageTk
import socket
import cv2
from ultralytics import YOLO
import struct
import threading

# Define TCP connection parameters
UR10_IP = "192.168.0.43"
PORT = 30000

# Socket to act as a server
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("192.168.0.80", PORT))  # IP address of the UP developer board
# server_socket.listen(1)

# print("Waiting for robot connection...")
# client_socket, client_address = server_socket.accept()
# print(f"Connected to robot: {client_address}")
# client_socket.setblocking(False)

# SENSOR_PIN = 23
# sensor_box = GPIO(SENSOR_PIN, "in")

data = [0, 0, 0]  # 4 bags ready, box ready, option
# client_socket.settimeout(0.1)

# model = YOLO("Coffee.pt")

running = False

# def send_array(data):
#     try:
#         packed_data = struct.pack(f'{len(data)}B', *data)
#         client_socket.send(packed_data)
#         print(f"Sent data: {data}")
#     except Exception as e:
#         print(f"Error sending data: {e}")
#         sensor_box.close()
#         server_socket.close()
#         client_socket.close()

# def read_sensor_and_process():
#     global data, running
#     while running:
#         try:
#             # Leer el estado del sensor
#             box_ready = 1 if sensor_box.read() == 0 else 0
#             data[1] = box_ready

#             if box_ready == 1:
#                 print("Box is ready. Starting camera detection...")
#                 detect_bags()  # Ejecutar detección de bolsas
#             else:
#                 print("Waiting for box to be ready...")

#             send_array(data)
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"Error reading sensor: {e}")
#             break

# def detect_bags():
#     global data
#     try:
#         while running:
#             cap = cv2.VideoCapture(0)
#             if not cap.isOpened():
#                 print("Cannot access the camera.")
#                 return

#             ret, frame = cap.read()
#             if not ret:
#                 print("Cannot take picture.")
#                 return

#             # Ejecutar modelo YOLO en el frame
#             frame_resized = cv2.resize(frame, (640, 480))
#             results = model(frame_resized)

#             bags_detected = sum([1 for box in results[0].boxes if int(box.cls) == 0])

#             if bags_detected < 4:
#                 print(f"Missing bags. Detected: {bags_detected}. Retrying...")
#             else:
#                 print(f"Detection complete. Detected: {bags_detected}")
#                 data[0] = 1  # 4 bags detected
#                 send_array(data)
#                 break  # Salir del bucle si se detectan 4 bolsas

#             time.sleep(2.5)  # Esperar antes de volver a intentar
        
#             annotated_frame = results[0].plot()  # Plot returns the frame with predictions drawn
#             cv2.imwrite('BagsImage.jpg', annotated_frame)
#     except Exception as e:
#         print(f"Error during bag detection: {e}")
#     finally:
#         cap.release()

def options():
    global running, data
    data = [0, 0, 0]
    selection = option.get()
    data[2] = selection
    print(f"Option selected: {options_text[selection - 1]}")

    submitBt.pack_forget()
    stopBt.pack(pady=30)

    running = True
    # threading.Thread(target=read_sensor_and_process, daemon=True).start()

def stop():
    global running
    running = False
    print("Stopping...")
    stopBt.pack_forget()
    submitBt.pack(pady=30)

def close():
    global running
    running = False
    print("Closing...")
    # sensor_box.close()
    # server_socket.close()
    # client_socket.close()
    window.destroy()

# Create the GUI
window = tk.Tk()
window.title("Coffee Selector")
window.attributes("-fullscreen", True)
window.configure(bg="white")

# Logo
logo = Image.open("logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(window, image=logo, bg="white")
logo_label.pack(pady=20)

# Title
title_label = tk.Label(window, text="Coffee Packing Selector", font=("Arial", 28, "bold"), bg="white", fg="black")
title_label.pack(pady=10)

# Option selection
option = tk.IntVar()
option.set(1)

options_text = ["0.25 Kg", "0.50 Kg", "1.0 Kg", "2.5 Kg"]

disabled_options = [2, 3]  # Indices of options to disable (500g and 1kg)

options_frame = tk.Frame(window, bg="white")
options_frame.pack(pady=20)

for i, text in enumerate(options_text, start=1):
    rb = tk.Radiobutton(
        options_frame,
        text=text,
        variable=option,
        value=i,
        font=("Arial", 18),
        bg="white",
    )
    if i in disabled_options:
        rb.config(state="disabled")
    rb.grid(row=i, column=0, sticky="w", padx=50, pady=10)

# Submit button
submitBt = tk.Button(window, text="Submit", command=options, font=("Arial", 18), bg="green", fg="white", width=10)
submitBt.pack(pady=20)

# Stop button
stopBt = tk.Button(window, text="Stop", command=stop, font=("Arial", 18), bg="red", fg="white", width=10)

# Exit button
exitBt = tk.Button(window, text="Exit", command=close, font=("Arial", 18), bg="gray", fg="white", width=10)
exitBt.pack(side="bottom", pady=30)

# Start the GUI loop
window.mainloop()
