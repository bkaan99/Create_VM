from vCenter.IaaS.Connections.vSphere_connection import *
from pyVim.connect import Disconnect
from pyVmomi import vim, vmodl

# def dswitch_creator(content):
#     dvs_name = "DVS-Test"
#     dvs_spec = vim.DVSCreateSpec()
#     dvs_spec.configSpec = vim.VMwareDVSConfigSpec()
#     dvs_spec.configSpec.name = dvs_name
#     dvs_spec.configSpec.maxMtu = 9000
#     dvs_spec.configSpec.uplinkPortPolicy = vim.DVSNameArrayUplinkPortPolicy()
#     dvs_spec.configSpec.uplinkPortPolicy.uplinkPortName = ["Uplink1", "Uplink2"]
#     dvs_spec.configSpec.numStandalonePorts = 4
#     dvs_spec.configSpec.linkDiscoveryProtocolConfig = vim.LinkDiscoveryProtocolConfig()
#     dvs_spec.configSpec.linkDiscoveryProtocolConfig.protocol = "CDP"
#     dvs_spec.configSpec.linkDiscoveryProtocolConfig.operation = "listen"
#     dvs_spec.configSpec.linkDiscoveryProtocolConfig.adminInterval = 60
#     dvs_spec.configSpec.networkResourceManagementEnabled = True
#     dvs_spec.configSpec.defaultPortConfig = vim.VMwareDVSPortSetting()
#     dvs_spec.configSpec.defaultPortConfig.vlan = vim.VmwareDistributedVirtualSwitchVlanIdSpec()
#     dvs_spec.configSpec.defaultPortConfig.vlan.vlanId = 0
#     dvs_spec.configSpec.defaultPortConfig.vlan.inherited = False
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy = vim.VMwareDVSSecurityPolicy()
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.allowPromiscuous = vim.BoolPolicy()
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.allowPromiscuous.value = False
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.forgedTransmits = vim.BoolPolicy()
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.forgedTransmits.value = False
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.macChanges = vim.BoolPolicy()
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.macChanges.value = False
#     dvs_spec.configSpec.defaultPortConfig.securityPolicy.inherited = False
#
#     dvs_folder = content.dvSwitchManager.networkFolder
#     task = dvs_folder.CreateDVS_Task(dvs_spec)
#     WaitForTask(task, service_instance)
#     print(f"{dvs_name} isimli DVS başarıyla oluşturuldu.")
#
#     return dvs_name

def create_dvs(content, dvs_name, datacenter_name):
    datacenter = None
    for dc in content.rootFolder.childEntity:
        if dc.name == datacenter_name:
            datacenter = dc
            break

    if not datacenter:
        raise Exception(f"Datacenter '{datacenter_name}' not found.")

    dvs_config_spec = vim.DistributedVirtualSwitch.ConfigSpec()
    dvs_config_spec.name = dvs_name
    dvs_config_spec.description= "DVS created by BKAAN"
    dvs_config_spec.uplinkPortPolicy = vim.DistributedVirtualSwitch.NameArrayUplinkPortPolicy()
    dvs_config_spec.uplinkPortPolicy.uplinkPortName = ["dvUplink1", "dvUplink2"]

    dvs_create_spec = vim.DistributedVirtualSwitch.CreateSpec()
    dvs_create_spec.configSpec = dvs_config_spec

    try:
        task = datacenter.networkFolder.CreateDVS_Task(spec=dvs_create_spec)
        return task
    except vmodl.MethodFault as error:
        print(f"Caught vmodl fault : {error.msg}")
    except Exception as e:
        print(f"Caught exception : {str(e)}")

def get_dswitch(content):
    dvs_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    dvs = dvs_view.view
    return dvs

def get_datacenter(content):
    datacenter_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datacenter], True)
    datacenters = datacenter_view.view
    return datacenters

def create_dvportgroup(content, dvs_name, dvportgroup_name, vlan_type=None):
    dvs = None
    for dvs in get_dswitch(content):
        if dvs.name == dvs_name:
            break

    if not dvs:
        raise Exception(f"Distributed Virtual Switch '{dvs_name}' not found.")

    #check dvs_name is already exist
    for dvportgroup in dvs.portgroup:
        if dvportgroup.name == dvportgroup_name:
            raise Exception(f"Distributed Virtual Portgroup '{dvportgroup_name}' already exists.")

    dvportgroup_spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
    dvportgroup_spec.name = dvportgroup_name
    dvportgroup_spec.numPorts = 12
    dvportgroup_spec.type = vim.dvs.DistributedVirtualPortgroup.PortgroupType.earlyBinding

    if vlan_type == "trunk":
        vlan_trunk_spec = vim.dvs.VmwareDistributedVirtualSwitch.TrunkVlanSpec()
        vlan_range = vim.NumericRange()
        vlan_range.start = 100
        vlan_range.end = 200
        vlan_trunk_spec.vlanId = [vlan_range]
        vlan_trunk_spec.inherited = False
        # Assign VLAN trunk spec to default port config
        dvportgroup_spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
        dvportgroup_spec.defaultPortConfig.vlan = vlan_trunk_spec

    else:
        dvportgroup_spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
        dvportgroup_spec.defaultPortConfig.vlan = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
        dvportgroup_spec.defaultPortConfig.vlan.vlanId = 2307
        dvportgroup_spec.defaultPortConfig.vlan.inherited = False

    try:
        task = dvs.AddDVPortgroup_Task([dvportgroup_spec])
        return task
    except vmodl.MethodFault as error:
        print(f"Caught vmodl fault : {error.msg}")
    except Exception as e:
        print(f"Caught exception : {str(e)}")

def main():
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    service_instance, content = create_vsphere_connection(host=vCenter_host_ip, user=vCenter_user, password=vCenter_password)

    # dvs_name = dswitch_creator(content)
    datacenters=get_datacenter(content)
    datacenter_name = datacenters[0].name

    #TODO: datacenter'ın adını alıp, dvs oluşturulacak

    #create_dvs(content, "bkaan_dvs", datacenter_name)
    create_dvportgroup(content, "bkaan_dvs", "lllllllllkkkkkkkk")

    Disconnect(service_instance)

if __name__ == "__main__":
    main()

