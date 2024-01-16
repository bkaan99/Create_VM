from pyVim.connect import SmartConnect, Disconnect
from ESXi.IaaS.ESXi_Connection.esxi_connection import *
from pyVmomi import vim
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

def main(vm_name_to_suspend, esxi_host_ip, esxi_user, esxi_password):
    si, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)
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
