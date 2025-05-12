import socketio
import time
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('response')
def on_response(sid, data):

    print('Response received:', data)


try:
    sio.connect('http://localhost:5000', auth={'ip': "127.0.0.1", 'token': 'ubuntu'})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")

sio.wait()