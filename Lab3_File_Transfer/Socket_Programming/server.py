import socket
import os
import time
from threading import Thread

IP = "127.0.0.1"
port = 3381
ADDR = (IP, port)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected...")

    # Get the list of files in the server directory
    files = os.listdir('.')
    file_list = '\n'.join(files)

    # Print the list of files available
    # print("List of files available for download:")
    # for file_name in files:
    #     print(file_name)

    # Send the file list to the client
    conn.send(file_list.encode())

    conn.send("Enter the filename you want to download: ".encode())
    filename = conn.recv(1024).decode()
    file_path = os.path.join("/home/asus/Documents/Python/NetworkingLab/Lab2_File_Transfer/Socket_Programming", filename)

    if os.path.exists(file_path):
        download_time = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(file_path, "rb") as file:
            data = file.read()

        conn.sendall(data)
        print(f"[SENT] File '{filename}' sent to {addr}  at {download_time}.")
    else:
        conn.send("File not found.".encode())

    print(f"[DISCONNECTED] {addr} disconnected...")
    conn.close()

def start_server():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP} : {port}...")

    while True:
        conn, addr = server.accept()
        client_handler = Thread(target=handle_client, args=(conn, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()