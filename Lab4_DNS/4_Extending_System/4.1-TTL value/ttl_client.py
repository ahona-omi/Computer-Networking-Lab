import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    query = "www.example.com"
    client_socket.send(query.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print("Response:", response)

    client_socket.close()

if __name__ == "__main__":
    main()
