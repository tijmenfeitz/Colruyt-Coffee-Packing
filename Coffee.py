import time
from periphery import GPIO
import tkinter as tk
from PIL import Image, ImageTk
import socket
import cv2
from ultralytics import YOLO
import struct
import threading
import subprocess

# Define TCP connection parameters
UR10_IP = "192.168.0.43"
PORT = 30000

# Socket to act as a server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.0.185", PORT))  # IP address of the UP developer board
server_socket.listen(1)

print("Waiting for robot connection...")
client_socket, client_address = server_socket.accept()
print(f"Connected to robot: {client_address}")
client_socket.setblocking(False)

SENSOR_PIN = 23
sensor_box = GPIO(SENSOR_PIN, "in")

data = [0, 0, 0]  # 4 bags ready, box ready, option
client_socket.settimeout(0.1)

model = YOLO("coffee.pt")

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

def read_sensor():
    global data, running
    try:
        global data
        data[1] = 1 if sensor_box.read() == 0 else 0
    except BlockingIOError:
        pass


def detect_bags():
    global data
    print("inside detect")
    print("", data)
    
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

            frame_resized = cv2.resize(frame, (640, 480))
            results = model(frame_resized)
          
            bags_detected = sum([1 for box in results[0].boxes if int(box.cls) == 0])
         
            if data[2] == 1:
                if bags_detected < 10:
                    print(f"Missing bags. Detected: {bags_detected}. Retrying...")
                    data[0] = 0
                else:
                    print(f"Detection complete. Detected: {bags_detected}")
                    data[0] = 1  # 4 bags detected
                    send_array(data)
                    break
                    
            if data[2] == 4:
                if bags_detected < 4:
                    print(f"Missing bags. Detected: {bags_detected}. Retrying...")
                    data[0] = 0
                else:
                    print(f"Detection complete. Detected: {bags_detected}")
                    data[0] = 1  # 4 bags detected
                    send_array(data)
                    break
                            
            time.sleep(2.5)    
            annotated_frame = results[0].plot()  # Plot returns the frame with predictions drawn
            cv2.imwrite('BagsImage.jpg', annotated_frame)
            
    except Exception as e:
        print(f"Error during bag detection: {e}")
    finally:
        cap.release()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
def wait_for_robot_signal():
    global received_value
    while running:  
        try:
            final = client_socket.recv(1)
            if final:  
                received_value = struct.unpack('B', final)[0]  
                print(f"Received data from robot: {received_value}")

                if received_value == 99:  
                    print("Robot sent reset signal. Calling servo script...")
                    
                    subprocess.run(["python3", "servo.py"], check=True)
                    
                    received_value = 0
                    return
        except socket.timeout:
            pass 
        except Exception as e:
            print(f"Error while waiting for robot signal: {e}")
            break


def main_loop():
    global data
    while running:
        read_sensor()
        detect_bags()

        if data[0] == 1 and data[1] == 1:
            print("Ready to pack")
            send_array(data)

            print("Waiting for reset signal from robot...")
            wait_for_robot_signal()  
            
            data = [0, 0, data[2]]
            send_array(data)  
            print("System reset completed.")

def options():
    global running, data
    data = [0, 0, 0]
    selection = option.get()
    data[2] = selection
    print(f"Option selected: {options_text[selection - 1]}")

    submitBt.pack_forget()
    stopBt.pack(pady=30)

    running = True
    threading.Thread(target=main_loop, daemon=True).start()

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

# University logo (top-left corner)
uni_logo = Image.open("uniLogo.png")
uni_logo = uni_logo.resize((200, 70), Image.Resampling.LANCZOS)  
uni_logo = ImageTk.PhotoImage(uni_logo)
uni_logo_label = tk.Label(window, image=uni_logo, bg="white")
uni_logo_label.place(x=10, y=10)  

# Company Logo (centered)
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
