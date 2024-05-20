from datetime import datetime
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from Discovery import Credentials
from Discovery.itsm.general_itsm import get_all_requests, get_info_by_request_id


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def call_all_requests():
    r= get_all_requests(numberOfData=100)
    for i in r:
        for j in i:
            d = flatten_dict(j)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, int(d['id']), virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests", f"{base_url}/requests")

def get_request_full_details():
    get_info_by_request_id(258497)

def controller_method():
    call_all_requests()
    #get_request_full_details()

if __name__ == "__main__":
    base_url, api_key = Credentials.itsm_credential()
    createdDateForAppend = datetime.now()
    versionForAppend = 2
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "ITSM"
    virtualalizationEnvironmentIp = "172.28.0.30"

    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')

    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()

    controller_method()

    dataFrameForInsert.to_csv("itsm_disc.csv", index=False)

    #dataFrameForInsert.to_sql("itsm_disc", engineForPostgres, chunksize=5000, index=False, method=None,if_exists='append')
