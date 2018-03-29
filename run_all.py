# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import os
import multiprocessing

from flask import Flask, request

from sio_server import socketio
from task_client import print_log
from task_server import imitate_server


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
    <div>
        <a target="_blank" href="/task?msg=hello">send task</a>
    </div>
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

@app.route("/task")
def view_task():
    msg = request.values.get('msg', 'default empty msg')
    print_log(msg)
    return 'send task ok with msg:<br /><div style="border: 1px solid #fa1;">' + msg + '</div>'


def start_http_server(cfg):
    global socketio
    print('visit by [http://{0}:{1}]'.format(cfg['host'], cfg['port']))
    try:
        socketio.run(app, **cfg)
    except (KeyboardInterrupt, SystemExit):
        print('closing by user...')
        pass
    finally:
        with app.app_context():
            socketio.stop()

def main():
    # set os.environ with key REAL_RUN
    # if is debug mode, flask with launch main() twice, but will not reset os.environ
    # so, we can judge if it's the second times launch
    # if not to judge, log precess will raise `OSError: [Errno 98] Address already in use`
    # so, only launch log precess once
    # ------------------------------
    # debug mode can't work when reload because of code change
    is_debug = False
    if is_debug:
        os.environ['REAL_RUN'] = '1' if 'REAL_RUN' in os.environ else '0'
    else:
        os.environ['REAL_RUN'] = '1'

    log_port = 10909
    log_precess = None
    if os.environ['REAL_RUN'] == '1':
        log_process = multiprocessing.Process(
            name='print_log_server',
            target=imitate_server,
            args=(),
            kwargs={
                'port': log_port
            }
        )
        log_process.daemon = True

    cfg = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': is_debug
    }

    try:
        if os.environ['REAL_RUN'] == '1':
            log_process.start()
        start_http_server(cfg)
    except (KeyboardInterrupt, SystemExit):
        print('closing by user...')
    finally:
        if os.environ['REAL_RUN'] == '1':
            if isinstance(log_precess, multiprocessing.Process):
                log_precess.join()

if __name__ == '__main__':
    main()