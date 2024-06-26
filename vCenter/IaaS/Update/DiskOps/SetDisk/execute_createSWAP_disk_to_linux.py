from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
from pyVmomi import vim


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

def create_swap(content, target_vm, auth, added_disk_full_path_name):
    # Yeni disk için swap alanı oluşturma
    cmd_create_swap = f"sudo mkswap {added_disk_full_path_name}1 && sudo swapon {added_disk_full_path_name}1"
    spec_create_swap = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/bash",
                                                               arguments=f"-c '{cmd_create_swap}'")
    pid_create_swap = content.guestOperationsManager.processManager.StartProgramInGuest(target_vm, auth,
                                                                                         spec_create_swap)
    print(f"Creating swap on new disk with PID {pid_create_swap}")

def main(vm_name, vCenter_host_ip, vCenter_user, vCenter_password):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

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
        disk_device = "/dev/sd"
        added_disk_full_path_name = disk_device + added_disk_label

        # Swap alanı oluşturma
        create_swap(content, target_vm, auth, added_disk_full_path_name)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)
