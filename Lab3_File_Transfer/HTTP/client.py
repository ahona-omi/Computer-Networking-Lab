import os

import requests
import mimetypes


def list_files():
    file_list = requests.get('http://localhost:8080/').text
    print("Available files for download or posting:")
    print(file_list)


def get_file():
    list_files()
    fil = input('Enter File Name: ')

    response = requests.get(f'http://localhost:8080/{fil}')

    if response.status_code == 200:
        # Prompt the user for the name to save the file as
        filename = input("Enter the name to save the file as (including extension): ")
        with open(filename, "wb") as f:
            f.write(response.content)
            file_size_bytes = os.path.getsize(filename)
            file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"[SERVER]: File '{filename}' downloaded successfully. Size: {file_size_mb:.2f} MB")
    else:
        print("Error: Could not receive file")


def post_file():
    list_files()
    file_path = input('Enter File Path for Posting: ')

    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return

    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post('http://localhost:8080/', files=files)

    if response.status_code == 200:
        print("File successfully posted")
    else:
        print(f"Error: Could not post file. Server response: {response.status_code}")
        print(response.text)  # Print out the response content for debugging




def main():
    choice = input("Choose operation (1 for GET, 2 for POST): ")

    if choice == '1':
        get_file()
    elif choice == '2':
        post_file()
    else:
        print("Invalid choice. Please choose 1 for GET, 2 for POST.")


if __name__ == '__main__':
    main()
