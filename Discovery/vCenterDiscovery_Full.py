from Discovery.ipam_disck4 import check_ip_addres_with_hostname, Connect_IPAM, get_subnet
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import base64
import psycopg2
import pandas as pd
import sys
from sqlalchemy import create_engine
from datetime import datetime

def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def connect_esxi_environment(esxi_host, username, password):
    # Bağlantı yap
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE  # Sertifika doğrulamasını devre dışı bırak

    si = SmartConnect(host=esxi_host, user=username, pwd=password, port=443, sslContext=context)

    # Sanal makineleri al
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    return vms, si

def vm_summary_section(vm, vmID):
    summary_config = vars(vm.summary.config)
    for key, value in summary_config.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes="vm.summary.config")

    summary_guest = vars(vm.summary.guest)
    for key, value in summary_guest.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes="vm.summary.guest")

    summary_overallStatus = vars(vm.summary.overallStatus)
    for key, value in summary_overallStatus.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes="vm.summary.overallStatus")

    summary_quickStats = vars(vm.summary.quickStats)
    for key, value in summary_quickStats.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes="vm.summary.quickStats")

    summary_runtime = vars(vm.summary.runtime)
    for key, value in summary_runtime.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes="vm.summary.runtime")

    summary_storage = vars(vm.summary.storage)
    for key, value in summary_storage.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes="vm.summary.storage")

def datastore_section(vm, vmID):
    try:
        vmDatastore = vm.datastore
        for datastore in vmDatastore:
            try:
                datastoreAlarmActions = datastore.alarmActionsEnabled
                keyToInsert = "alarmActionsEnabled"
                append_dataframe_given_values(keyToInsert, datastoreAlarmActions, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                              "vm.datastore.datastoreAlarmActions")
            except:
                pass

            try:
                datastoreCapabilities = vars(datastore.capability)
                for key, value in datastoreCapabilities.items():
                    value = str(value)
                    keyToInsert = key
                    append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                  "vm.datastore.capability")
            except:
                pass

            try:
                datastoreConfigStatus = datastore.configStatus
                keyToInsert = "configStatus"
                append_dataframe_given_values(keyToInsert, datastoreConfigStatus, isDeletedValueForAppend, versionForAppend,
                                                createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                "vm.datastore.configStatus")
            except:
                pass

            try:
                declaredAlarmState = datastore.declaredAlarmState
                for alarm in declaredAlarmState:
                    alarmDesc = vars(alarm)
                    for key, value in alarmDesc.items():
                        value = str(value)
                        keyToInsert = key
                        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                      "vm.datastore.declaredAlarmState")
            except:
                pass

            #disabledMethod
            try:
                disabledMethod = datastore.disabledMethod
                for method in disabledMethod:
                    keyToInsert = "disabledMethod"
                    append_dataframe_given_values(keyToInsert, method, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                  "vm.datastore.disabledMethod")
            except:
                pass

            #effectiveRole
            try:
                effectiveRole = datastore.effectiveRole
                keyToInsert = "effectiveRole"
                append_dataframe_given_values(keyToInsert, effectiveRole, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                              "vm.datastore.effectiveRole")
            except:
                pass

            #host bilgisi
            try:
                all_host = datastore.host
                for host in all_host:
                    #key bilgisi


                    #mountInfo
                    try:
                        mountInfo = vars(host.mountInfo)
                        for key, value in mountInfo.items():
                            value = str(value)
                            keyToInsert = key
                            append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                          None,
                                                          "vm.datastore.host.mountInfo")
                    except:
                        pass


            except:
                pass

    except:
        pass


