#!/usr/bin/env python3

from drone_api import Drone_api
from socket import *
import argparse
import time

parser = argparse.ArgumentParser(description='Server-drone')
parser.add_argument('-l', '--logfile', dest='logfile', action='store_true',
                    help='if set, output is saved to a file "neuroLog_<TIME>.txt"')
args = parser.parse_args()


def get_time():
    now = time.gmtime(time.time())
    return f'{time.strftime("%Y.%m.%d %H:%M:%S", time.gmtime())}'


# Можно менять
max_speed_xy = 1  # m/s
max_speed_z = 0.5


is_started = False
is_open = False
drone = Drone_api(redefine_zero_point=True, disable_signals=True)

command_type = 'udfblr'  # Up Down Forward Back Left Right
port = 50202
addr = ('', port)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)
# timeout до закрытия сокета 10 часов
# maybe: сделать бесконечным
udp_socket.settimeout(36000)
# time_now = get_time() # todo: убрать
print(f'[{get_time()}] Start server, port: {port}')

try:
    while not drone.is_shutdown():
        data, client_arrd = udp_socket.recvfrom(8)
        time_now = get_time()
        if args.logfile and is_open:
            log.write(f'[{time_now}] {data} {client_arrd}\n')
        print(f'[{time_now}] {data} {client_arrd}')
        data = data.decode()
        # Старт полета
        if data == 'start':
            if not is_started:
                is_started = True
                if args.logfile:
                    time_now = get_time()
                    log = open(f'neuroLog_{time_now}.txt', 'w')
                    is_open = True
                    print(f'[{time_now}] Logfile open')
                drone.start()
                drone.set_local_pose(0, 0, 3)
                time_now = get_time()
                if args.logfile:
                    log.write(f'[{time_now}] Takeoff\n')
                print(f'[{time_now}] Takeoff')
                while not drone.point_is_reached():
                    drone.sleep(0.1)
                time_now = get_time()
                if args.logfile:
                    log.write(f'[{time_now}] Ready\n')
                print(f'[{time_now}] Ready')
        # Остановка полета
        elif data == 'stop':
            if is_started:
                is_started = False
                drone.stop()
                time_now = get_time()
                if args.logfile:
                    log.write(f'[{time_now}] Landing\n')
                print(f'[{time_now}] Landing')
                if args.logfile:
                    log.close()
                    is_open = False
                    print(f'[{get_time()}] Logfile closed')
        # Управление полетом
        elif is_started:
            if data == '':
                drone.set_velocity(0, 0, 0)
            else:
                c_t = data[0]
                if c_t in command_type:
                    try:
                        force = int(data[1:])
                    except ValueError:
                        print(f'[{get_time()}] Incorrect command')
                        continue
                    if force < 0 or force > 100:
                        print(f'[{get_time()}] Incorrect command')
                    else:
                        force /= 100
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
                    print(f'[{get_time()}] Incorrect command')

except KeyboardInterrupt:
    pass
except Exception as e:
    if args.logfile:
        log.write(str(e))
    print(e)
finally:
    print()
    if is_started:
        drone.stop()
        time_now = get_time()
        if args.logfile:
            log.write(f'[{time_now}] Landing\n')
        print(f'[{time_now}] Landing')
        if args.logfile:
            log.close()
            print(f'[{get_time()}] Logfile closed')
    udp_socket.close()
    print(f'[{get_time()}] Close server')
