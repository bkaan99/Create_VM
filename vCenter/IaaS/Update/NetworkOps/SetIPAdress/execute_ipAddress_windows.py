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

def main(vm_name ,vCenter_host_ip, vCenter_user, vCenter_password, ipAddress):

    # vCenter'a bağlanın
    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)
    target_vm = get_vm_by_name(content, vm_name)

    if target_vm is None:
        print(f"VM {vm_name} not found.")
        Disconnect(service_instance)
        return

    # Komut istemcisine yazılacak komutları oluşturun
    cmd_command = (
        f'netsh interface ip set address name="Ethernet0" static '
        f'{ipAddress} 255.255.255.0 10.14.45.1'
    )

    dns_script = (
        f'netsh interface ip set dns name="Ethernet0" static '
        f'8.8.8.8 &&'
        f'netsh interface ip add dns name="Ethernet0" 8.8.4.4'
    )

    auth = vim.vm.guest.NamePasswordAuthentication(
        username="cekino",
        password="1234"
    )
    pm = content.guestOperationsManager.processManager

    # Komutu sanal makinede çalıştırma
    try:
        # Komutları sırayla çalıştırma
        for script in [cmd_command]:
            ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath="C:\\Windows\\System32\\cmd.exe",
                arguments=f'/c "{script}"'
            )
            pid = pm.StartProgramInGuest(target_vm, auth, ps)
            print(f"Command started with PID {pid}")
            print("Komutlar sırayla çalıştırıldı.")
            wait_for_task(pm.ListProcessesInGuest(target_vm, auth, [pid])[0])
    except Exception as e:
        print(f"Error: {e}")


    try:
        for script in [dns_script]:
            ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath="C:\\Windows\\System32\\cmd.exe",
                arguments=f'/c "{script}"'
            )
            pid = pm.StartProgramInGuest(target_vm, auth, ps)
            print(f"Command started with PID {pid}")
            wait_for_task(pm.ListProcessesInGuest(target_vm, auth, [pid])[0])

    except Exception as e:
        print(f"Error: {e}")

    Disconnect(service_instance)
