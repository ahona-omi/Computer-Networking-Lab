import socket
import random
import struct
import os

def trans_layer_decode(packet):
    seq, ack, win = struct.unpack("!III", packet[:12])
    return seq, ack, win

def make_packet(seq, ack, window):
    transport_header = struct.pack("!III", seq, ack, window)
    network_header = b'\x45\x00\x05\xdc'  # IP version 4, header length 20 bytes, total length 1500 bytes
    network_header += b'\x00\x00\x00\x00'  # Identification
    network_header += b'\x40\x06\x00\x00'  # TTL=64, protocol=TCP, checksum=0 (will be filled in by kernel)
    network_header += b'\x0a\x00\x00\x02'  # Source IP address
    network_header += b'\x0a\x00\x00\x01'  # Destination IP address
    packet = network_header + transport_header
    return packet

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8082))
server_socket.listen(1)
print('Server is listening for incoming connections')

# Accept a client connection
client_socket, address = server_socket.accept()
print(f'Accepted connection from {address}')

# Set receive window size (in bytes)
receive_window_size = 1460
rwnd = receive_window_size

# Open file to be sent
file = open('sending_file.txt', 'rb')
file_size = os.path.getsize('sending_file.txt')

# Send packet with transport and network layer headers
sequence_number = random.randint(0, 0)
ack_number = 0

while True:
    payload = file.read(1460)
    payload_size = len(payload)
    ack_number += payload_size
    if not payload:
        break
    packet = make_packet(sequence_number, ack_number, rwnd)
    sequence_number += len(payload)
    client_socket.send(packet)

    # Wait for acknowledgment from client
    acknowledgment = client_socket.recv(1024)
    if acknowledgment:
        # Parse acknowledgment
        _, acknowledgment_sequence_number, _ = trans_layer_decode(acknowledgment[20:32])

        # Check if all packets up to and including the acknowledged packet have been received
        if acknowledgment_sequence_number == sequence_number:
            print(f'Received acknowledgment for packet {sequence_number}')
        else:
            print(f'Received acknowledgment for packet {acknowledgment_sequence_number}, but expected {sequence_number}')
    else:
        print('Did not receive acknowledgment')

# Close file
file.close()

# Close sockets
client_socket.close()
server_socket.close()
print('Done')
