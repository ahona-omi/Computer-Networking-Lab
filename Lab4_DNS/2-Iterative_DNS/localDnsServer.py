import socket
import struct

ROOT_DNS_ADDR = ('127.0.0.1', 4487)
TLD_DNS_ADDR = ('127.0.0.1', 4488)
AUTH_DNS_ADDR = ('127.0.0.1', 4489)

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

def resolve_domain(domain_name):
    try:
        # Query Root DNS Server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as root_server:
            root_server.sendto(domain_name.encode(), ROOT_DNS_ADDR)
            root_response, _ = root_server.recvfrom(1024)
            tld_addr = root_response.decode()

        # Query TLD DNS Server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as tld_server:
            tld_server.sendto(domain_name.encode(), TLD_DNS_ADDR)
            tld_response, _ = tld_server.recvfrom(1024)
            auth_addr = tld_response.decode()

        # Query Authoritative DNS Server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as auth_server:
            auth_server.sendto(domain_name.encode(), AUTH_DNS_ADDR)
            auth_response, _ = auth_server.recvfrom(1024)
            ip_address = auth_response.decode()

        return ip_address

    except Exception as e:
        print("Error occurred while resolving domain:", e)
        return None

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('localhost', 5000))

        print("[LISTENING] Local DNS Server is listening on port 5000...")

        while True:
            data, addr = server.recvfrom(1024)
            domain_name = data.decode()
            print(f"[RECEIVED QUERY] {domain_name} from {addr}")

            # Resolve domain iteratively
            ip_address = resolve_domain(domain_name)

            if ip_address:
                # Send IP address to client
                server.sendto(ip_address.encode(), addr)
                print(f"Sent IP address of {domain_name} to {addr}")

    except Exception as e:
        print("Error occurred in main:", e)

if __name__ == "__main__":
    main()
