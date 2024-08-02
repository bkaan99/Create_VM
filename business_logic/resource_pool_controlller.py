from vCenter.IaaS.Connections.vSphere_connection import *
from pyVim.connect import Disconnect

def resource_pool_creator(content, resource_pool_name, datacenter_name):
    datacenter = None
    for dc in content.rootFolder.childEntity:
        if dc.name == datacenter_name:
            datacenter = dc
            break

    if not datacenter:
        raise Exception(f"Datacenter '{datacenter_name}' not found.")

    resource_pool_spec = vim.ResourceConfigSpec()
    resource_pool_spec.cpuAllocation = vim.ResourceAllocationInfo()
    resource_pool_spec.cpuAllocation.limit = -1
    resource_pool_spec.cpuAllocation.reservation = 0
    resource_pool_spec.cpuAllocation.shares = vim.SharesInfo()
    resource_pool_spec.cpuAllocation.shares.level = "normal"
    resource_pool_spec.cpuAllocation.shares.shares = 1000

    resource_pool_spec.memoryAllocation = vim.ResourceAllocationInfo()
    resource_pool_spec.memoryAllocation.limit = -1
    resource_pool_spec.memoryAllocation.reservation = 0
    resource_pool_spec.memoryAllocation.shares = vim.SharesInfo()
    resource_pool_spec.memoryAllocation.shares.level = "normal"
    resource_pool_spec.memoryAllocation.shares.shares = 1000

    try:
        task = datacenter.resourcePool.CreateResourcePool_Task(name=resource_pool_name, spec=resource_pool_spec)
        return task

    except Exception as e:
        print(f"Resource Pool Oluşturulurken Hata Oluştu: {e}")
        return
def main():
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    service_instance, content = create_vsphere_connection(host=vCenter_host_ip, user=vCenter_user, password=vCenter_password)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
