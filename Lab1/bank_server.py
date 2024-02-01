import random
import socket
import time

# Dummy database for card and balance information
database = {
    "123456789": {"name": "Joty", "password": "1234", "balance": 10000},
    "987654321": {"name": "Ahona", "password": "5678", "balance": 5000}
}

def verify_card_and_password(card_number, password):
    if card_number in database and database[card_number]["password"] == password:
        return True
    else:
        return False

def get_balance(card_number):
    return database[card_number]["balance"]

def withdraw_money(card_number, amount):
    if amount <= 0:
        return False, "WITHDRAW_ACK FAILURE Invalid amount"

    if database[card_number]["balance"] >= amount:
        database[card_number]["balance"] -= amount
        return True, f"WITHDRAW_ACK SUCCESS Withdrawn {amount} successfully"
    else:
        return False, "WITHDRAW_ACK FAILURE Insufficient funds"

def create_account(card_number, name, password, initial_balance):
    if card_number not in database:
        database[card_number] = {"name": name, "password": password, "balance": initial_balance}
        return True
    else:
        return False

def deposit_money(card_number, amount):
    if amount <= 0:
        return False, "DEPOSITE_ACK FAILURE Invalid amount"

    database[card_number]["balance"] += amount
    return True, "DEPOSIT_ACK SUCCESS Amount deposited successfully"

def random_error(error_probability):
    return random.random() <= error_probability

def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    request_data = request.split()
    response = ""

    if random_error(0.2):  # Adjust the probability as needed
        error_time = time.time()  # Record the time when the error occurs
        response = "ERROR_ACK Random error occurred"
        # Calculate and print the time in seconds for the error
        print("Error occurred at:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(error_time)))
    else:
        if request_data[0] == "VERIFY_CARD_AND_PASSWORD":
            card_number, password = request_data[1], request_data[2]
            if verify_card_and_password(card_number, password):
                response = "VERIFY_ACK SUCCESS"
            else:
                response = "VERIFY_ACK FAILURE"

        elif request_data[0] == "BALANCE_INQUIRY":
            card_number = request_data[1]
            balance = get_balance(card_number)
            response = f"BALANCE_ACK {balance}"


        elif request_data[0] == "WITHDRAW":
            card_number, amount = request_data[1], int(request_data[2])
            success, message = withdraw_money(card_number, amount)
            response = message if success else message


        elif request_data[0] == "CREATE_ACCOUNT":
            card_number, name, password, initial_balance = request_data[1], request_data[2], request_data[3], int(request_data[4])
            if create_account(card_number, name, password, initial_balance):
                response = "CREATE_ACCOUNT_ACK SUCCESS Account created successfully"
            else:
                response = "CREATE_ACCOUNT_ACK FAILURE Account already exists"

        elif request_data[0] == "DEPOSIT":
            card_number, amount = request_data[1], int(request_data[2])
            success, message = deposit_money(card_number, amount)
            response = message if success else message

    client_socket.send(response.encode())
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5020))
    server_socket.listen(5)

    print("Bank server listening on port 5050...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from ATM booth: {addr[0]}:{addr[1]}")
        handle_client_connection(client_socket)

if __name__ == "__main__":
    main()
