from pyVim.connect import SmartConnect, Disconnect
from pyVim import connect
from pyVmomi import vim
import ssl


def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None
def clone_vm(content, source_vm, clone_vm_name,datastore, clone_folder):
    try:
        for child in content.rootFolder.childEntity:
            if isinstance(child, vim.Datacenter):
                datacenter = child
                break

        if datacenter is None:
            print("Datacenter bulunamadı.")
            return None

        folder = datacenter.vmFolder
        resource_pool = datacenter.hostFolder.childEntity[0].resourcePool
        clone_spec = vim.vm.CloneSpec(powerOn=True, template=False , location=vim.vm.RelocateSpec(datastore=datastore, pool=resource_pool))

        task = source_vm.Clone(name=clone_vm_name, folder=folder, spec=clone_spec)
        WaitForTask(task)

        print(f"VM cloned successfully: {clone_vm_name}")

    except Exception as e:
        print(f"Error: {e}")

def WaitForTask(task):
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

    service_instance = connect.SmartConnect(host="10.14.45.11",
                                            user="root",
                                            pwd="Aa112233!",
                                            sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    source_vm_name = "bkaan_deneme"
    clone_vm_name = "bkaan_deneme_clone2"

    source_vm = get_vm_by_name(content, source_vm_name)
    datastore = source_vm.datastore[0]

    if source_vm is None:
        print(f"VM {source_vm_name} not found.")
        return

    if datastore is None:
        print(f"Datastore {datastore} not found.")
        return

    clone_folder = "bulent"

    source_file_path = f"[{datastore.name}] {clone_folder}/"

    # Clone the VM
    clone_vm(content, source_vm, clone_vm_name, datastore=datastore, clone_folder=source_file_path)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
