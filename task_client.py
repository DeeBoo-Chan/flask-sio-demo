# -*- coding: utf-8 -*-
import os
import socket
import traceback


class LogClient(object):
    """docstring for LogClient"""
    def __init__(self, port=10909, host='127.0.0.1'):
        super(LogClient, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (host, port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def write(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf-8', 'ignore')
        send = self.sock.sendto(msg, self.addr)
        # print(send)

def print_log(msg, port=10909, host='127.0.0.1'):
    try:
        with LogClient(port, host) as lc:
            # print(msg, file=lc, end='')
            lc.write(msg)
    except Exception as e:
        print('=' * 60, sep='')
        print(msg)
        print('=' * 60)
        traceback.print_exc()