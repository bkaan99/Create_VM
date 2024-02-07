from pyVim.connect import Disconnect
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

def main(vm_name_to_shut_down, esxi_host_ip, esxi_user, esxi_password):
    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)

    vm_to_shut_down = get_vm_by_name(content, vm_name_to_shut_down)

    if vm_to_shut_down is not None:
        # Shut down the VM
        shut_down_vm(vm_to_shut_down)

        print("VM is shutting down...")
    else:
        print(f"VM with name {vm_name_to_shut_down} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
