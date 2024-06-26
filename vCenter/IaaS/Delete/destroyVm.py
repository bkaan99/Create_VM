from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def destroy_vm(vm):
    try:
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            print("Shutting down VM...")
            task = vm.PowerOff()
            WaitForTask(task)

        task = vm.Destroy_Task()
        WaitForTask(task)

    except (vim.fault.InvalidPowerState, vim.fault.VimFault, vim.fault.TaskInProgress) as e:
        print("Sanal makineyi yok etme sırasında bir hata oluştu:", e)

    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", e)

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(destroy_vm_name :str ,vCenter_host_ip :str, vCenter_user :str, vCenter_password :str):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)
    vm_name_to_destroy = destroy_vm_name

    vm_to_destroy = get_vm_by_name(content, vm_name_to_destroy)

    if vm_to_destroy is not None:
        # Destroy the VM
        destroy_vm(vm_to_destroy)
    else:
        print(f"VM with name {vm_name_to_destroy} not found")

    Disconnect(service_instance)
