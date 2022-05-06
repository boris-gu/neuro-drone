#!/usr/bin/env python3

# Модуль socket для сетевого программирования
from drone_api import Drone_api
from socket import *

# ДРОН
max_speed_xy = 1  # m/s
max_speed_z = 0.5

drone = Drone_api(redefine_zero_point=True, disable_signals=True)
drone.start()
print('Armed')
drone.set_local_pose(0, 0, 3)
while not drone.point_is_reached():
    drone.sleep(0.1)

# СЕРВЕР
command_type = 'udfblr'  # Up Down Forward Back Left Right
port = 50202
addr = ('', port)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)
print(f'Start server, port: {port}')

try:
    while not drone.is_shutdown():
        print("OK")
        data, address = udp_socket.recvfrom(8)
        print(data, addr)
        data = data.decode()
        c_t = data[0]
        if c_t in command_type:
            try:
                force = int(data[1:])
            except ValueError:
                print('Incorrect command')
                continue
            if force < 0 or force > 100:
                print('Incorrect command')
            else:
                force /= 100
                print(force)
                if c_t == 'u':
                    drone.set_velocity(0, 0, max_speed_z*force)
                elif c_t == 'd':
                    drone.set_velocity(0, 0, -max_speed_z*force)
                elif c_t == 'f':
                    drone.set_velocity(max_speed_xy*force, 0, 0)
                elif c_t == 'b':
                    drone.set_velocity(-max_speed_xy*force, 0, 0)
                elif c_t == 'l':
                    drone.set_velocity(0, max_speed_xy*force, 0)
                elif c_t == 'r':
                    drone.set_velocity(0, -max_speed_xy*force, 0)
        else:
            print('Incorrect command')

except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    print('\nClose server, landing')
    udp_socket.close()
