# import tkinter as tk
# import socket
# import time
# import threading

# # Define TCP connection parameters
# UR10_IP = "192.168.0.43"
# PORT = 30000

# # Socket to act as a server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind socket to Raspberry Pi's IP and port
# s.bind(("192.168.0.80", PORT))
# s.listen(5)
# print("Server is listening for connections...")

# # Global variable to store the selected program
# program_value = 0
# bags_ready = 0
# box_ready = 0

# # Function to handle communication with the UR10
# def handle_client(clientsocket):
#     global program_value
#     while True:
#         # Send the current program state as a 3-element array
#         # For now, assume bags_ready and box_ready are always 1 for testing
#         data = [bags_ready, box_ready, program_value]
#         clientsocket.send(bytes(str(data), "ascii"))
#         time.sleep(1)  # Send data every second


# def button_pressed(weight):
#     global program_value
#     # Update program_value based on button pressed
#     if weight == "250g":
#         program_value = 250
#         print("You selected 250g!")
#     elif weight == "2.5kg":
#         program_value = 2.5
#         print("You selected 2.5kg!")
#     else:
#         print("Unsupported selection.")

# # Create the main window
# root = tk.Tk()
# root.title("Coffee Selector")
# root.geometry("300x300")

# # Create buttons
# button_250g = tk.Button(root, text="250g", command=lambda: button_pressed("250g"))
# button_250g.pack(pady=10)

# button_2_5kg = tk.Button(root, text="2.5kg", command=lambda: button_pressed("2.5kg"))
# button_2_5kg.pack(pady=10)

# # Start server in a separate thread
# def server_thread():
#     while True:
#         clientsocket, address = s.accept()
#         print(f"Connection from {address} has been established!")
#         threading.Thread(target=handle_client, args=(clientsocket,)).start()

# server_thread = threading.Thread(target=server_thread, daemon=True)
# server_thread.start()

# # Run the Tkinter application
# root.mainloop()

# import time
# from periphery import GPIO
# import tkinter as tk
# from PIL import Image, ImageTk
# import socket
# import cv2
# from ultralytics import YOLO
# import struct
# import threading

# # Define TCP connection parameters
# UR10_IP = "192.168.0.43"
# PORT = 30000

# # Socket to act as a server
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("192.168.0.80", PORT))  # IP address of the UP developer board
# server_socket.listen(1)

# print("Waiting for robot connection...")
# client_socket, client_address = server_socket.accept()
# print(f"Connected to robot: {client_address}")
# client_socket.setblocking(False)

# SENSOR_PIN = 23
# sensor_box = GPIO(SENSOR_PIN, "in")

# data = [0, 0, 0] # 4 bags ready, box ready, option
# client_socket.settimeout(0.1)

# model = YOLO("Coffee.pt")

# # Function to send data array to the robot
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

# # Function to read sensor data (box)
# def read_sensor():
#     global data
#     while running:
#         try:
#             data[1] = 1 if sensor_box.read() == 0 else 0
#             send_array(data)
#             time.sleep(0.1)
#         except Exception as e:
#             print(f"Error reading sensor: {e}")
#             break

# # Function to handle camera processing (placeholder)
# def camera():
#     global data
#     try:
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             print("Cannot access the camera.")
#             return

#         ret, frame = cap.read()

#         if not ret:
#             print("Cannot take picture.")
#             return

#         # Execute YOLO model on the frame
#         frame_resized = cv2.resize(frame, (640, 480))
#         results = model(frame_resized)

#         bags_detected = sum([1 for box in results[0].boxes if int(box.cls) == 0])

#         if bags_detected < 4:
#             print(f"Missing bags. Detected: {bags_detected}")
#             camera()
#         else:
#             print(f"Detection complete. Detected: {bags_detected}")
#             data[0] = 1 #4 bags detected
#             send_array(data)

#         annotated_frame = results[0].plot()  # Plot returns the frame with predictions drawn
#         cv2.imwrite('BagsImage.jpg', annotated_frame)

#     except Exception as e:
#         print(f"Error reading camera: {e}")
#     finally:
#         cap.release()

# # Function to handle option selection
# def options():
#     global option, running, data
#     data = [0, 0, 0]
#     selection = option.get()
#     data[2] = selection

#     submitBt.pack_forget()
#     stopBt.pack(pady=30)

#     running = True
#     threading.Thread(target=read_sensor).start()

# # Function to show box selection interface
# def selection():
#     boxSelection.pack_forget()
#     boxSelection.pack(fill="both", expand=True)

# # Function to stop the program
# def stop():
#     global running
#     running = False
#     print("Stopping...")
#     stopBt.pack_forget()
#     submitBt.pack(pady=30)

# # Function to close the program
# def close():
#     global running
#     running = False
#     print("Closing...")
#     sensor_box.close()
#     server_socket.close()
#     client_socket.close()
#     window.destroy()

# # Create the GUI
# window = tk.Tk()
# window.title("Coffee Selector")
# window.attributes("-fullscreen", True)
# window.configure(bg="white")

# # Logo
# logo = Image.open("logo.jpg")
# logo = ImageTk.PhotoImage(logo)
# logo_label = tk.Label(window, image=logo, bg="white")
# logo_label.pack(pady=10)

