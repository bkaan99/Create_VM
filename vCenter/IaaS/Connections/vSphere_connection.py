import sys
from pyVim import connect
import ssl
from pyVmomi import vim
import socket


def create_vsphere_connection(host: str, user: str, password: str, timeout=10):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        socket.create_connection((host, 443), timeout=timeout)
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=password,
                                                sslContext=ssl_context)

        content = service_instance.RetrieveContent()

        return service_instance, content

    except ssl.SSLError as e:
        print(f"SSL Hatası: {e}")
        sys.exit(1)

    except socket.timeout as e:
        print(f"Soket Zaman Aşımı Hatası: {e}")
        sys.exit(1)

    except socket.error as e:
        print(f"Soket Hatası: {e}")
        sys.exit(1)

    except vim.fault.InvalidLogin as e:
        print(f"Geçersiz Giriş Hatası: {e}")
        sys.exit(1)

    except vim.fault.HostConnectFault as e:
        print(f"Ana Bilgisayar Bağlantı Hatası: {e}")
        sys.exit(1)

    except vim.fault.NoPermission as e:
        print(f"Izin Hatası: {e}")
        sys.exit(1)

    except vim.fault.NotFound as e:
        print(f"Bulunamadı Hatası: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        sys.exit(1)


def get_vm_by_name(content, vm_name: str):
    try:
        container_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        for vm in container_view.view:
            if vm.name == vm_name:
                return vm
        return None

    except Exception as e:
        print("Sanal makine aranırken hata oluştu:", str(e))
