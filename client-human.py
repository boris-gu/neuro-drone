#!/usr/bin/env python3

import argparse
from socket import *

# ПАРСЕР
descr = 'Drone message sender.\n'
descr += 'COMMAND: type(first letter) + force([0,100])\n'
descr += 'EXAMPLE: r34\n\n'
descr += 'COMMAND TYPES:\nUp\nDown\nForward\nBack\nLeft\nRight'

parser = argparse.ArgumentParser(description=descr,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--host', default='localhost', help='host IP')
args = parser.parse_args()

# КЛИЕНТ
command_type = 'udfblr'  # Up Down Forward Back Left Right

#host = 'localhost'
print(args.host)
port = 50202
addr = (args.host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        data = input('> ')
        # Проверка верности команды
        if data == '' or data == 'start' or data == 'stop':
            udp_socket.sendto(data.encode(), addr)
        elif data[0] in command_type:
            try:
                force = int(data[1:])
            except ValueError:
                print('Incorrect command')
                continue
            if force < 0 or force > 100:
                print('Incorrect command')
            else:
                #data = str.encode(data)
                udp_socket.sendto(data.encode(), addr)
        else:
            print('Incorrect command')
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    print('\nClose client')
    udp_socket.close()
