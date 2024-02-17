import socket
import struct

ROOT_DNS_ADDR = ('127.0.0.1', 4487)


def encode_msg(message):
    try:
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
    except Exception as e:
        print("Error occurred while encoding message:", e)
        return None


def resolve_domain(domain_name, server_addr):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns_server:
            dns_server.sendto(domain_name.encode(), server_addr)
            response, _ = dns_server.recvfrom(1024)
            return response.decode(), server_addr[1]

    except Exception as e:
        print("Error occurred while resolving domain:", e)
        return None, None


def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('localhost', 5000))

        print("[LISTENING] Local DNS Server is listening on port 5000...")

        while True:
            try:
                data, addr = server.recvfrom(1024)
                domain_name = data.decode()
                print(f"[RECEIVED QUERY] {domain_name} from {addr[0]} for target {addr[1]}")

                ip_address, port = resolve_domain(domain_name, ROOT_DNS_ADDR)

                if ip_address and port:
                    server.sendto(ip_address.encode(), addr)
                    print(f"Sent IP address of {domain_name} to {addr}")

            except Exception as e:
                print("Error occurred in query processing:", e)

    except KeyboardInterrupt:
        print("Server terminated by user.")
    except Exception as e:
        print("Error occurred in main:", e)
    finally:
        server.close()


if __name__ == "__main__":
    main()
