import time
def APIThread(proxmox, resources):
    print("Starting API thread")
    while(True):
        try:
            resources.nodes = proxmox.nodes.get()
            resources.vms = proxmox.cluster.resources.get(type="vm")
            if not resources.started:
                resources.started = True
                print("Proxmox API connection established and resources fetched.")
            time.sleep(10)
        except Exception as e:
            print(f"Error connecting to Proxmox API: {e}")
            time.sleep(5)