from pyVim.connect import SmartConnect, Disconnect
from ESXi.IaaS.ESXi_Connection.esxi_connection import *
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

def unregister_vm(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        poweroff = vm.PowerOffVM_Task()
        task = vm.Unregister()
        if task:
            WaitForTask(task)
        else:
            print("Failed to initiate the shutdown process.")
    else:
        vm.Unregister()


def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        time.sleep(1)  # Bir süre bekleyerek döngüyü kontrol et
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(unregister_vm_name ,esxi_host_ip, esxi_user, esxi_password):

    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)
    vm_name_to_shut_down = unregister_vm_name

    vm_to_unregister = get_vm_by_name(content, vm_name_to_shut_down)

    if vm_to_unregister is not None:
        # Shut down the VM
        unregister_vm(vm_to_unregister)
        print("VM is unregistering...")
    else:
        print(f"VM with name {vm_name_to_shut_down} not found")

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
