import socketio
import time
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('response')
def on_response(sid, data):

    print('Response received:', data)

@sio.on('resp test')
def on_resp_test(data):
    print('Response test received:', data)

@sio.on('*')
def get(sid, data):
    """
    Get fault tolerance information.
    """
    print('Data received:', data)
    # Here you can process the data as needed
    # For example, you can send a response back to the server

@sio.on('/rest/faulttolerance/post')
def post_fault_tolerance(data):
    """
    Post fault tolerance information.
    """
    print('Fault tolerance post data received:', data)
    # Here you can process the data as needed
    # For example, you can send a response back to the server

try:
    sio.connect('http://localhost:5000', auth={'token': 'DitkYWBEv8cnAyCs'})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")


#sio.emit('/rest/ha/groups/post', {'ip': "192.168.22.14", 'data': {"nodes": "pve3", "group": "test", "nofailback": 1 }})
#sio.emit('/rest/ha/groups/delete', {'ip': "192.168.22.14", 'data': {"group": "test"}})
#sio.emit('/rest/ha/resources/get', {'ip': "192.168.22.14"})
#sio.emit('/rest/ha/resources/post', {'ip': "192.168.22.14", 'data': {"sid": "vm:101", "group": "ha", "state": "started"}})
#sio.emit('/rest/ha/resources/delete', {'ip': "192.168.22.14", 'data': {"sid": "vm:101"}})
#sio.emit('/rest/cluster/resources/get', {'ip': '192.168.22.14'})
sio.emit('/rest/qemu/migration/post', {'ip': '192.168.22.14', 'data': {"node": "pve", "target": "pve2", "vmid": 101}})
sio.wait()