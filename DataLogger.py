import socket
from pynput import keyboard
import time
print("Starting")

#---------SETUP KEYLOGGER PART

pressed = 0

def on_press(key):
    global pressed
    try:
        pressed = 1
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global pressed
    pressed = 0
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False



#---------SETUP EMG PART
FSAMP = 2      # if MODE != 3: 0 = 500 Hz,  1 = 1000 Hz, 2 = 2000 Hz
                # if MODE == 3: 0 = 2000 Hz, 1 = 4000 Hz, 2 = 8000 Hz
NCH  = 0       # 0 = 8 channels, 1 = 16 channels, 2 = 32 channels, 3 = 64 channels
MODE = 1       # 0 = Monopolar, 1 = Bipolar, 2 = Differential, 3 = Accelerometers, 6 = Impedance check, 7 = Test Mode
HRES = 1       # 0 = 16 bits, 1 = 24 bits
HPF  = 0       # 0 = DC coupled, 1 = High pass filter active
EXTEN = 0      # 0 = standard input range, 1 = double range, 2 = range x 4, 3 = range x 8
TRIG = 0       # 0 = Data transfer and REC on SD controlled remotely, 3 = REC on SD controlled from the pushbutton
GO   = 1       # 0 = just send the settings, 1 = send settings and start the data transfer

ConvFact = 0.000286

Command = 0

Command = Command + GO
Command = Command + TRIG * 4
Command = Command + EXTEN * 16
Command = Command + HPF * 64
Command = Command + HRES * 128
Command = Command + MODE * 256
Command = Command + NCH * 2048
Command = Command + FSAMP * 8192

bin_command = "{0:b}".format(Command)
bin_command_stop = "{0:b}".format(Command-1)
# print("Command")
# print(Command)
# print("Command")
# print(bin(Command))
# print()

NumChan = 8

sampFreq = 2000

TCP_IP = '0.0.0.0'
# TCP_IP = "192.168.1.4"
TCP_PORT = 45454
BUFFER_SIZE = 500000

print("Creating server")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server binding")
s.bind((TCP_IP, TCP_PORT))
print("Server listening")
s.listen(1)

conn, addr = s.accept()
print("Connection address: {}".format(addr))

conn.send(bin_command)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    for i in range 100:
        print(i)
        data = conn.recv(1024)
        print(data)

        print(pressed)
    listener.join()



conn.send(bin_command_stop)
# data = s.recv(BUFFER_SIZE)
s.close()
