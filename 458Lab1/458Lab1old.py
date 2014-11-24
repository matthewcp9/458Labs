from datetime import datetime
import time
import random
import base64
import binascii

class MT19937:
    
    def __init__(self):
        self.MT = [None] * 624
        self.index = 0
    def initialize_generator(self, seed):
        index = self.index
        MT = self.MT
        index = 0
        MT[0] = seed
        for i in range(1, 624):
            MT[i] = 0x00000000ffffffff & (1812433253 * (MT[i - 1] ^  (MT[i - 1] >> 30)) + i)

    def extract_number(self):
        index = self.index
        MT = self.MT
        if index == 0:
            self.generate_numbers()

        y = MT[index]
        y = y ^ (y >> 11)
        y = y ^ (y << 7 & (2636928640))
        y = y ^ (y << 15 & (4022730752))
        y = y ^ (y >> 18)

        index = (index + 1) % 624
        return y

    def generate_numbers(self):
        MT = self.MT
        for i in range(0, 624):
            y = (MT[i] & 0x80000000) + (MT[(i + 1) % 624] & 0x7fffffff)
            MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
            if (y % 2) != 0:
                MT[i] = (MT[i] ^ 2567483615)

def oracle():
    random_sec = random.randint(5, 60)
    time.sleep(random_sec)
    timestamp = int(time.time())
    ex = MT19937()
    print("The time stamp/seed is %d" % timestamp)
    ex.initialize_generator(timestamp)
    output = ex.extract_number()
    #print(output)
    random_sec = random.randint(5, 60)
    time.sleep(random_sec)
    b64output = bin(output).encode('base64','strict')
    return b64output

def findSeed(b64output):
    mt = MT19937()
    timestamp = int(time.time())
    for x in range(1, 200):
        mt.initialize_generator((timestamp - x))
        print("Trying %d ...." % (timestamp - x))
        guess = mt.extract_number()
        #print(guess)
        b64guess = bin(guess).encode('base64','strict')
        if (b64guess == b64output):
            return ("Seed is %d" % (timestamp - x))

    return "Seed could not be found"

def main():
    print(findSeed(oracle()))
main()
