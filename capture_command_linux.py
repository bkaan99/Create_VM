import ssl
import time
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim


def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None


def capture_command_output(vm, content, auth, command, output_file_path, timeout=10):
    pm = content.guestOperationsManager.processManager
    cmd = f"{command} > {output_file_path}"

    #cmd = f"{command} | tee {output_file_path}"
    ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=cmd)
    res = pm.StartProgramInGuest(vm, auth, ps)

    start_time = time.time()

    try:
        while time.time() - start_time < timeout:
            time.sleep(1)
            try:
                file_info = content.guestOperationsManager.fileManager.GetFileInfoInGuest(vm, auth, output_file_path)
                if file_info is not None:
                    print(f"Command output saved to {output_file_path}")
                    return
            except vim.fault.FileNotFound:
                pass

        print(f"Error: File {output_file_path} was not found after waiting.")

    except Exception as e:
        print(f"Error: {e}")


def main():
    esxi_host = "10.14.45.10"
    esxi_user = "administrator@vsphere.local"
    esxi_password = "Aa112233!"

    vm_name = "bkaan_sapaas"
    vm_username = "root"
    vm_password = "111111"

    command = "lsblk"
    output_file_path = "/tmp/output.txt"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, sslContext=ssl_context)
    content = service_instance.RetrieveContent()

    target_vm = get_vm_by_name(content, vm_name)

    if target_vm is None:
        print(f"VM with name {vm_name} not found.")
        Disconnect(service_instance)
        return

    try:
        auth = vim.vm.guest.NamePasswordAuthentication(username=vm_username, password=vm_password)

        capture_command_output(target_vm, content, auth, command, output_file_path)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)


if __name__ == "__main__":
    main()
