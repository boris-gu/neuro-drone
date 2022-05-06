#!/usr/bin/env python3

from socket import *

command_type = 'udfblr'  # Up Down Forward Back Left Right

host = 'localhost'
port = 50202
addr = (host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        data = input('> ')
        # Проверка верности команды
        if data[0] in command_type:
            try:
                force = int(data[1:])
            except ValueError:
                print('Incorrect command')
                continue
            if force < 0 or force > 100:
                print('Incorrect command')
            else:
                data = str.encode(data)
                udp_socket.sendto(data, addr)
        else:
            print('Incorrect command')
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    print('\nClose')
    udp_socket.close()
