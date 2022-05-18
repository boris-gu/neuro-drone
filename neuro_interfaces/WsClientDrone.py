import json
import multiprocessing
import time
from queue import Empty
from socket import *
from threading import Thread
from websocket import create_connection
import settings


class WsClientDrone(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.ws = create_connection(f"ws://{settings.HEAD_BAND_PC_IP}:1336")
        self.queue = queue
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.current_direction = b'up'
        self.drone_ip = settings.DRONE_IP
        self.drone_port = settings.DRONE_PORT
        self.directions = {
            b'forward': 'f',
            b'back': 'b',
            b'left': 'l',
            b'right': 'r',
            b'up': 'u',
            b'down': 'd',
        }

    def send_drone_msg(self, msg):
        self.udp_socket.sendto(
            msg.encode(),
            (self.drone_ip, self.drone_port)
        )

    def run(self):
        try:
            while True:
                try:
                    arm_band_msg = self.queue.get_nowait()
                    if arm_band_msg is not None:
                        self.current_direction = arm_band_msg
                except Empty:
                    pass
                self.ws.send(json.dumps({"command": "concentration"}))
                msg_ws = self.ws.recv()
                msg_ws = json.loads(msg_ws)
                if "concentration" in msg_ws:
                    print(msg_ws["concentration"])
                    if msg_ws["concentration"] < 30:
                        speed = '0'
                    elif msg_ws["concentration"] >= 30:
                        speed = str(msg_ws["concentration"])
                    self.send_drone_msg(
                        self.directions[self.current_direction] + speed
                    )

                time.sleep(0.01)
        finally:
            self.udp_socket.close()
            self.ws.close()
