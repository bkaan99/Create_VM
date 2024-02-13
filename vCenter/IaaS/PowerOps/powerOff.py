from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *


def power_off_vm(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        task = vm.PowerOffVM_Task()
        wait_for_task(task)
        print("VM powered off.")
    else:
        print("VM is already powered off.")

def wait_for_task(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(vm_name, vCenter_host_ip, vCenter_user, vCenter_password):
    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)
    vm_to_manage = get_vm_by_name(content, vm_name)

    if vm_to_manage is not None:
        # Power off the VM if it's powered on
        power_off_vm(vm_to_manage)
    else:
        print(f"VM with name {vm_name} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
