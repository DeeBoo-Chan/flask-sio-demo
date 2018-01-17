# -*- coding: utf-8 -*-
import os
import socket
import traceback

from sio_client import get_ws_client


def imitate_server(port=10909):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('0.0.0.0', port)
    start_msg = 'udp log server listen at [{0}:{1}]'.format(addr[0], addr[1])
    print(start_msg)
    try:
        sock.bind(addr)
        while True:
            data, address = sock.recvfrom(4096)
            if bool(data):
                msg = data.decode('utf-8', 'ignore')
                print(msg)
                send_msg(msg)
    except (KeyboardInterrupt, SystemExit, Exception):
        print('=' * 60, sep='')
        traceback.print_exc()
        print('=' * 60)
    finally:
        sock.close()

def send_msg(msg):
    # TODO: your code
    ws_cfg = {
        'host': '127.0.0.1',
        'port': 5000,
        'resource': 'ws'
    }
    ws_client = get_ws_client(ws_cfg)
    ws_client.emit('write_task_log', 'msg: ' + msg, path='/test')
    ws_client.disconnect()

if __name__ == '__main__':
    imitate_server()