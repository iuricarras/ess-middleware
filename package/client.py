import socketio
import time
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('response')
def on_response(sid, data):

    print('Response received:', data)

@sio.on('resp test')
def on_resp_test(data):
    print('Response test received:', data)

@sio.on('/rest/faulttolerance/get')
def get_fault_tolerance(data):
    """
    Get fault tolerance information.
    """
    print('Fault tolerance data received:', data)
    # Here you can process the data as needed
    # For example, you can send a response back to the server

try:
    sio.connect('http://localhost:5000', auth={'token': 'ubuntu'})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")

sio.emit('/rest/faulttolerance/get', {'ip': "127.0.0.1"})
sio.wait()