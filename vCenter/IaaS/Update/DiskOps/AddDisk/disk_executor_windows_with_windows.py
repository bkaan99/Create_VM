import string
from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def get_vm_disk_info(vm):
    disk_info = []

    for device in vm.config.hardware.device:
        if isinstance(device, vim.VirtualDisk):
            disk_name = device.deviceInfo.label
            disk_size_gb = device.capacityInKB / (1024 * 1024)  # Byte cinsinden kapasiteyi GB'ye çevir
            disk_info.append({"Disk Name": disk_name, "Disk Size (GB)": disk_size_gb})

    return disk_info

def wait_for_task(task):
    """Waits and provides updates on a vSphere task until it is completed."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Task completed successfully.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Error: {task.info.error}")
            task_done = True

def main(target_vm_name, vCenter_host_ip, vCenter_user, vCenter_password):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    target_vm = get_vm_by_name(content, target_vm_name)

    if target_vm is None:
        print(f"VM {target_vm_name} not found.")
        Disconnect(service_instance)
        return

    # Sanal makine disk bilgileri
    vm_disk_info = get_vm_disk_info(target_vm)
    #sonuncu disk numarasını al
    last_disk_number = int(vm_disk_info[-1]["Disk Name"].split(" ")[-1]) - 1

    allowed_letters = string.ascii_uppercase[4 + len(vm_disk_info):]  # "E" harfinden başlayarak "Z" harfine kadar olan harfler
    current_letter = allowed_letters[0]


    # Disk set ayarları
    label = "Glass_House_Disk_" + str(last_disk_number)
    assign_letter = current_letter
    disk_number = last_disk_number
    create_partition_type = "primary"

    #os credentials
    os_user = "cekino"
    os_password = "1234"

    # CMD komutları
    cmd_commands = (
        f'echo select disk {disk_number} > diskpart_commands.txt && ',
        'echo clean >> diskpart_commands.txt && ',
        f'echo create partition {create_partition_type} >> diskpart_commands.txt && ',
        f'echo assign letter={assign_letter} >> diskpart_commands.txt && ',
        f'echo format fs=ntfs label={label} quick >> diskpart_commands.txt && ',
        'echo exit >> diskpart_commands.txt && ',
        'start /wait diskpart /s diskpart_commands.txt && ',
        'del diskpart_commands.txt'
    )

    # CMD komutlarını sanal makinede çalıştırma
    try:
        auth = vim.vm.guest.NamePasswordAuthentication(
            username = os_user,
            password = os_password
        )
        pm = content.guestOperationsManager.processManager

        cmd_string = ''.join(cmd_commands)
        ps = vim.vm.guest.ProcessManager.ProgramSpec(
            programPath="C:\\Windows\\System32\\cmd.exe",
            arguments=f'/c "{cmd_string}"'
        )

        pid = pm.StartProgramInGuest(target_vm, auth, ps)
        print(f"Command started with PID {pid}")
        wait_for_task(pm.ListProcessesInGuest(target_vm, auth, [pid])[0])
    except Exception as e:
        print(f"Error: {e}")

    Disconnect(service_instance)
