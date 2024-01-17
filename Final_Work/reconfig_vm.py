from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def reconfigure_vm(vm, cpu_count, memory_mb, disk_size_gb):
    try:
        # Create a VimVMConfigSpec object to specify the changes
        spec = vim.vm.ConfigSpec()
        spec.numCPUs = cpu_count
        spec.memoryMB = memory_mb

        # vm: vim.VirtualMachine instance already obtained
        vdisk = None
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                vdisk = device
                break
        if not vdisk:
            raise Exception("Failed to find VM virtual disk for resizing!")
        cspec = vim.vm.ConfigSpec()
        vdisk.capacityInKB = disk_size_gb * 1024 ** 2
        vdisk_spec = vim.vm.device.VirtualDeviceSpec(
            device=vdisk,
            operation=vim.vm.device.VirtualDeviceSpec.Operation.edit,
        )
        cspec.deviceChange = [vdisk_spec]
        WaitForTask(vm.Reconfigure(cspec))

        # # Find the first virtual disk
        # virtual_disks = [device for device in vm.config.hardware.device if
        #                  isinstance(device, vim.vm.device.VirtualDisk)]
        #
        # if len(virtual_disks) > 0:
        #     disk = virtual_disks[0]
        #     # Update the disk size (in kilobytes)
        #     disk.capacityInKB = disk_size_gb * 1024 * 1024
        #
        #     # Invoke ReconfigVM_Task to apply the changes
        #     task = vm.ReconfigVM_Task(spec=spec)
        #     WaitForTask(task)

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

def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    vm_name_to_reconfigure = "Pzt_Ubuntu_Deneme"

    target_cpu_count = 3  # Modify with the desired CPU count
    target_memory_mb = 4096 # Modify with the desired memory size in MB
    target_disk_size_gb = 20  # Modify with the desired disk size in GB

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} not found.")
        return

    # Power On durumunda ise shutdown et
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("Powering off VM...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    reconfigure_vm(vm_to_reconfigure, target_cpu_count, target_memory_mb, target_disk_size_gb)
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
