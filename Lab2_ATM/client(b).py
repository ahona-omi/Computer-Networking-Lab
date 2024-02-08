import socket

HEADER = 64
PORT = 5040
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    client.send(username.encode(FORMAT))
    client.send(password.encode(FORMAT))
    response = client.recv(1024).decode(FORMAT)
    if response == "LOGIN_SUCCESS":
        print("Logged in successfully!")
        atm_operations(username)
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response = client.recv(2048).decode(FORMAT)
    print(f"[SERVER RESPONSE] {response}")

def atm_operations(username):
    while True:
        user_input = input("Enter command (BALANCE, WITHDRAW <amount>, DEPOSIT <amount>) or 'quit' to disconnect: ")
        if user_input == "quit":
            send(DISCONNECT_MSG)
            break
        # Prepend the username to the user_input before sending
        full_input = f"{username} {user_input}"
        send(full_input)


login()