def vm_information_getter(vms):
    for vm in vms:
        try:
            vmID = str(vm.summary.vm).split(":")[1].replace("'","")

            vmID = int(vmID.split('-')[-1])

        except:
            vmID = None

        # Summary Section
        vm_summary_section(vm, vmID)

        #alarmactionenabled description
        try:
            vmAlarmActionEnabled = vm.alarmActionsEnabled
            keyToInsert = "alarmActionEnabled"
            append_dataframe_given_values(keyToInsert, vmAlarmActionEnabled, isDeletedValueForAppend, versionForAppend,
                                            createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                            "vm")
        except:
            pass


        #Capability Section
        capability = vars(vm.capability)
        for key, value in capability.items():
            value = str(value)
            keyToInsert = key
            append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          notes="vm.capability")

        #Config Section
        config = vars(vm.config)
        for key, value in config.items():
            value = str(value)
            keyToInsert = key
            append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          notes="vm.config")

        #Config Status
        vmConfigStatus = vm.configStatus
        keyToInsert = "configStatus"
        append_dataframe_given_values(keyToInsert, vmConfigStatus, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          notes="vm.configStatus")

        #Datastore Section
        datastore_section(vm, vmID)



        try:
            vmPowerState = vm.runtime.powerState
            keyToInsert = "powerState"
            append_dataframe_given_values(keyToInsert, vmPowerState, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmPowerState)
        except:
            pass
        try:
            vmCreateDate = vm.summary.runtime.bootTime
            keyToInsert = "vmCreateDate"
            append_dataframe_given_values(keyToInsert, vmCreateDate, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmCreateDate)
        except:
            pass
        try:
            vmCPUNumber = vm.summary.config.numCpu
            keyToInsert = "cpu"
            append_dataframe_given_values(keyToInsert, vmCPUNumber, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmCPUNumber)
        except:
            pass
        try:
            vmRamValue = vm.summary.config.memorySizeMB
            keyToInsert = "memory"
            append_dataframe_given_values(keyToInsert, vmRamValue, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmRamValue)
        except:
            pass
        try:
            vmOsInfo = vm.summary.config.guestFullName
            keyToInsert = "ostype"
            append_dataframe_given_values(keyToInsert, vmOsInfo, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmOsInfo)
        except:
            pass

        #datastore
        try:
            vmDatastore = vm.datastore[0].info.name
            keyToInsert = "datastore"
            append_dataframe_given_values(keyToInsert, vmDatastore, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmDatastore)
        except:
            pass

        #cluster name
        try:
            vmClusterName = vm.resourcePool.name
            keyToInsert = "clusterName"
            append_dataframe_given_values(keyToInsert, vmClusterName, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          vmClusterName)
        except:
            pass

        # hostname
        try:
            vmHostName = vm.summary.guest.hostName
            keyToInsert = "hostname"
            append_dataframe_given_values(keyToInsert, vmHostName, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                          None,
                                          vmHostName)

            ipam = Connect_IPAM()
            ipam_return = check_ip_addres_with_hostname(IPAM=ipam, hostname=vmHostName)

            if ipam_return is None:
                continue

            else:
                ipam_ip = ipam_return[0]
                keyToInsert = "ipam_ip"
                append_dataframe_given_values(keyToInsert, ipam_ip, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                              None,
                                              ipam_ip)

                ipam_subnet = ipam_return[1]
                keyToInsert = "ipam_subnet_id"
                append_dataframe_given_values(keyToInsert, ipam_subnet, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                              None,
                                              ipam_subnet)

                subnet_info = get_subnet(IPAM=ipam, subnet_id=ipam_subnet)

                if subnet_info is not None:
                    subnet_ip = subnet_info[0]
                    subnet_mask = subnet_info[1]

                    keyToInsert = "subnet_ip"
                    append_dataframe_given_values(keyToInsert, subnet_ip, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType,
                                                  esxi_host, None,
                                                  subnet_ip)

                    keyToInsert = "subnet_mask"
                    append_dataframe_given_values(keyToInsert, subnet_mask, isDeletedValueForAppend,
                                                  versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType,
                                                  esxi_host, None,
                                                  subnet_mask)
        except:
            pass




        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                try:
                    vmDiskName = device.deviceInfo.label
                    keyToInsert = "diskname"
                    append_dataframe_given_values(keyToInsert, vmDiskName, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                  None,
                                                  vmDiskName)
                except:
                    pass
                try:
                    vmDiskCapacity = device.capacityInKB / 1024 / 1024
                    keyToInsert = "diskSize"
                    append_dataframe_given_values(keyToInsert, vmDiskCapacity, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                  None,
                                                  vmDiskCapacity)
                except:
                    pass
                try:
                    vmDiskType = device.backing.diskMode
                    keyToInsert = "diskType"
                    append_dataframe_given_values(keyToInsert, vmDiskType, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                  None,
                                                  vmDiskType)
                except:
                    pass

                #total virtualdisk number of vm
                try:
                    vmDiskNumber = len(vm.config.hardware.device)
                    keyToInsert = "diskNumber"
                    append_dataframe_given_values(keyToInsert, vmDiskNumber, isDeletedValueForAppend, versionForAppend,
                                                    createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                    None,
                                                    vmDiskNumber)
                except:
                    pass



        if (vm.snapshot is None):
            pass
        else:
            for snapshot in vm.snapshot.rootSnapshotList:
                try:
                    vmSnapShotName = snapshot.name
                    keyToInsert = "snapshotName"
                    append_dataframe_given_values(keyToInsert, vmSnapShotName, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                  None,
                                                  vmSnapShotName)
                except:
                    pass
                try:
                    vmSnapShotCreationTime = snapshot.createTime
                    keyToInsert = "snapshotCreateDate"
                    append_dataframe_given_values(keyToInsert, vmSnapShotCreationTime, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                  None,
                                                  vmSnapShotCreationTime)
                except:
                    pass



if __name__ == "__main__":
    createdDateForAppend = datetime.now()
    versionForAppend = 1
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "vCenter"
    esxi_host = "10.14.45.10"
    username = "administrator@vsphere.local"
    password = "Aa112233!"
    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")

    def Convert(string):
        li = list(string.replace(' ', '').split(","))
        return li

    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()
    vmIdList = Convert(mystring)
    vmsFromESXI, si = connect_esxi_environment(esxi_host, username, password)
    vm_information_getter(vmsFromESXI)
    Disconnect(si)
    dataFrameForInsert.to_sql("vcenter_disc", engineForPostgres, chunksize=5000, index=False, method=None,
                              if_exists='append')