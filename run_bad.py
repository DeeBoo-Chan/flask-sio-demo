# run.py
from threading import Thread

from flask import Flask, request

from sio_server import socketio
from sio_client import get_ws_client


app = Flask(__name__)

socketio.init_app(app)
app.socketio = socketio

index_tmpl_str = '''
<!DOCUMENT html>
<html>
<head>
    <meta charset="uff-8" />
    <title>flask socketio demo</title>
</head>
<body>
    <div>please watch server response at console of web browser(you can press F12)</div>
    <!-- socket.io cdn -->
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.slim.js"></script>
    <script type="text/javascript">
        var namespace = '/test';
        var ws_url = [location.protocol, '//', document.domain, ':', location.port, namespace].join('');
        var socket = io.connect(ws_url, {
            path: '/ws/'
        });

        socket.on('send_log', function(message) {
            console.log(message);
        });
    </script>
</body>
</html>
'''

@app.route("/")
def view_index():
    return index_tmpl_str

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

@app.route("/task")
def view_task():
    msg = request.values.get('msg', 'empty msg')
    send_msg(msg)
    return 'send task ok'

if __name__ == '__main__':
    cfg = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True
    }
    print('visit by [http://{0}:{1}]'.format(cfg['host'], cfg['port']))
    socketio.run(app, **cfg)