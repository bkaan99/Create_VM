import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import paramiko

def execute_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None


def remove_existing_ip(ssh, existing_ip):
    # Önceki IP'yi kaldırma komutunu belirtin
    remove_ip_command = f'sudo ip addr del {existing_ip} dev ens192'

    # Komutu çalıştırma
    output, error = execute_command(ssh, remove_ip_command)
    if not error:
        print(f"Removed existing IP successfully: {existing_ip}")
    else:
        print(f"Error removing existing IP: {error.strip()}")


def main():
    # ESXi bilgileri
    esxi_host = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    # VM bilgileri
    vm_name = "centos_clone"
    existing_ip = "10.14.45.171"

    # SSH bilgileri
    ssh_user = "root"
    ssh_password = "1234"

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

    # Sanal makineye bağlan
    vm_ip_address = existing_ip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())



    try:
        ssh.connect(vm_ip_address, username=ssh_user, password=ssh_password)

        # Mevcut IP'yi kaldır

        # Yeni IP'yi ekle

        # IP ve DNS ayarlarını değiştiren komutları belirtin
        ip_command = 'sudo ip addr add 10.14.45.163/24 dev ens192 && sudo ip route add default via 10.14.45.1'
        dns_command = 'echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf > /dev/null'

        # Komutları sırayla çalıştırma
        for cmd in [ip_command, dns_command]:
            output, error = execute_command(ssh, cmd)
            if not error:
                print(f"Command executed successfully: {output.strip()}")
            else:
                print(f"Error executing command: {error.strip()}")

        remove_existing_ip(ssh, existing_ip)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()
        Disconnect(service_instance)

if __name__ == "__main__":
    main()
