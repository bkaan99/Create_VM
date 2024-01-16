import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def find_highest_disk_number(vm):
    highest_disk_number = 0
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualDisk):
            disk_label = device.deviceInfo.label
            try:
                disk_number = int(disk_label.split()[-1])
                highest_disk_number = max(highest_disk_number, disk_number)
            except ValueError:
                pass  # Disk numarasını çıkaramazsak (örneğin, "Harddisk" gibi bir etiket varsa), hatayı yok say

    return highest_disk_number

def get_letter_for_disk_number(disk_number):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if disk_number <= len(alphabet):
        return alphabet[disk_number - 1]
    else:
        # Eğer disk numarası alfabedeki harf sayısından büyükse, "AA", "AB", "AC", vb. gibi kombinasyonlarla devam eder.
        quotient, remainder = divmod(disk_number - 1, len(alphabet))
        return alphabet[quotient - 1] + alphabet[remainder]

def main():
    # ESXi bilgileri
    esxi_host = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    # VM bilgileri
    vm_name = "esxi_centos_bkaan"  # Linux sanal makinenizin adını buraya ekleyin

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

        highest_disk_number = find_highest_disk_number(target_vm)

        # Disk numarasına göre alfabede karşılık gelen harfi bul
        letter_for_disk_number = get_letter_for_disk_number(highest_disk_number)
        added_disk_label = letter_for_disk_number.lower()

        # Yeni disk oluşturma ve mount işlemleri
        disk_device = "/dev/sd"  # Burada disk cihazının başlangıç değerini tanımlayın
        added_disk_full_path_name = disk_device + added_disk_label

        cmd_create_disk = f"sudo parted {added_disk_full_path_name} <<EOF\n" \
                          "mklabel gpt\n" \
                          "mkpart  primary xfs 1MiB 100%\n" \
                          "quit\n" \
                          "EOF"
        spec_create_disk = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                                   arguments=f"-c '{cmd_create_disk}'")
        pid_create_disk = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                            spec_create_disk)
        print(f"Creating new disk with PID {pid_create_disk}")

        cmd_format_disk = f"sudo mkfs.xfs {added_disk_full_path_name}1"
        spec_format_disk = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                                   arguments=f"-c '{cmd_format_disk}'")
        pid_format_disk = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                            spec_format_disk)
        print(f"Formatting new disk with PID {pid_format_disk}")

        cmd_create_mount_point = "sudo mkdir /hana/log"
        spec_create_mount_point = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                                          arguments=f"-c '{cmd_create_mount_point}'")
        pid_create_mount_point = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                                   spec_create_mount_point)
        print(f"Creating mount point with PID {pid_create_mount_point}")

        # /etc/fstab dosyasını düzenleme
        cmd_edit_fstab = f'echo "{added_disk_full_path_name}1   /hana/log   xfs    defaults    0   0" | sudo tee -a /etc/fstab'
        spec_edit_fstab = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                                  arguments=f"-c '{cmd_edit_fstab}'")
        pid_edit_fstab = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                           spec_edit_fstab)
        print(f"Editing /etc/fstab with PID {pid_edit_fstab}")

        # Systemd'i yeniden yükle
        cmd_reload_systemd = "sudo systemctl daemon-reload"
        spec_reload_systemd = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                                      arguments=f"-c '{cmd_reload_systemd}'")
        pid_reload_systemd = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                               spec_reload_systemd)
        print(f"Reloading systemd with PID {pid_reload_systemd}")

        # Mount etme
        cmd_mount = f'sudo mount {added_disk_full_path_name}1  /hana/log'
        spec_mount = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash", arguments=f"-c '{cmd_mount}'")
        pid_mount = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth, spec_mount)
        print(f"Mounting new disk with PID {pid_mount}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)

if __name__ == "__main__":
    main()
