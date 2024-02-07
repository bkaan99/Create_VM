from pyVim.connect import Disconnect
from pyVmomi import vim
from ESXi.IaaS.ESXi_Connection.esxi_connection import *

def main(vm_name, esxi_host_ip, esxi_user, esxi_password):

    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)

    # Belirtilen sanal makineyi bul
    target_vm = get_vm_by_name(content, vm_name)

    if target_vm is None:
        print(f"VM {vm_name} not found.")
        Disconnect(service_instance)
        return

    try:
        # Mevcut IP adresini al
        current_ip = target_vm.summary.guest.ipAddress
        # Yeni IP adresini setle
        new_ip = "10.14.45.109"
        new_dns = "1.1.1.1"

        auth = vim.vm.guest.NamePasswordAuthentication(
            username="root",
            password="1234"
        )

        # Mevcut IP adresini sil
        if current_ip:
            cmd_del_ip = f"sudo ip addr del {current_ip}/24 dev ens192"
            spec_del_ip = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_del_ip}'")
            pid_del_ip = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_del_ip)
            print(f"Deleting current IP with PID {pid_del_ip}")

        # Yeni IP adresini setle
        cmd_set_ip = f"sudo ip addr add {new_ip}/24 dev ens192 && sudo ip route add default via 10.14.45.1"
        spec_set_ip = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_set_ip}'")
        pid_set_ip = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_set_ip)
        print(f"Setting new IP with PID {pid_set_ip}")

        # DNS adresini setle
        cmd2 = f'echo "nameserver {new_dns}" | sudo tee /etc/resolv.conf > /dev/null'
        spec2 = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd2}'")
        pid2 = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec2)

        cmd3 = f'echo "nameserver {"8.8.8.8"}" | sudo tee /etc/resolv.conf > /dev/null'
        spec3 = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd3}'")
        pid3 = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec3)
        print(f"Setting DNS with PID {pid2}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)

if __name__ == "__main__":
    main()