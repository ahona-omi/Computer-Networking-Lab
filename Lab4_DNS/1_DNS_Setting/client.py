import socket
import struct
import time

ADDR = ('192.168.1.194', 4487)
SIZE = 1024
FORMAT = 'utf-8'


def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = input("Enter a message to send to the server: ")
        client.sendto(message.encode(FORMAT), ADDR)
        request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        msg, addr = client.recvfrom(SIZE)
        print('Received DNS Response Message in bytes:')
        print(msg)

        header = struct.unpack("6H", msg[:12])
        ms = msg[12:].decode('utf-8').split()
        print('\nDecoded DNS Response:')
        print("Header:", header)
        print("Request Time:", request_time)
        print("Domain Name:", ms[0])
        if len(ms) > 1:
            print("DNS Record:", ms[1])
            if len(ms) > 2:
                print("Additional Information:", ms[2])

    except Exception as e:
        print("Error occurred while communicating with the server:", e)


if __name__ == '__main__':
    main()
