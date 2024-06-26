from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def rename_vm(vm, new_name):
    spec = vim.vm.ConfigSpec()
    spec.name = new_name
    task = vm.ReconfigVM_Task(spec=spec)
    WaitForTask(task)

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(old_vm_name, new_vm_name, vCenter_host_ip, vCenter_user, vCenter_password):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_to_rename = get_vm_by_name(content, old_vm_name)

    if vm_to_rename is not None:
        # Rename the VM
        rename_vm(vm_to_rename, new_vm_name)
    else:
        print(f"VM with name {old_vm_name} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)
