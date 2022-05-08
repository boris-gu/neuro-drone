#!/usr/bin/env python3

from drone_api import Drone_api
from socket import *
import argparse

parser = argparse.ArgumentParser(description='Server-drone')
parser.add_argument('-l', '--logfile', dest='logfile', action='store_false',
                    help='if set, output is saved to a file "neuro_drone_log.txt"')
args = parser.parse_args()

# ДРОН
max_speed_xy = 1  # m/s
max_speed_z = 0.5

if args.logfile:
    log = open('neuro_drone_log.txt', 'w')

drone = Drone_api(redefine_zero_point=True, disable_signals=True)
drone.start()

if args.logfile:
    log.write('Armed\n')
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
if args.logfile:
    log.write(f'Start server, port: {port}\n')
print(f'Start server, port: {port}')

try:
    while not drone.is_shutdown():
        data, client_arrd = udp_socket.recvfrom(8)
        if args.logfile:
            log.write(f'{data} {client_arrd}\n')
        print(data, client_arrd)
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
    if args.logfile:
        log.write(e)
    print(e)
finally:
    if args.logfile:
        log.write('Close server, landing')
        log.close()
    print('\nClose server, landing')
    udp_socket.close()
