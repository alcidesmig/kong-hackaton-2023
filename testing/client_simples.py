import socket
import dl_translate as dlt

# Instantiate translation model
mt = dlt.TranslationModel()

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 12345
server_socket.bind((host, port))
server_socket.listen(1)  # Listen for one incoming connection

print(f"Server listening on {host}:{port}")
while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print(f"Received data from client: {data}")

    # Process data (e.g., perform some operation)
    response = mt.translate(data, source="Portuguese", target="English")

    print("Translate: ", response.encode())

    # Send a response back to the client
    print("Sending response...")
    print(client_socket.send(response.encode()+b"\n"))

from time import sleep
sleep(5)
# Close the sockets
client_socket.close()
server_socket.close()

