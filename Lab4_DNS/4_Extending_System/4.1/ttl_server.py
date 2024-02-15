import socket
import threading
import time

class DNSRecord:
    def __init__(self, name, value, record_type, ttl):
        self.name = name
        self.value = value
        self.record_type = record_type
        self.ttl = ttl
        self.creation_time = time.time()

    def is_expired(self):
        return (time.time() - self.creation_time) > self.ttl

class DNSServer:
    def __init__(self):
        self.records = {}
        self.deleted_records = {}  # To store deleted records
        self.cleanup_interval = 10  # Cleanup interval in seconds
        self.cleanup_thread = threading.Thread(target=self.cleanup_records)
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()

    def add_record(self, name, value, record_type, ttl):
        self.records[name] = DNSRecord(name, value, record_type, ttl)

    def get_record(self, name):
        record = self.records.get(name)
        if record and not record.is_expired():
            return record.value
        else:
            return None

    def cleanup_records(self):
        while True:
            expired_records = [name for name, record in self.records.items() if record.is_expired()]
            for name in expired_records:
                # Move expired record to deleted_records
                self.deleted_records[name] = self.records.pop(name)
                print(f"Record {name} deleted due to TTL expiration")
            time.sleep(self.cleanup_interval)

def handle_client(client_socket, dns_server):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        response = dns_server.get_record(request)
        if response:
            client_socket.send(response.encode('utf-8'))
        else:
            client_socket.send(b'Record not found')
    client_socket.close()

def main():
    dns_server = DNSServer()
    dns_server.add_record("www.example.com", "192.168.1.100", "A", ttl=5)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)

    print("DNS Server running...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected to", addr)
        threading.Thread(target=handle_client, args=(client_socket, dns_server)).start()

if __name__ == "__main__":
    main()
