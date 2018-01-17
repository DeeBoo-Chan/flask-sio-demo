# -*- coding: utf-8 -*-
import time

from flask import (
    session,
    request
)
from flask_socketio import (
    SocketIO,
    emit
)


socketio = SocketIO(path='ws', logger=False, engineio_logger=False, async_mode='gevent')

@socketio.on('write_task_log', namespace='/test')
def handle_task_log(message):
    socketio.emit(
        'send_log',
        task_log(message),
        namespace='/test'
    )

def task_log(message):
    return {
        'msg': message,
        'level': 'info',
        'timestamp': int(time.time())
    }