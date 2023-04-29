#!/usr/bin/env python3
import random
import os
import sys
import time

def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def main():
    time.sleep(1)
    Data = "\"P4 TESTING DATA: {}, P4 TESTING DATA: {},P4 TESTING DATA: {}!\"".format(generate_random_str(random.randint(1,200)), 
               generate_random_str(random.randint(1,200)), 
               generate_random_str(random.randint(1,200)))
    cmd = "python3 ./send.py {} {} {} {}".format(sys.argv[1], sys.argv[2], Data, random.randint(1,4))
    print(cmd)
    print(os.system(cmd))

if __name__ == '__main__':
    main()