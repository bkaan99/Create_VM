import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def main():
    # ESXi bilgileri
    esxi_host = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    # VM bilgileri
    vm_name = "SUSE-Temp-15-3"

    # ESXi'ye bağlan
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, sslContext=ssl_context)
    content = service_instance.RetrieveContent()

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
        new_ip = "200.14.45.141"
        new_dns = "1.1.1.1"

        device_spec_name = "ens192"

        VM_username = "root"
        VM_password = "111111"

        auth = vim.vm.guest.NamePasswordAuthentication(
            username= VM_username,
            password= VM_password
        )

        # Mevcut IP adresini sil
        if current_ip:
            cmd_del_ip = f"sudo ip addr del {current_ip}/24 dev {device_spec_name}"
            spec_del_ip = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_del_ip}'")
            pid_del_ip = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_del_ip)
            print(f"Deleting current IP with PID {pid_del_ip}")

        # Yeni IP adresini setle
        cmd_set_ip = f"sudo ip addr add {new_ip}/24 dev {device_spec_name} && sudo ip route add default via 10.14.45.1"
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
