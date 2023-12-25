from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import time

def get_vm_by_name(content, vm_name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for child in container.view:
        if child.name == vm_name:
            return child
    return None

def shut_down_vm(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        task = vm.ShutdownGuest()
        if task:
            WaitForTask(task)
        else:
            print("Failed to initiate the shutdown process.")


def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        time.sleep(1)  # Bir süre bekleyerek döngüyü kontrol et
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main():
    vcenter_server = "10.14.45.11"
    vcenter_user = "root"
    vcenter_password = "Aa112233!"
    vm_name_to_shut_down = "yeni_bkaan_cemo"

    # Disable SSL certificate verification
    sslContext = ssl.create_default_context()
    sslContext.check_hostname = False
    sslContext.verify_mode = ssl.CERT_NONE

    # Connect to vCenter
    si = SmartConnect(
        host=vcenter_server,
        user=vcenter_user,
        pwd=vcenter_password,
        sslContext=sslContext,
    )

    # Retrieve the VM to shut down
    content = si.RetrieveContent()
    vm_to_shut_down = get_vm_by_name(content, vm_name_to_shut_down)

    if vm_to_shut_down is not None:
        # Shut down the VM
        shut_down_vm(vm_to_shut_down)

        print("VM is shutting down...")
    else:
        print(f"VM with name {vm_name_to_shut_down} not found")

    # Disconnect from vCenter


    Disconnect(si)

if __name__ == "__main__":
    main()
