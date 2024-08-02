from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
from pyVmomi import vim
import time

def clone_template(content, template_name, clone_name, disk_size_gb, disk_mode,memory_mb, cpu_count):

    template = get_template_by_name(content, template_name)

    if not template:
        print(f"{template_name} adında bir template bulunamadı.")
        exit(1)

    #TODO: Buraya vm'i kuraağımız alanı dinamik yapmamız gerekecek. Şuan için default olarak vm_folder = template.parent
    vm_folder = template.parent

    clone_spec = create_clone_spec(content, template, vm_folder, clone_name, disk_size_gb, disk_mode ,memory_mb, cpu_count)
    clone_task = template.CloneVM_Task(folder=vm_folder, name=clone_name, spec=clone_spec)

    print(f"{template_name} Template VM'i kopyalanıyor. Lütfen bekleyin...")
    while clone_task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        continue

    if clone_task.info.state == vim.TaskInfo.State.success:
        print("Template Clone işlemi başarılı:", clone_name)
    else:
        print("Error cloning template:", clone_task.info.error.msg)

def get_template_by_name(content, template_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.config.template and vm.name == template_name:
            return vm
    return None

def create_clone_spec(content, template, folder, clone_name, disk_size_gb, disk_mode, memory_mb, cpu_count):
    clone_spec = vim.vm.CloneSpec()
    relocate_spec = vim.vm.RelocateSpec()
    relocate_spec.folder = folder
    resource_pool = get_resource_pool(content)
    relocate_spec.pool = resource_pool
    clone_spec.location = relocate_spec
    clone_spec.powerOn = True

    clone_spec.config = vim.vm.ConfigSpec()
    clone_spec.config.name = clone_name

    # CPU ve bellek ayarlarını yapın
    clone_spec.config.numCPUs = cpu_count
    clone_spec.config.memoryMB = memory_mb

    # Disk ayarları
    device_changes = []
    for device in template.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualDisk):
            if disk_size_gb < device.capacityInKB / 1024 ** 2:
                disk_size_gb = device.capacityInKB / 1024 ** 2
            disk_spec = vim.vm.device.VirtualDeviceSpec()
            disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            disk_spec.device = device
            #disk_size_gb değeri var olan boyuttan büyük olmalı (GB)
            disk_spec.device.capacityInKB = int(disk_size_gb * 1024 * 1024)

            # Disk modunu ayarla
            if disk_mode == 0:
                disk_spec.device.backing.diskMode = 'persistent'
            elif disk_mode == 1:
                disk_spec.device.backing.diskMode = 'independent_persistent'
            elif disk_mode == 2:
                disk_spec.device.backing.diskMode = 'independent_nonpersistent'

            device_changes.append(disk_spec)
    clone_spec.config.deviceChange = device_changes

    return clone_spec

def get_resource_pool(content):
    resource_pool = None
    clusters = get_cluster_list(content)
    if clusters:
        rp = clusters[0].resourcePool
        resource_pool = rp
    return resource_pool

def get_cluster_list(content):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.ClusterComputeResource], True)
    cluster_list = container.view
    return cluster_list

def main(vCenter_host_ip, vCenter_user, vCenter_password, template_name, clone_name, disk_size_gb, disk_mode, memory_mb, cpu_count):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    if not service_instance:
        print("Failed to connect to vSphere server.")
        sys.exit(1)

    try:
        # Call clone_template function with desired template name and clone name
        clone_template(content= content,
                       template_name= template_name,
                       clone_name= clone_name,
                       disk_size_gb= disk_size_gb,
                       disk_mode= disk_mode,
                       memory_mb= memory_mb,
                       cpu_count= cpu_count)
        time.sleep(2)
        # vm poweroff ise poweron yap
        if clone_name is not None:
            vm = get_vm_by_name(content, clone_name)
            if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
                print(f"{clone_name} powered off olduğu için açılıyor...")
                task = vm.PowerOnVM_Task()
                #TODO: Buraya while ile power on işlemi beklenebilir.Şuan için gerekli değil.

    except Exception as e:
        print("Clone Error:", e)

    # Disconnect from vSphere server
    Disconnect(service_instance)

if __name__ == "__main__":
    main(vCenter_host_ip="10.14.45.10",
         vCenter_user="administrator@vsphere.local",
         vCenter_password="Aa112233!",
         template_name="Win2019_test_template",
         clone_name="bülent_test_clone",
         disk_size_gb=20,
         disk_mode=0,
         memory_mb=2048,
         cpu_count=2)