# # Title
# title_label = tk.Label(window, text="Coffee Packing Selector", font=("Arial", 24, "bold"), bg="white")
# title_label.pack(pady=10)

# # Option selection
# option = tk.IntVar()
# option.set(1)
# boxSelection = tk.Frame(window, bg="white")
# boxSelection.pack(fill="both", expand=True)

# for i in range(1, 4):
#     rb = tk.Radiobutton(
#         boxSelection,
#         text=f"Option {i}",
#         variable=option,
#         value=i,
#         font=("Arial", 16),
#         bg="white",
#     )
#     rb.pack(anchor="w", padx=20, pady=5)

# # Submit button
# submitBt = tk.Button(window, text="Submit", command=options, font=("Arial", 16), bg="green", fg="white")
# submitBt.pack(pady=30)

# # Stop button
# stopBt = tk.Button(window, text="Stop", command=stop, font=("Arial", 16), bg="red", fg="white")

# # Exit button
# exitBt = tk.Button(window, text="Exit", command=close, font=("Arial", 16), bg="gray", fg="white")
# exitBt.pack(side="bottom", pady=20)

# # Start the GUI loop
# window.mainloop()

import time
from periphery import GPIO
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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.0.80", PORT))  # IP address of the UP developer board
server_socket.listen(1)

print("Waiting for robot connection...")
client_socket, client_address = server_socket.accept()
print(f"Connected to robot: {client_address}")
client_socket.setblocking(False)

SENSOR_PIN = 23
sensor_box = GPIO(SENSOR_PIN, "in")

data = [0, 0, 0]  # 4 bags ready, box ready, option
client_socket.settimeout(0.1)

model = YOLO("Coffee.pt")

running = False

def send_array(data):
    try:
        packed_data = struct.pack(f'{len(data)}B', *data)
        client_socket.send(packed_data)
        print(f"Sent data: {data}")
    except Exception as e:
        print(f"Error sending data: {e}")
        sensor_box.close()
        server_socket.close()
        client_socket.close()

def read_sensor_and_process():
    global data, running
    while running:
        try:
            # Leer el estado del sensor
            box_ready = 1 if sensor_box.read() == 0 else 0
            data[1] = box_ready

            if box_ready == 1:
                print("Box is ready. Starting camera detection...")
                detect_bags()  # Ejecutar detección de bolsas
            else:
                print("Waiting for box to be ready...")

            send_array(data)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading sensor: {e}")
            break

def detect_bags():
    global data
    try:
        while running:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Cannot access the camera.")
                return

            ret, frame = cap.read()
            if not ret:
                print("Cannot take picture.")
                return

            # Ejecutar modelo YOLO en el frame
            frame_resized = cv2.resize(frame, (640, 480))
            results = model(frame_resized)

            bags_detected = sum([1 for box in results[0].boxes if int(box.cls) == 0])

            if bags_detected < 4:
                print(f"Missing bags. Detected: {bags_detected}. Retrying...")
            else:
                print(f"Detection complete. Detected: {bags_detected}")
                data[0] = 1  # 4 bags detected
                send_array(data)
                break  # Salir del bucle si se detectan 4 bolsas

            time.sleep(2.5)  # Esperar antes de volver a intentar
        
            annotated_frame = results[0].plot()  # Plot returns the frame with predictions drawn
            cv2.imwrite('BagsImage.jpg', annotated_frame)
    except Exception as e:
        print(f"Error during bag detection: {e}")
    finally:
        cap.release()

def options():
    global running, data
    data = [0, 0, 0]
    selection = option.get()
    data[2] = selection

    submitBt.pack_forget()
    stopBt.pack(pady=30)

    running = True
    threading.Thread(target=read_sensor_and_process, daemon=True).start()

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
    sensor_box.close()
    server_socket.close()
    client_socket.close()
    window.destroy()

# Create the GUI
window = tk.Tk()
window.title("Coffee Selector")
window.attributes("-fullscreen", True)
window.configure(bg="white")

# Logo
logo = Image.open("logo.jpg")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(window, image=logo, bg="white")
logo_label.pack(pady=10)

# Title
title_label = tk.Label(window, text="Coffee Packing Selector", font=("Arial", 24, "bold"), bg="white")
title_label.pack(pady=10)

# Option selection
option = tk.IntVar()
option.set(1)

for i in range(1, 4):
    rb = tk.Radiobutton(
        window,
        text=f"Option {i}",
        variable=option,
        value=i,
        font=("Arial", 16),
        bg="white",
    )
    rb.pack(anchor="w", padx=20, pady=5)

# Submit button
submitBt = tk.Button(window, text="Submit", command=options, font=("Arial", 16), bg="green", fg="white")
submitBt.pack(pady=30)

# Stop button
stopBt = tk.Button(window, text="Stop", command=stop, font=("Arial", 16), bg="red", fg="white")

# Exit button
exitBt = tk.Button(window, text="Exit", command=close, font=("Arial", 16), bg="gray", fg="white")
exitBt.pack(side="bottom", pady=20)

# Start the GUI loop
window.mainloop()
