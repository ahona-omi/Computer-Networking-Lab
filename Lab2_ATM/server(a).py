import socket


def convert_to_lowercase(data):
    return data.lower()


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def is_palindrome(num):
    return str(num) == str(num)[::-1]


def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    request_data = request.split()

    if request_data[0] == 'convert':
        response = convert_to_lowercase(request_data[1])
    elif request_data[0] == 'check':
        num = int(request_data[1])
        operation = request_data[2]
        if operation == 'prime':
            response = 'Prime' if is_prime(num) else 'Not Prime'
        elif operation == 'palindrome':
            response = 'Palindrome' if is_palindrome(num) else 'Not Palindrome'
    else:
        response = 'Invalid request'

    client_socket.send(response.encode())
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1234))
    server_socket.listen(5)

    print("Server listening on port 1234...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        handle_client_connection(client_socket)


if __name__ == "__main__":
    main()