from datetime import datetime
from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
from vCenter.IaaS.Connections.db_connection import *
from pyVmomi import vim
import pandas as pd
from sqlalchemy import create_engine

def get_datastores(content):
    datastore_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)
    datastores = datastore_view.view
    return datastores


def print_datastore_info(datastores):
    datastore_list = []
    for datastore in datastores:
        createdDateForAppend = datetime.now()
        datastore_info = {
            "Datastore Name": datastore.name,
            "Datastore URL": datastore.summary.url,
            "Capacity (GB)": round(datastore.summary.capacity / (1024 ** 3), 2),
            "Used Space": round((datastore.summary.capacity - datastore.summary.freeSpace) / (1024 ** 3), 2),
            "Free Space": round(datastore.summary.freeSpace / (1024 ** 3), 2),
            "Datastore Type": "VMFS" if datastore.summary.type == "VMFS" else "NFS",
            "Created Date": createdDateForAppend
        }
        datastore_list.append(datastore_info)

    return datastore_list

def connect_Postgres():
    try:
        connectionForPostgres = create_engine('postgresql://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
        return connectionForPostgres

    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

    return None

def insert_datastore_info_with_pandas(datastore_list):
    try:
        # DataFrame oluştur
        df = pd.DataFrame(datastore_list)
        # kolon isimlerini düzenle
        df.columns = ['datastore_name', 'datastore_url', 'capacity_gb', 'used_space_gb', 'free_space_gb', 'datastore_type', 'check_time']

        # Veritabanı bağlantısı oluştur
        engine = connect_Postgres()

        # DataFrame'i PostgreSQL veritabanına yaz
        df.to_sql('datastore_info', engine, if_exists='append', index=False, chunksize=5000, method=None,)

        print("Veri deposu bilgileri başarıyla eklendi.")

    except Exception as error:
        print("Hata oluştu:", error)


def main():
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    print("Datastore Information:")
    datastores = get_datastores(content)
    datastore_info = print_datastore_info(datastores)

    insert_datastore_info_with_pandas(datastore_info)

    Disconnect(service_instance)

    datetime.now()


if __name__ == "__main__":
    main()
