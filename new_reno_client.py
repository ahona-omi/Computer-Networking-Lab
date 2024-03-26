import socket
import random
import time

# Define global variables
cwnd = 1
ssthresh = 8
dup_ack_count = 0
last_ack_number = -1
last_sequence_number = -1
tim_out = 5
est_rtt = 0.5
sample_rtt = 0.5
alpha = 0.125
beta = 0.25
dev_rtt = 0.5


def congestion_avoidance(curr_cwnd):
    return curr_cwnd + 1


def slow_start(curr_cwnd):
    return curr_cwnd * 2


def fast_retransmit(curr_cwnd):
    return curr_cwnd // 2


def fast_recovery(curr_cwnd):
    return curr_cwnd + 3  # Increase the congestion window by 3 in fast recovery phase


def trans_layer_decode(packet):
    seq = packet[:6]
    ack = packet[6:12]
    win = packet[12:16]
    check = packet[16:20]
    return (int(seq.decode('utf-8')), int(ack.decode('utf-8')), int(win.decode('utf-8')), int(check.decode('utf-8')))


def make_packet(seq, ack, window, checksum, payload):
    seq = int(seq)
    ack = int(ack)
    window = int(window)
    checksum = int(checksum)
    transport_header = f'{seq:06d}{ack:06d}{window:04d}{checksum:04d}'.encode('utf-8')[:20].ljust(20)

    # Build network layer header
    network_header = b'\x45\x00\x05\xdc'  # IP version 4, header length 20 bytes, total length 1500 bytes
    network_header += b'\x00\x00\x00\x00'  # Identification
    network_header += b'\x40\x06\x00\x00'  # TTL=64, protocol=TCP, checksum=0 (will be filled in by kernel)
    network_header += b'\x0a\x00\x00\x01'  # Source IP address
    network_header += b'\x0a\x00\x00\x02'  # Destination IP address

    # Build packet by concatenating headers and payload
    packet = network_header + transport_header + payload
    return packet


# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.110', 8882))
client_socket.settimeout(5)

# Set receive window size (in bytes)
receive_window_size = 1460
rwnd = 5
mss = 1460

# Open file to be sent
file = open('receiving_file.txt', 'wb')

while True:
    try:
        data = client_socket.recv(1500)
    except socket.timeout:
        print('No data received within 5 seconds')
        break

    if data:
        # Parse received packet
        network_header = data[:20]
        transport_header = data[20:40]
        payload = data[40:]
        server_seq, client_ack, rwnd, checksum = trans_layer_decode(transport_header)

        if server_seq == client_ack:
            # Send acknowledgment
            ack_packet = make_packet(server_seq, client_ack + len(payload), rwnd, checksum, b'')
            client_socket.send(ack_packet)

            # Write payload to file
            file.write(payload)

            print(f'Received packet with sequence number {server_seq} and acknowledged with {client_ack}')

        else:
            print(f'Received packet with sequence number {server_seq}, but expected {client_ack}')
    else:
        print('Connection closed by server')
        break

# Close file
file.close()

# Close socket
client_socket.close()
print('Done')
