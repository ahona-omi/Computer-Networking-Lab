import socket
import threading

# Constants
HEADER = 64
PORT = 5040
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
ACCOUNTS = {'ahona': {'password': '1234', 'balance': 1000}}

# Socket setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Functions
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    authenticated = False
    while not authenticated:
        # Receive username and password
        username = conn.recv(1024).decode(FORMAT)
        password = conn.recv(1024).decode(FORMAT)

        # Validate username and password
        if username in ACCOUNTS and ACCOUNTS[username]['password'] == password:
            authenticated = True
            conn.send("LOGIN_SUCCESS".encode(FORMAT))
            print(f"[{username}] Authenticated successfully.")
        else:
            conn.send("LOGIN_FAIL".encode(FORMAT))

    while authenticated:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                authenticated = False
            else:
                handle_request(conn, msg)

    conn.close()

def handle_request(conn, msg):
    try:
        command, *args = msg.split()
        if command == "BALANCE":
            if len(args) == 1:
                card_number = args[0]
                if card_number in ACCOUNTS:
                    conn.send(f"BALANCE_RESPONSE {ACCOUNTS[card_number]['balance']}".encode(FORMAT))
                else:
                    conn.send("INVALID_REQUEST".encode(FORMAT))
            else:
                conn.send("INVALID_REQUEST".encode(FORMAT))

        elif command == "WITHDRAW":
            if len(args) == 2:
                card_number, amount = args
                if card_number in ACCOUNTS and int(amount) > 0 and int(amount) <= ACCOUNTS[card_number]['balance']:
                    ACCOUNTS[card_number]['balance'] -= int(amount)
                    conn.send(f"WITHDRAW_SUCCESS {ACCOUNTS[card_number]['balance']}".encode(FORMAT))
                else:
                    conn.send("WITHDRAW_FAIL".encode(FORMAT))
            else:
                conn.send("INVALID_REQUEST".encode(FORMAT))

        elif command == "DEPOSIT":
            if len(args) == 2:
                card_number, amount = args
                if card_number in ACCOUNTS and int(amount) > 0:
                    ACCOUNTS[card_number]['balance'] += int(amount)
                    conn.send(f"DEPOSIT_SUCCESS {ACCOUNTS[card_number]['balance']}".encode(FORMAT))
                else:
                    conn.send("DEPOSIT_FAIL".encode(FORMAT))
            else:
                conn.send("INVALID_REQUEST".encode(FORMAT))

        else:
            conn.send("INVALID_REQUEST".encode(FORMAT))
    except Exception as e:
        print(f"Error handling request: {e}")
        conn.send("INVALID_REQUEST".encode(FORMAT))



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting... ")
start()
