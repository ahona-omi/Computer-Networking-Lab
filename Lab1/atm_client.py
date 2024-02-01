import socket
import random
import time

def random_error(error_rate):
    return random.randint(1, 100) <= error_rate

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5020))

    if random_error(20):  # Adjust the error rate as needed (10% error rate in this example)
        print("Simulating random error.")
        response = "ERROR"
    else:
        client_socket.send(request.encode())
        response = client_socket.recv(1024).decode()

    print("Response from bank server:", response)
    client_socket.close()

send_request.last_error_time = time.time()  # Initialize the last error time

def main():
    while True:
        print("\nMenu:")
        print("1. Verify Card and Password")
        print("2. Balance Inquiry")
        print("3. Withdraw Money")
        print("4. Create Account")
        print("5. Deposit Money")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            card_number = input("Enter card number: ")
            password = input("Enter password: ")
            send_request(f"VERIFY_CARD_AND_PASSWORD {card_number} {password}")
        elif choice == '2':
            card_number = input("Enter card number: ")
            send_request(f"BALANCE_INQUIRY {card_number}")
        elif choice == '3':
            card_number = input("Enter card number: ")
            amount = input("Enter amount to withdraw: ")
            send_request(f"WITHDRAW {card_number} {amount}")
        elif choice == '4':
            card_number = input("Enter new card number: ")
            password = input("Enter password for new account: ")
            initial_balance = input("Enter initial balance: ")
            send_request(f"CREATE_ACCOUNT {card_number} {password} {initial_balance}")
        elif choice == '5':
            card_number = input("Enter card number: ")
            amount = input("Enter amount to deposit: ")
            send_request(f"DEPOSIT {card_number} {amount}")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
