import socketio
import time
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('response')
def on_response(sid, data):

    print('Response received:', data)

@sio.on('resp test')
def on_resp_test(data):
    print('Response test received:', data)

try:
    sio.connect('http://localhost:5000', auth={'token': 'ubuntu'})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")

sio.emit('get_cluster')
sio.emit('testing', {'ip': '127.0.0.1'})
sio.wait()