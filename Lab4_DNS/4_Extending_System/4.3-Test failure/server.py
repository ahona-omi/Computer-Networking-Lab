import os
import socket
import threading
import struct

IP = ''
PORT = 4487
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
dic = {
    "www.google.com": ('100.20.8.1', 'A', 86400),
    "www.cse.du.ac.bd": ('100.20.55.2', 'A', 86400),
    "www.yahoo.com": ('100.20.89.7', "A", 86400)
}

# Variable to indicate whether the server is active or not
server_active = True

def encode_msg(message):
    data = message.split()
    name = data[0]
    type = data[1]

    flag = 0
    q = 0
    a = 1
    auth_rr = 0
    add_rr = 0

    ms = (name + ' ' + type + ' ' + data[2] + ' ' + data[3]).encode('utf-8')
    packed_data = struct.pack(f"6H{len(ms)}s", 50, flag, q, a, auth_rr, add_rr, ms)
    return packed_data

def decode_msg(msg):
    header = struct.unpack("6H", msg[:12])
    ms = msg[12:].decode('utf-8')
    return ms

def handle_client(data, addr, server):
    global server_active
    try:
        print(f"[RECEIVED MESSAGE] {data} from {addr}.")
        if data == "simulate_failure":
            print("Simulating server failure...")
            server_active = False
        elif data == "simulate_recovery":
            print("Simulating server recovery...")
            server_active = True
        else:
            if server_active:  # Check if the server is active
                if data in dic:
                    if dic[data][1] == 'A' or dic[data][1] == 'AAAA':
                        msg = encode_msg(str(data + ' ' + dic[data][0] + ' ' + dic[data][1] + ' ' + str(dic[data][2])))
                        server.sendto(msg, addr)
                else:
                    server.sendto(('error Server could not find the requested domain').encode(FORMAT), addr)
            else:
                print("Server is currently inactive. Cannot process requests.")
    except Exception as e:
        print("ERROR: ", str(e))
        server.sendto(('error ' + str(e)).encode(FORMAT), addr)

def main():
    global server_active
    print("[STARTING] ROOT Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] ROOT Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(SIZE)
        data = data.decode(FORMAT)
        handle_client(data, addr, server)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
