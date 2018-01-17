# -*- coding: utf-8 -*-
from socketIO_client import SocketIO

from socketIO_client import BaseNamespace


class WSNamespace(BaseNamespace):
    _connected = True

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

def get_ws_client(ws_cfg):
    return SocketIO(
        ws_cfg['host'],
        ws_cfg['port'],
        resource=ws_cfg['resource'],
        Namespace=WSNamespace
    )