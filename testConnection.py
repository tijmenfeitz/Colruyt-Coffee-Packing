import socket

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

    while True:
        # Receive a message with expected byte length of 1024 byte
        msg = clientsocket.recv(1024) 
        if not msg:  # If no message is received, break the loop
            break

        # Decode message to utf-8 format 
        print(msg.decode("utf-8"))

        # Send floating point number
        message_to_send = "(1.2, 1.3, 1.4)"
        clientsocket.send(bytes(message_to_send, "ascii"))

    # Close the client socket
    clientsocket.close()