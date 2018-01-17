prepare for anwser: https://stackoverflow.com/questions/29461028/flask-rabbitmq-socketio-forwarding-messages

> my code running environment:
> * OS: ubuntu 16.04 LTS
> * Python: 3.5.2
> * pip: 9.0.1

#### file description:
```
├── requirements.txt      -- packages list file (i use latest version)
├── run_bad.py            -- incorrect example
├── run.py                -- correct example
├── sio_client.py         -- socket.io client call
├── sio_server.py         -- cocket.io server call
├── task_client.py        -- a udp client wrapper
└── task_server.py        -- a udp server wrapper
```

#### setup & run
```shell
pip install -r requirements.txt
# one terminal window 
python run.py
# another terminal window
python task_server.py
```

#### look result
1. open web browser, open http://127.0.0.1:5000/, we named this tab as tab1
2. and, press F12 to open dev tool, and switch to **console** panel
3. open another tab and open http://127.0.0.1:5000/task?msg=hello, we named this tab as tab2
4. look at the console panel at tab1, you could see some output

#### ps
`run_bad.py` is an incorrect example
Design ideas:
```
-> GET /task (Browser=>Server)(http req1)
    -> socket.io\[write_task_log\] (Client=>Server) (ws req2)
        -> socket.io\[send_log\] (Server=>Browser) (ws req3)
```
ideas is ok, but, server is **Single Process** and **Single Thread**, so when **req2** created, **req1** isn't completed, then **req1** wait **req2** finish, but **req2** wait response from server, where is blocking at there now.
so that, i need to create a external service to send request for **req2**, and udp connect request will immediately finish after send data, so **req1** will finish soon. **req2** can get server's response as expected, all is ok.