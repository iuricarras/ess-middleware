import socketio
import time
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('response')
def on_response(sid, data):

    print('Response received:', data)

@sio.on('testing')
def on_testing(data):
    print('Testing received:', data)
    sio.emit('resp test', {'status': 'ok'})

try:
    sio.connect('http://localhost:5000', auth={'ip': "127.0.0.1", 'token': 'ubuntu'})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")

sio.wait()