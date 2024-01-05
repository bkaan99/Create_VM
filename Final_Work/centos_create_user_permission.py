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
    vm_name = "centos_clone"  # Linux sanal makinenizin adını buraya ekleyin

    os_username = "cekino"

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

if __name__ == "__main__":
    main()