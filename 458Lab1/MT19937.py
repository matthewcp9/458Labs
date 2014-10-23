from datetime import datetime
import time
import random
import base64
import binascii

#Mersenne Twister MT 19937
class MT19937:
    
    def __init__(self, seed):
        self.MT = [None] * 624
        self.index = 0
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = 0x00000000ffffffff & (1812433253 * (self.MT[i - 1] ^  (self.MT[i - 1] >> 30)) + i)

    def extract_number(self):
        print("Index is %d " % self.index)
        MT = self.MT
        if self.index == 0:
		     print("Need to regen nums")
		     self.generate_numbers()

        y = MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ (y << 7 & (2636928640))
        y = y ^ (y << 15 & (4022730752))
        y = y ^ (y >> 18)

        self.index = (self.index + 1) % 624
        return y

    def generate_numbers(self):
        MT = self.MT
        for i in range(0, 624):
            y = (MT[i] & 0x80000000) + (MT[(i + 1) % 624] & 0x7fffffff)
            MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
            if (y % 2) != 0:
                MT[i] = (MT[i] ^ 2567483615)

