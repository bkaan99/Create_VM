import time
from pyVim.connect import Disconnect
from pyVmomi import vim
from ESXi.IaaS.ESXi_Connection.esxi_connection import *


def main():
    esxi_host = "10.14.45.10"
    esxi_user = "administrator@vsphere.local"
    esxi_password = "Aa112233!"

    vm_name= "bkaan_sapaas"

    service_instance, content = create_vsphere_connection(esxi_host, esxi_user, esxi_password)

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
        new_ip = "13.13.13.13"
        new_dns = "1.1.1.1"

        auth = vim.vm.guest.NamePasswordAuthentication(
            username="root",
            password="111111"
        )

        # Mevcut IP adresini sil
        if current_ip:
            cmd_del_ip = f"sudo ip addr del {current_ip}/24 dev ens192"
            spec_del_ip = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_del_ip}'")
            pid_del_ip = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_del_ip)
            print(f"Deleting current IP with PID {pid_del_ip}")

        # Yeni IP adresini setle
        cmd_set_ip = f"echo \"IPADDR='{new_ip}'\nNAME=''\nBOOTPROTO='static'\nSTARTMODE='auto'\nZONE=''\nDEVICE='eth0'\nONBOOT=yes\nPREFIX=24\" | sudo tee /etc/sysconfig/network/ifcfg-eth0 > /dev/null"
        spec_set_ip = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_set_ip}'")
        pid_set_ip = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_set_ip)
        print(f"Setting new IP with PID {pid_set_ip}")

        # # DNS adresini setle
        # cmd_set_dns = f"sudo bash -c 'echo -e \"nameserver {new_dns}\" > /etc/resolv.conf'"
        # spec_set_dns = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_set_dns}'")
        # pid_set_dns = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_set_dns)
        # print(f"Setting DNS with PID {pid_set_dns}")

        cmd3 = f'echo "nameserver {"8.8.8.8"}" | sudo tee /etc/resolv.conf > /dev/null'
        spec3 = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd3}'")
        pid3 = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec3)
        print(f"Setting DNS with PID {pid3}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)

if __name__ == "__main__":
    main()
    time.sleep(5)