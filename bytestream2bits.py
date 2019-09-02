
import struct
import sys
import numpy as np
from bitstring import BitArray

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder = 'big')

def bytes_to_bitstring(s):
    integer = int.from_bytes(s, byteorder='big')
    bits = '{0:08b}'.format(integer)
    return bits

TestCommand = "01000001101000001"
print(TestCommand)

TestCommandBytes = bitstring_to_bytes(TestCommand)
print(TestCommandBytes)

TestCommandBits = bytes_to_bitstring(TestCommandBytes)
print(TestCommandBits)
