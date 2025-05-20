import socketio
sio = socketio.Client(logger=True, engineio_logger=True)
from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI
from package.classes.resources import Resources
from package.threads.apiThread import APIThread
import os
import threading

load_dotenv()

ip = os.getenv("PROXMOX_IP")
port = os.getenv("PROXMOX_PORT")
user = os.getenv("PROXMOX_USER")
password = os.getenv("PROXMOX_PASSWORD")

proxmox = ProxmoxAPI(ip + ":"+ port, user=user, password=password, verify_ssl=False, timeout=30)
presources = Resources()

threading.Thread(target=APIThread, args=(proxmox, presources)).start()



try:
    sio.connect('http://localhost:5000', auth={'ip': "192.168.22.14", 'token': 'DitkYWBEv8cnAyCs'})
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")

from . import resources

resources.startFaultTolerance()

sio.wait()