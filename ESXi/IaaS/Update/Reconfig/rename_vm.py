from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from ESXi.IaaS.ESXi_Connection.esxi_connection import *


def get_vm_by_name(content, vm_name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for child in container.view:
        if child.name == vm_name:
            return child
    return None

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

def main(old_vm_name, new_vm_name, esxi_host_ip, esxi_user, esxi_password):

    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)

    vm_to_rename = get_vm_by_name(content, old_vm_name)

    if vm_to_rename is not None:
        # Rename the VM
        rename_vm(vm_to_rename, new_vm_name)
    else:
        print(f"VM with name {old_vm_name} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
