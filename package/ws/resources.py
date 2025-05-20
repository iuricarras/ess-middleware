from . import sio
from package.__main__ import session, VM
from package.classes.threadResources import ThreadResources
import threading
from package.threads.faultTolerance import FaultTolerance
from . import proxmox, presources
import json
import time

threads = []

def startFaultTolerance():
    global threads
    time.sleep(5)
    VMs = session.query(VM).all()
    for vm in VMs:
        vmID = vm.name
        thread_resources = ThreadResources()
        thread_resources.vmID = vmID
        thread_resources.killThread = threading.Event()

        thread = threading.Thread(target=FaultTolerance, args=(vmID, proxmox, presources, thread_resources.killThread))
        thread.start()

        thread_resources.thread = thread

        threads.append(thread_resources)
        print(f"Thread started for VM {vmID}")


@sio.on('/rest/faulttolerance/get')
def get_fault_tolerance(data):
    """
    Get fault tolerance information.
    """
    vmList = []
    vmListDB = session.query(VM).all()

    for vm in vmListDB:
        vmList.append(vm.name)

    sio.emit('/rest/faulttolerance/get', json.dumps(vmList))

@sio.on('/rest/faulttolerance/post')
def post_fault_tolerance(data):
    global threads

    vmListPost = data['data']
    print(f"Received VM list: {vmListPost}")
    vmListDB = session.query(VM).all()


    for vm in vmListPost:
        # Check if VM exists in the database
        vm_exists = False
        for vm_db in vmListDB:
            if vm_db.name == vm:
                vm_exists = True
                vmListDB.remove(vm_db)
                break
        if not vm_exists:
            # If VM does not exist, create a new entry in the database
            new_vm = VM(name=vm)
            session.add(new_vm)
            session.commit()
            print(f"VM {vm} added to the database.")

            # Start a new thread for the VM
            thread_resources = ThreadResources()
            thread_resources.vmID = vm
            thread_resources.killThread = threading.Event()
            thread = threading.Thread(target=FaultTolerance, args=(vm, proxmox, presources, thread_resources.killThread))
            thread.start()
            thread_resources.thread = thread
            threads.append(thread_resources)
            print(f"Thread started for VM {vm}")
        else:
            print(f"VM {vm} already exists in the database.")    

    
    for vm in vmListDB:
        # If VM exists in the database but not in the request, stop the thread
        for thread_resources in threads:
            if thread_resources.vmID == vm.name:
                thread_resources.killThread.set()
                print(f"Thread for VM {vm.name} stopped.")
                session.query(VM).filter_by(name=vm.name).delete()
                session.commit()
                break

    return {"status": "Fault tolerance completed"}, 200

@sio.on('/rest/remotemigration/post')
def get_remote_migration(data):
    global proxmox
    global f
    body = data
    vmID = body['vmID']
    node = body['node']
    target_endpoint = body['target_endpoint']
    target_storage = body['target_storage']
    target_bridge = body['target_bridge']

    data = dict()
    data['target-endpoint'] = target_endpoint
    data['target-storage'] = target_storage
    data['target-bridge'] = target_bridge

    try:
        proxmox.nodes(node).qemu(vmID).remote_migrate.post(
            **data
        )
        return {"status": "Remote migration completed"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@sio.on('/rest/ha/groups/get')
def get_ha_groups(data):
    """
    Get HA group information.
    """
    try:
        ha_groups = proxmox.cluster.ha.groups.get()
        sio.emit('/rest/ha/groups/get', json.dumps(ha_groups))
    except Exception as e:
        print(f"Error fetching HA group information: {e}")
        sio.emit('/rest/ha/groups/get', json.dumps({"error": str(e)}))

@sio.on('/rest/ha/groups/post')
def post_ha_groups(data):
    """
    Post HA group information.
    """
    try:
        ha_group = data['data']
        proxmox.cluster.ha.groups.post(**ha_group)
        sio.emit('/rest/ha/groups/post', json.dumps({"status": "HA group created"}))
    except Exception as e:
        print(f"Error creating HA group: {e}")
        sio.emit('/rest/ha/groups/post', json.dumps({"error": str(e)}))


@sio.on('/rest/ha/groups/delete')
def delete_ha_groups(data):
    """
    Delete HA group information.
    """
    try:
        ha_group = data['data']
        proxmox.cluster.ha.groups(ha_group["group"]).delete()
        sio.emit('/rest/ha/groups/delete', json.dumps({"status": "HA group deleted"}))
    except Exception as e:
        print(f"Error deleting HA group: {e}")
        sio.emit('/rest/ha/groups/delete', json.dumps({"error": str(e)}))

@sio.on('/rest/ha/resources/get')
def get_ha_resources(data):
    """
    Get HA resource information.
    """
    try:
        ha_resources = proxmox.cluster.ha.resources.get()
        sio.emit('/rest/ha/resources/get', json.dumps(ha_resources))
    except Exception as e:
        print(f"Error fetching HA resource information: {e}")
        sio.emit('/rest/ha/resources/get', json.dumps({"error": str(e)}))

@sio.on('/rest/ha/resources/post')
def post_ha_resources(data):
    """
    Post HA resource information.
    """
    try:
        ha_resource = data['data']
        proxmox.cluster.ha.resources.post(**ha_resource)
        sio.emit('/rest/ha/resources/post', json.dumps({"status": "HA resource created"}))
    except Exception as e:
        print(f"Error creating HA resource: {e}")
        sio.emit('/rest/ha/resources/post', json.dumps({"error": str(e)}))

@sio.on('/rest/ha/resources/delete')
def delete_ha_resources(data):
    """
    Delete HA resource information.
    """
    try:
        ha_resource = data['data']
        proxmox.cluster.ha.resources(ha_resource["sid"]).delete()
        sio.emit('/rest/ha/resources/delete', json.dumps({"status": "HA resource deleted"}))
    except Exception as e:
        print(f"Error deleting HA resource: {e}")
        sio.emit('/rest/ha/resources/delete', json.dumps({"error": str(e)}))


@sio.on('/rest/cluster/resources/get')
def get_cluster_resources(data):
    """
    Get cluster resources information
    """
    try:
        cluster_resources = proxmox.cluster.resources.get()
        sio.emit('/rest/cluster/resources/get', json.dumps(cluster_resources))
    except Exception as e:
        print(f"Error fetching cluster resources information: {e}")
        sio.emit('/rest/cluster/resources/get', json.dumps({"error": str(e)}))

@sio.on('/rest/qemu/migration/post')
def post_qemu_migration(data):
    """
    Creates a new migration task.
    """
    try:
        migration = data['data']
        proxmox.nodes(migration['node']).qemu(migration['vmid']).migrate.post(**migration)
        sio.emit('/rest/qemu/migration/post', json.dumps({"status": "Migration Done"}))
    except Exception as e: 
        print(f"Error creating HA resource: {e}")
        sio.emit('/rest/qemu/migration/post', json.dumps({"error": str(e)}))