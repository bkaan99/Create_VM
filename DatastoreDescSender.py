from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def get_datastores(content):
    datastore_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)
    datastores = datastore_view.view
    return datastores

def print_datastore_info(datastores):
    for datastore in datastores:
        print("Datastore Name:", datastore.name)
        print("Datastore URL:", datastore.summary.url)
        print("Capacity:", datastore.summary.capacity)
        print("Free Space:", datastore.summary.freeSpace)
        print("------------------------------")

def wait_for_task(task):
    """Waits and provides updates on a vSphere task until it is completed."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Task completed successfully.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Error: {task.info.error}")
            task_done = True

def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    print("Datastore Information:")
    datastores = get_datastores(content)
    print_datastore_info(datastores)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
