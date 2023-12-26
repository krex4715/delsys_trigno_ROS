import struct
import time
import socket
import numpy as np

EMG_IP = "192.168.50.226"
EMG_COMMAND_PORT = 50040
EMG_STREAM_PORT = 50043

emgCommandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
emgCommandSocket.connect((EMG_IP, EMG_COMMAND_PORT))
emgStreamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
emgStreamSocket.connect((EMG_IP, EMG_STREAM_PORT))

emgCommandSocket.sendall(b'START')
emgCommandSocket.sendall(b'TRIGGER START\r\n\r\n')
startTime = time.time()

def receive_full_packet(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

try:
    while True:
        emgData = receive_full_packet(emgStreamSocket, 64)
        if emgData is None:
            print("Connection closed.")
            break
        if len(emgData) == 64:
            emgArray = np.array(struct.unpack("<16f", emgData))
            print('time: ', time.time() - startTime)
            print(emgArray.tolist())
        else:
            print("Received incomplete packet.")
except KeyboardInterrupt:
    print("Streaming stopped by user.")

emgCommandSocket.sendall(b'STOP')
emgCommandSocket.close()
emgStreamSocket.close()
