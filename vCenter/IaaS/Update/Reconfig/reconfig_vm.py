from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def reconfigure_vm(vm, cpu_count, memory_mb, disk_size_gb):
    try:
        spec = vim.vm.ConfigSpec()
        spec.numCPUs = cpu_count
        spec.memoryMB = memory_mb

        vdisk = None
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                vdisk = device
                break
        if not vdisk:
            raise Exception("Failed to find VM virtual disk for resizing!")
        cspec = vim.vm.ConfigSpec()

        #disk_size_gb değeri var olan boyuttan büyük olmalı
        if disk_size_gb < vdisk.capacityInKB / 1024 ** 2:
            raise Exception("Disk boyutu var olan boyuttan küçük olamaz.")

        vdisk.capacityInKB = disk_size_gb * 1024 ** 2
        vdisk.capacityInBytes = disk_size_gb * 1024 ** 3
        vdisk_spec = vim.vm.device.VirtualDeviceSpec(
            device=vdisk,
            operation=vim.vm.device.VirtualDeviceSpec.Operation.edit,
        )
        cspec.deviceChange = [vdisk_spec]
        WaitForTask(vm.Reconfigure(cspec))

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
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Error: {task.info.error}")
            task_done = True

def main(vCenter_host_ip, vCenter_user, vCenter_password, clone_name, cpu_count, memory_mb, disk_size_gb):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_name_to_reconfigure = clone_name

    target_cpu_count = int(cpu_count)
    #target_cpu_count değeri string olarak gelmektedir. Bu yüzden int'e çeviriyoruz.
    target_memory_mb = int(memory_mb)
    #target_disk_size_gb değeri long olmalı
    target_disk_size_gb = int(disk_size_gb)

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} not found.")
        return

    # VM Power On durumunda ise shutdown et
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print(f"{vm_name_to_reconfigure} Powering off VM...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    reconfigure_vm(vm_to_reconfigure, target_cpu_count, target_memory_mb, target_disk_size_gb)

    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        print(f"{vm_name_to_reconfigure} Powering on VM...")
        task = vm_to_reconfigure.PowerOnVM_Task()
        WaitForTask(task)

    Disconnect(service_instance)

