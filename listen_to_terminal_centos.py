import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def run_lsblk(content, vm, auth):
    try:
        process_manager = content.guestOperationsManager.processManager

        # lsblk komutunu çalıştır
        spec = vim.vm.guest.ProcessManager.ProgramSpec(
            programPath="/bin/bash",
            arguments=f"-c 'lsblk'"
        )

        pid = process_manager.StartProgramInGuest(vm, auth, spec)
        print(f"Started process with PID {pid}")

        # Sürecin çıkışını bekleyin
        process_info = process_manager.ListProcessesInGuest(vm, auth, [pid])[0]
        while process_info.exitCode is None:
            process_info = process_manager.ListProcessesInGuest(vm, auth, [pid])[0]

        print(f"Process exited with code {process_info.exitCode}")

        # Sürecin çıktısını al
        if process_info.exitCode == 0:
            output = process_manager.ReadProcessOutput(vm, auth, pid, True, True)
            print("lsblk output:\n", output)

    except Exception as e:
        print(f"Error: {e}")

def main():
    # ESXi bilgileri
    esxi_host = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    # VM bilgileri
    vm_name = "esxi_centos_sali"  # İzlemek istediğiniz Linux sanal makinenizin adını buraya ekleyin

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
            password="1234"  # İzlemek istediğiniz Linux sanal makinesinin şifresini buraya ekleyin
        )

        # lsblk komutunu sanal makine içinde çalıştırma
        run_lsblk(content, target_vm, auth)

    finally:
        Disconnect(service_instance)

if __name__ == "__main__":
    main()
