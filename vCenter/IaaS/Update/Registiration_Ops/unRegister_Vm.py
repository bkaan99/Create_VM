from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
from pyVmomi import vim
import time


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

def main(unregister_vm_name ,vCenter_host_ip, vCenter_user, vCenter_password):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_to_unregister = get_vm_by_name(content, unregister_vm_name)

    if vm_to_unregister is not None:

        if vm_to_unregister.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            poweroff = vm_to_unregister.PowerOffVM_Task()
            WaitForTask(poweroff)

        unregister_vm(vm_to_unregister)
        print("VM is unregistering...")
    else:
        print(f"VM with name {unregister_vm_name} not found")

    Disconnect(service_instance)

