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

def suspend(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        task = vm.Suspend()
        if task:
            WaitForTask(task)
            print("VM is suspending...")
        else:
            print("Failed to initiate the reboot process.")

    else:
        print("VM is powered off.")


def WaitForTask(task):
    while task.info.state == vim.TaskInfo.State.running:
        task_info = task.info
        if hasattr(task_info, 'progress') and task_info.progress:
            print(f"Task Progress: {task_info.progress}%")
        time.sleep(1)
    return task.info.state

def main():
    vcenter_server = "10.14.45.11"
    vcenter_user = "root"
    vcenter_password = "Aa112233!"
    vm_name_to_suspend = "yeni_bkaan_cemo"

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
    vm_to_suspend = get_vm_by_name(content, vm_name_to_suspend)

    if vm_to_suspend is not None:
        #reboot the VM
        suspend(vm_to_suspend)

    else:
        print(f"VM with name {vm_name_to_suspend} not found")

    # Disconnect from vCenter


    Disconnect(si)

if __name__ == "__main__":
    main()
