from vCenter.IaaS.Connections.vSphere_connection import *
from pyVim.connect import Disconnect
from pyVmomi import vim, vmodl

def create_resource_pool(content, cluster_name, resource_pool_name):
    cluster = None
    for datacenter in content.rootFolder.childEntity:
        for cluster_obj in datacenter.hostFolder.childEntity:
            if cluster_obj.name == cluster_name:
                cluster = cluster_obj
                break
        if cluster:
            break

    if not cluster:
        raise Exception(f"Cluster '{cluster_name}' bulunamadı.")

    rp_spec = vim.ResourceConfigSpec()

    cpu_allocation = vim.ResourceAllocationInfo()
    cpu_allocation.shares = vim.SharesInfo(level="high", shares=8000)
    cpu_allocation.reservation = 12
    cpu_allocation.expandableReservation = True
    cpu_allocation.limit = 100


    memory_allocation = vim.ResourceAllocationInfo()
    memory_allocation.shares = vim.SharesInfo(level="high", shares=500000)
    memory_allocation.reservation = 12
    memory_allocation.expandableReservation = True
    memory_allocation.limit = 26000

    rp_spec.cpuAllocation = cpu_allocation
    rp_spec.memoryAllocation = memory_allocation

    try:
        resource_pool = cluster.resourcePool.CreateResourcePool(name=resource_pool_name, spec=rp_spec)
        print(f"'{resource_pool_name}' isimli Resource Pool başarıyla oluşturuldu.")
        return resource_pool
    except vim.fault.DuplicateName as error:
        print(f"Aynı isimde bir Resource Pool mevcut: {error}")
    except vim.fault.InvalidName as error:
        print(f"Geçersiz isim: {error}")
    except Exception as e:
        print(f"Resource Pool oluşturulurken hata: {str(e)}")


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def create_vm_folder(content, datacenter_name, folder_name):
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if datacenter is None:
        print(f"Datacenter '{datacenter_name}' not found")
        return

    ds_browser = datacenter.vmFolder
    if ds_browser:
        try:
            ds_browser.CreateFolder(folder_name)
            print(f"Datastore folder '{folder_name}' created in datacenter '{datacenter_name}'")
        except vim.fault.AlreadyExists:
            print(f"Datastore folder '{folder_name}' already exists in datacenter '{datacenter_name}'")
        except Exception as e:
            print(f"Error creating datastore folder: {e}")
    else:
        print(f"Datastore folder not found in datacenter '{datacenter_name}'")



def main():
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    cluster_name = "Cluster01"
    resource_pool_name = "New Resource Pool_ TEST!!!!"

    create_resource_pool(content, cluster_name, resource_pool_name)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
