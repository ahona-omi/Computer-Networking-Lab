import socket

def receive_file(server_socket, filename):
    with open(filename, "wb") as f:
        while True:
            data = server_socket.recv(1024)  # Receive data
            if not data:
                break
            f.write(data)  # Write received data to file

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)

    print("Server listening...")

    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")

    # Set receive window size
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*64)

    receive_file(client_socket, "received_file.txt")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
