import socket


def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    print("Response:", response)
    client_socket.close()


def main():
    while True:
        print("\nMenu:")
        print("1. Convert to lowercase")
        print("2. Check prime or palindrome")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            data = input("Enter text to convert to lowercase: ")
            send_request(f"convert {data}")
        elif choice == '2':
            num = input("Enter number: ")
            operation = input("Enter operation (prime/palindrome): ")
            send_request(f"check {num} {operation}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()