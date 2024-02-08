import socket
import os

IP = "127.0.0.1"
port = 3381
ADDR = (IP, port)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Receive prompt for filename from the server
    prompt = client.recv(1024).decode()
    print("List of files available for download from [SERVER]:")
    print(f"{prompt}")

    # Receive list of files from server
    file_list = client.recv(1024).decode()

    print(file_list)

    # Get the filename from the user
    filename = input()
    client.send(filename.encode())

    # Receive file data from the server
    data = b""
    while True:
        chunk = client.recv(1024)
        if not chunk:
            break
        data += chunk

    # Check if the server sent an error message
    if data == b"File not found.":
        print(f"[SERVER]: File not found.")
    else:
        # Save the received data to a file
        with open(f"downloaded_{filename}", "wb") as file:
            file.write(data)

        file_size_bytes = os.path.getsize(f"downloaded_{filename}")
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"[SERVER]: File '{filename}' downloaded successfully. Size: {file_size_mb:.2f} MB")

    client.close()


if __name__ == "__main__":
    main()