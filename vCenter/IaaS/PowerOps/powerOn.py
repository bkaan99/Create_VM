from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def power_on_vm(vm):
    if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
        task = vm.PowerOnVM_Task()
        WaitForTask(task)
    else:
        print("VM is already powered on.")

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(vm_name :str,vCenter_host_ip :str, vCenter_user :str, vCenter_password :str):
    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)
    vm_to_power_on = get_vm_by_name(content, vm_name)

    if vm_to_power_on is not None:
        power_on_vm(vm_to_power_on)
    else:
        print(f"VM with name {vm_name} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)
