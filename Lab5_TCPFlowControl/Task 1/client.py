import socket
import struct

def make_packet(seq, ack, window):
    transport_header = struct.pack("!III", seq, ack, window)
    network_header = b'\x45\x00\x05\xdc'  # IP version 4, header length 20 bytes, total length 1500 bytes
    network_header += b'\x00\x00\x00\x00'  # Identification
    network_header += b'\x40\x06\x00\x00'  # TTL=64, protocol=TCP, checksum=0 (will be filled in by kernel)
    network_header += b'\x0a\x00\x00\x01'  # Source IP address
    network_header += b'\x0a\x00\x00\x02'  # Destination IP address
    packet = network_header + transport_header
    return packet

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8082))
print('Connected to server')

# Buffer
max_buffer_size = 1465 * 20  # 10 MB buffer size
data_buffer = b''

try:
    # Receive packets and write to file
    with open('received_file.txt', 'wb') as file:
        expected_sequence_number = 0
        while True:
            # Receive packet from server
            packet = client_socket.recv(1500)
            if not packet:
                break

            # Parsing packet
            _, ack, _ = struct.unpack("!III", packet[20:32])
            ack = ack - expected_sequence_number

            if ack > 0:
                data_buffer += packet[40:]
                expected_sequence_number += ack

                if len(data_buffer) >= max_buffer_size:
                    file.write(data_buffer)
                    data_buffer = b''

                # Construct acknowledgment packet
                ack_packet = make_packet(0, expected_sequence_number, max_buffer_size - len(data_buffer))
                client_socket.send(ack_packet)  # Send acknowledgment packet to the server

except Exception as e:
    print(f"Error: {e}")

# Write remaining data to file
if data_buffer:
    with open('received_file.txt', 'ab') as file:
        file.write(data_buffer)

client_socket.close()
print('Done')
