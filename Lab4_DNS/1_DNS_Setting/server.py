import os
import socket
import threading
import struct
import time

IP = '192.168.1.194'
PORT = 4487
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
dic = {}


def handle_client(data, addr, server):
    try:
        request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[RECEIVED MESSAGE] {data} from {addr} at {request_time}.")

        data = data.split()
        print("Request Time:", request_time)
        domain_name = data[0]
        print("Domain Name:", domain_name)

        file1 = open('dns_records.txt', 'r')
        found = False
        for line in file1:
            line = line.split()
            name = line[0]
            value = line[1]
            type = line[2]
            ttl = line[3]
            if name == domain_name and type == data[1]:
                print('Found DNS Record')
                flag = 0
                q = 0
                a = 1
                auth_rr = 0
                add_rr = 0

                # Pack DNS header fields and message into the same buffer
                ms = (name + ' ' + value + ' ' + type + ' ' + ttl).encode('utf-8')
                packed_data = struct.pack(f"6H{len(ms)}s", 50, flag, q, a, auth_rr, add_rr, ms)

                server.sendto(packed_data, addr)
                found = True
                break

        if not found:
            # If no matching DNS record found, send an empty response
            print('No DNS Record Found')
            server.sendto(b'', addr)

    except Exception as e:
        print("Error occurred while handling client request:", e)


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #SOCK_DGRAM-> use UDP instead of TCP
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        try:
            data, addr = server.recvfrom(SIZE)
            data = data.decode(FORMAT)
            thread = threading.Thread(target=handle_client, args=(data, addr, server))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        except Exception as e:
            print("Error occurred while accepting client connection:", e)


if __name__ == "__main__":
    main()
