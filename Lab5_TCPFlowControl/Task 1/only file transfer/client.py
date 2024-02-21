import socket

def send_file(client_socket, filename):
    with open(filename, "rb") as f:
        for data in f:
            client_socket.sendall(data)  # Send data

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print('Connected to server')

    # Set cumulative acknowledgment
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    send_file(client_socket, "sending_file.txt")

    client_socket.close()

if __name__ == "__main__":
    main()
