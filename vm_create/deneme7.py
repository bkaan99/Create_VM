import subprocess
import time
import psutil
import os

DEFAULT_ISO_PATH = "/ex_files/Core-current.iso"

def create_vm(vm_name, memory_size_mb, iso_path):
    # Validate inputs
    if not isinstance(memory_size_mb, int) or memory_size_mb <= 0:
        raise ValueError("Memory size must be a positive integer.")

    # If iso_path is not provided or the file does not exist, use the default ISO path
    if not iso_path or not os.path.exists(iso_path):
        print(f"Provided ISO path is invalid. Using the default ISO path: {DEFAULT_ISO_PATH}")
        iso_path = DEFAULT_ISO_PATH

    # Construct QEMU command
    qemu_command = [
        "qemu-system-x86_64",
        "-name", vm_name,
        "-m", str(memory_size_mb),
        "-cdrom", iso_path,
        "-boot", "d",
        "-net", "nic",
        "-net", "user",
        "-nographic"  # Disable graphical output
    ]

    try:
        # Run QEMU command in the background
        qemu_process = subprocess.Popen(qemu_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        # Optionally, you can wait for a few seconds to ensure the VM is up and running
        time.sleep(5)

        return qemu_process
    except subprocess.CalledProcessError as e:
        print(f"Error starting VM: {e}")
        raise

def is_process_running(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False

def list_running_vms(process_name):
    running_vms = []
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == process_name and process.info['cmdline']:
            vm_name = process.info['cmdline'][-1]  # Assuming the VM name is the last argument in the command line
            running_vms.append((process.info['pid'], vm_name))
    return running_vms

def terminate_vm(pid_to_terminate):
    try:
        process = psutil.Process(pid_to_terminate)
        process.terminate()
        process.wait(timeout=5)  # Wait for the process to exit

        # If the process is still running after waiting, force termination
        if process.is_running():
            process.kill()
            process.wait()

        print(f"VM with PID {pid_to_terminate} terminated.")
    except Exception as e:
        print(f"Error terminating VM: {e}")


if __name__ == "__main__":
    try:
        while True:
            print("\n1. VM Oluştur")
            print("2. Çalışan VM'leri Listele")
            print("3. VM'i Sonlandır")
            print("0. Çıkış")

            choice = input("Seçiminizi yapın (0-3): ")

            if choice == "1":
                # VM oluştur
                vm_name = input("Virtual machine name: ")
                memory_size_mb = int(input("Memory size in MB: "))
                iso_path = input("ISO path (leave empty to use default): ")
                vm_process = create_vm(vm_name, memory_size_mb, iso_path)
                print(f"{vm_name} started in the background.")

            elif choice == "2":
                # Çalışan VM'leri listele
                process_name = "qemu-system-x86_64"
                running_vms = list_running_vms(process_name)
                if running_vms:
                    print("Running VMs:")
                    for i, (pid, vm_name) in enumerate(running_vms, start=1):
                        print(f"  {i}. VM Name: {vm_name}, PID: {pid}")
                else:
                    print("No running VMs.")

            elif choice == "3":
                process_name = "qemu-system-x86_64"
                running_vms = list_running_vms(process_name)
                if running_vms:
                    for i, (pid, vm_name) in enumerate(running_vms, start=1):
                        print(f"  {i}. VM Name: {vm_name}, PID: {pid}")
                    choice_to_terminate = int(input("Terminate VM (enter the number): "))
                    if 1 <= choice_to_terminate <= len(running_vms):
                        pid_to_terminate = running_vms[choice_to_terminate - 1][0]
                        terminate_vm(pid_to_terminate)
                    else:
                        print("Invalid choice.")
                else:
                    print("No running VMs.")

            elif choice == "0":
                print("Exiting.")
                break

            else:
                print("Invalid choice.")

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Stopping the virtual machine.")
        vm_process.terminate()
