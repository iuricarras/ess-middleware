from . import sio
from package.__main__ import session, VM
from package.classes.threadResources import ThreadResources
import threading
from package.threads.faultTolerance import FaultTolerance
from . import proxmox, presources
import json

threads = []

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

    vmListPost = data
    vmListDB = VM.query.all()


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