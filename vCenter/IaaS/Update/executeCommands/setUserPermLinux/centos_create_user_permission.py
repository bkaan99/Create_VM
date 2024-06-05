from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def main(vm_name, vCenter_host_ip, vCenter_user, vCenter_password):
    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    # TODO: Burada hangi kullanıcıya yetki verilecekse onun adı yazılacak
    os_username = "bkaan"

    target_vm = get_vm_by_name(content, vm_name)

    if target_vm is None:
        print(f"VM {vm_name} not found.")
        Disconnect(service_instance)
        return

    try:
        auth = vim.vm.guest.NamePasswordAuthentication(
            username="root",
            password="1234"
        )

        # Yeni disk oluşturma ve mount işlemleri
        cmd_create_disk = f"""su root
        echo "{os_username} ALL=(ALL) ALL" | sudo tee -a /etc/sudoers
                """
        spec_create_perm = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                                   arguments=f"-c '{cmd_create_disk}'")
        pid_create_perm = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                            spec_create_perm)
        print(f"Creating perm on '{os_username}' with PID {pid_create_perm}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)