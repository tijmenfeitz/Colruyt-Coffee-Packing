import socket

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