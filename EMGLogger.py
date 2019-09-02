
# --- STRUCTURE OF INCOMING TCP SOCKET DATASTREAM FROM THE SESSNATAQUATTRO ---

# The data generated from sessantaquattro is just a continous strem of value
# on 16 bits with sign (int16). You receive sequencially the channels you
# have configured, for example, if you set 8 EMG channels the firts 2 bytes
# are the first sample of CH1, bytes 3 and 4 are the first sample of CH2 ...
# bytes 15 and 16 are the fisrt sample of CH8 and then you still have 4 bytes
# for the 2 aux channels and 4 bytes for the two accessory channels. After 24
# bytes everything is repeated for the sample 2 and so on

import socket
import struct
import sys
import numpy as np
from bitstring import BitArray

print("Starting")

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder = 'big')

def bytes_to_bitstring(s):
    integer = int.from_bytes(s, byteorder='big')
    bits = '{0:08b}'.format(integer)
    return bits

def bytes_to_integer(s):
    integer = int.from_bytes(s, byteorder='big')
    return integer

TCP_IP = '0.0.0.0'
TCP_PORT = 45454
buffer_size = 240

# Command string can be built from microsoft word documentation
bTestCommand = b"0100000101000001"
TestCommand = "0100000101000001"
TestCommandBytes = bitstring_to_bytes(TestCommand)

bStopCommand = b"0100000101000000"
StopCommand = "0100000101000000"
StopCommandBytes = bitstring_to_bytes(StopCommand)

print("Creating server")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server binding")
s.bind((TCP_IP, TCP_PORT))
print("Server listening")
s.listen(1)

conn, addr = s.accept()
print("Connection address: {}".format(addr))
print("Connected")
# If connected, LED blinks 3 times

conn.send(TestCommandBytes)
# If successfully sent valid command, data starts
# streaming and LED blinks 4 times

print(TestCommand + " sent")

for i in range(1000):
    print(i)
    rawDataStream = conn.recv(buffer_size) #Originally buffer size of 1024 for some reason
    #Should be integer multiple of bytes per sample

    print(rawDataStream)

    data = np.zeros((12, int(buffer_size/24))) #8 + 4 channels

    for timeStep in range(int(buffer_size/24)):
        samples = rawDataStream[timeStep:timeStep+24]

        for channel in range(12):
            sample = samples[channel:channel+2]
            data[channel, timeStep] = bytes_to_integer(sample)

    print(data)

conn.send(StopCommandBytes)
# This is required to make sure the socket
# doesn't "Hang" on the sessantaquattro side

s.close()
