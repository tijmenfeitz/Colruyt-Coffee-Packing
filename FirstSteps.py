import tkinter as tk
import socket
import time

# Define TCP connection parameters
UR10_IP = "192.168.0.43"
PORT = 30000

# Socket to act as a server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to your device's ip and port, port can be anything above 1024 
# You can't use port that used by other process
s.bind(("192.168.0.42", 30000))

s.listen(5)
print("Server is listening for connections...")

while True:
    # Accept a connection from a client
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")


    # Create the main window
    root = tk.Tk()
    root.title("Coffee")

    # Set the size of the window
    root.geometry("200x100")

    def button_pressed(weight):
    # If statements to check which button was pressed
        if weight == "250g":
            print("You selected 250g!")
            clientsocket.send(bytes("(250)", "ascii"))
        elif weight == "2,5kg":
            print("You selected 2,5kg!")
            clientsocket.send(bytes("(2.5)", "ascii"))
        else:
            print("Unknown selection.")

    # Create buttons
    button_250g = tk.Button(root, text="250g", command=lambda: button_pressed("250g"))
    button_250g.pack(pady=10)

    button_2_5kg = tk.Button(root, text="2,5kg", command=lambda: button_pressed("2,5kg"))
    button_2_5kg.pack(pady=10)

    # Run the application
    root.mainloop()
