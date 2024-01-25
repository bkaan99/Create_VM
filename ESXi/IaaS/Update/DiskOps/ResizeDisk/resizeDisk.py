from pyVim.connect import Disconnect
from ESXi.IaaS.ESXi_Connection.esxi_connection import *

def reconfigure_vm(vm, disk_size_gb):
    try:
        # Create a VimVMConfigSpec object to specify the changes
        spec = vim.vm.ConfigSpec()

        # Modify the first virtual disk (assuming there is only one disk)
        if len(vm.config.hardware.device) > 0 and isinstance(vm.config.hardware.device[0], vim.vm.device.VirtualDisk):
            disk = vm.config.hardware.device[0]
            disk.capacityInKB = disk_size_gb * 1024 * 1024

        # Invoke ReconfigVM_Task to apply the changes
        task = vm.ReconfigVM_Task(spec=spec)
        WaitForTask(task)

        print("VM reconfigured successfully.")
    except Exception as e:
        print(f"Error reconfiguring VM: {e}")

def WaitForTask(task):
    """Waits and provides updates on a vSphere task until it is completed."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Task completed successfully.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Error: {task.info.error}")
            task_done = True

def main(vm_name_to_reconfigure, esxi_host_ip, esxi_user, esxi_password):
    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)

    target_disk_size_gb = 48  # Modify with the desired disk size in GB

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} not found.")
        return

    # Power On durumunda ise shutdown et
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("Powering off VM...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    reconfigure_vm(vm_to_reconfigure, target_disk_size_gb)
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
