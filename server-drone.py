#!/usr/bin/env python3

# Модуль socket для сетевого программирования
from socket import *

# данные сервера
host = 'localhost'
port = 50202
addr = (host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)

try:
    while True:
        data, address = udp_socket.recvfrom(1024)
        print(data, addr)
        print(type(data))
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    print('\nClose')
    udp_socket.close()
