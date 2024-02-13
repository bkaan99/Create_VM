import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def connect_Postgres():
    try:
        engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
        connectionForPostgres = psycopg2.connect(
            host="10.14.45.69",
            port="7100",
            database="karcin_pfms",
            user="postgres",
            password="Cekino.123!")
        cursorForPostgres = connectionForPostgres.cursor()

        return connectionForPostgres

    except psycopg2.OperationalError as e:
        print(f"Operasyon Hatası: {e}")
    except psycopg2.InterfaceError as e:
        print(f"Arayüz Hatası: {e}")
    except psycopg2.DatabaseError as e:
        print(f"Veritabanı Hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

    return None

def get_vmList_Config(vmid):

    connectionForPostgres = connect_Postgres()
    VmListConfigrurationTable = pd.read_sql_query("select * from kr_vm_list where id=" + str(vmid),
                                                  connectionForPostgres)

    vmListConfig_Id = VmListConfigrurationTable.get("id")[0]
    vmListConfig_Cpu = VmListConfigrurationTable.get("cpu")[0]
    vmListConfig_RamSize = VmListConfigrurationTable.get("ramsizegb")[0]
    vmListConfig_VmName = VmListConfigrurationTable.get("vmname")[0]
    vmListConfig_HostName = VmListConfigrurationTable.get("hostname")[0]
    vmListConfig_IpAdress = VmListConfigrurationTable.get("ipaddress")[0]
    vmListConfig_Environment = VmListConfigrurationTable.get("environment")[0]
    vmListConfig_OperatingSystemInformation = VmListConfigrurationTable.get("operatingsysteminformation")[0]
    vmListConfig_OperatingSystemVersion = VmListConfigrurationTable.get("operatingsystemversion")[0]
    vmListConfig_InternetConnection = VmListConfigrurationTable.get("internetconnection")[0]
    vmListConfig_VirtualizationTechnology = VmListConfigrurationTable.get("virtualizationtechnology")[0]
    vmListConfig_PFMSConfigurationId = VmListConfigrurationTable.get("pfmsconfiguration_id")[0]

    pfmsConfigType = pd.read_sql_query(
        "select configtype from kr_pfms_configuration where id=" + str(vmListConfig_PFMSConfigurationId),
        connectionForPostgres).get("configtype")[0]

    return vmListConfig_Id, vmListConfig_Cpu, vmListConfig_RamSize, vmListConfig_VmName, vmListConfig_HostName, vmListConfig_IpAdress, vmListConfig_Environment, vmListConfig_OperatingSystemInformation, vmListConfig_OperatingSystemVersion, vmListConfig_InternetConnection, vmListConfig_VirtualizationTechnology, vmListConfig_PFMSConfigurationId, pfmsConfigType

def get_first_disik_Config(vmid):
    connectionForPostgres = connect_Postgres()
    VmFirstDiskConfigurationTable = pd.read_sql_query("select * from kr_vm_first_disk where vmlist_id=" + str(vmid) +" and is_deleted=false ORDER BY id",
                                                      connectionForPostgres)

    #vmFirstDiskConfig_Id = list(VmFirstDiskConfigurationTable.id)
    # vmFirstDiskConfig_ControllerLocation = VmFirstDiskConfigurationTable.get("controllerlocation")[0]
    # vmFirstDiskConfig_ControllerLocationValue = VmFirstDiskConfigurationTable.get("controllerlocationvalue")[0]
    #vmFirstDiskConfig_CreateDate = list(VmFirstDiskConfigurationTable.createdate)
    # vmFirstDiskConfig_isDeleted = VmFirstDiskConfigurationTable.get("isdeleted")[0]
    # vmFirstDiskConfig_DiskByte = VmFirstDiskConfigurationTable.get("diskbyte")[0]
    # vmFirstDiskConfig_DiskMod = VmFirstDiskConfigurationTable.get("diskmod")[0] if "diskmod" in VmFirstDiskConfigurationTable else None
    #vmFirstDiskConfig_DiskProvisioning = VmFirstDiskConfigurationTable.get("diskprovisioning")[0]
    vmFirstDiskConfig_DiskSize = list(VmFirstDiskConfigurationTable.disksize)
    #vmFirstDiskConfig_LimitOps = VmFirstDiskConfigurationTable.get("limitops")[0] if "limitops" in VmFirstDiskConfigurationTable else None
    # vmFirstDiskConfig_VmDiskImagePath = VmFirstDiskConfigurationTable.get("location")[0]
    # vmFirstDiskConfig_Shared = VmFirstDiskConfigurationTable.get("shared")[0]
    # vmFirstDiskConfig_SharedValue = VmFirstDiskConfigurationTable.get("sharedvalue")[0]
    # vmFirstDiskConfig_Sharing = VmFirstDiskConfigurationTable.get("sharing")[0]
    # vmFirstDiskConfig_Version = VmFirstDiskConfigurationTable.get("version")[0]
    #vmFirstDiskConfig_VmListId = VmFirstDiskConfigurationTable.get("vmlist_id")[0]

    return vmFirstDiskConfig_DiskSize
