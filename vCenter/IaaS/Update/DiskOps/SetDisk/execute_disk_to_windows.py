import time
from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *


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

def main(target_vm_name, vCenter_host_ip, vCenter_user, vCenter_password, label, assign_letter, disk_number):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    target_vm = get_vm_by_name(content, target_vm_name)

    if target_vm is None:
        print(f"VM {target_vm_name} not found.")
        Disconnect(service_instance)
        return

    # Disk set ayarları
    #label = "Glass_House_Disk"
    #assign_letter = "G"
    #disk_number = 1
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
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
