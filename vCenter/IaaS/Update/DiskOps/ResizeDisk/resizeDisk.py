from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
def reconfigure_vm(vm, disk_size_gb):
    try:
        spec = vim.vm.ConfigSpec()

        virtual_disks = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                virtual_disks.append(device)

        if virtual_disks:
            for disk in virtual_disks:
                if disk.unitNumber == 0:
                    if disk_size_gb < disk.capacityInKB / 1024 ** 2:
                        disk_size_gb = disk.capacityInKB / 1024 ** 2
                    disk.capacityInKB = int(disk_size_gb * 1024 * 1024)

                    # Create a VirtualDeviceConfigSpec to apply the new disk size
                    disk_spec = vim.vm.device.VirtualDeviceSpec()
                    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                    disk_spec.device = disk

                    spec.deviceChange = [disk_spec]

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

def main(vm_name_to_reconfigure, vCenter_host_ip, vCenter_user, vCenter_password):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    target_disk_size_gb = 60  # Modify with the desired disk size in GB

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
