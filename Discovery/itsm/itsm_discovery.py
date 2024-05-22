from datetime import datetime
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from Discovery import Credentials
from Discovery.itsm.utils_itsm import *


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def flatten_dict(d, parent_key='', sep='_'):
    # d boş listeyse boş dict döndür
    if not d:
        return {parent_key: ''}
    else:
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

def call_get_request_full_details():
    if get_info_by_request_id(258497) is not None:
        d = flatten_dict(get_info_by_request_id(258497))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, int(d['id']), virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}", f"{base_url}/requests/{d['id']}")

def call_get_request_summary():
    request_id = 258497
    if get_request_summary_by_id(request_id) is not None:
        d = flatten_dict(get_request_summary_by_id(request_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/summary", f"{base_url}/requests/{request_id}/summary")

def call_get_request_notes_by_id():
    request_id = 258497
    if get_request_notes_by_id(request_id) is not None:
        d = flatten_dict(get_request_notes_by_id(request_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/notes", f"{base_url}/requests/{request_id}/notes")

def call_get_request_approval_levels_by_id():
    request_id = 258497
    if get_request_approval_levels_by_id(request_id) is not None:
        d = flatten_dict(get_request_approval_levels_by_id(request_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/approval_level", f"{base_url}/requests/{request_id}/approval_levels")

def call_get_request_worklogs_by_id():
    request_id = 258497
    if get_request_worklogs_by_id(request_id) is not None:
        d = flatten_dict(get_request_worklogs_by_id(request_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/worklogs", f"{base_url}/requests/{request_id}/worklogs")
    else:
        print("No data found")
        pass

def call_get_list_promlebs():
    if get_list_promlebs() is not None:
        promlems = get_list_promlebs()
        for i in promlems:
            d = flatten_dict(i)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/promlebs", f"{base_url}/promlebs")
    else:
        print("No data found")
        pass

def call_get_list_promlem_notes():
    promlems_id = 60
    if get_list_promlem_notes(promlems_id) is not None:
        d = flatten_dict(get_list_promlem_notes(promlems_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, promlems_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/promlebs/{id}/notes", f"{base_url}/promlebs/{promlems_id}/notes")

def call_get_list_problem_worklogs():
    promlems_id = 60
    if get_list_problem_worklogs(promlems_id) is not None:
        d = flatten_dict(get_list_problem_worklogs(promlems_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, promlems_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/promlebs/{id}/worklogs", f"{base_url}/promlebs/{promlems_id}/worklogs")

def call_get_list_changes():
    if get_list_changes() is not None:
        changes = get_list_changes()
        for i in changes:
            d = flatten_dict(i)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/changes", f"{base_url}/changes")
    else:
        print("No data found")
        pass

def call_get_change_by_id():
    change_id = 2317
    if get_changes_by_id(change_id) is not None:
        d = flatten_dict(get_changes_by_id(change_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, change_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/changes/{id}", f"{base_url}/changes/{change_id}")
    else:
        print("No data found")
        pass

def call_get_list_projects():
    if get_list_projects() is not None:
        projects = get_list_projects()
        for i in projects:
            d = flatten_dict(i)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects", f"{base_url}/projects")
    else:
        print("No data found")
        pass

def call_get_project_by_id():
    project_id = 32
    if get_project_by_id(project_id) is not None:
        d = flatten_dict(get_project_by_id(project_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}", f"{base_url}/projects/{project_id}")
    else:
        print("No data found")
        pass

def call_get_list_project_comments():
    project_id = 32
    comments = get_list_project_comments(project_id)
    if comments is not None:
        for comment in comments:
            d = flatten_dict(comment)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}/comments", f"{base_url}/projects/{project_id}/comments")
    else:
        print("No data found")
        pass

def call_get_list_project_milestones():
    project_id = 32
    milestones = get_list_project_milestones(project_id)
    if milestones is not None:
        for milestone in milestones:
            d = flatten_dict(milestone)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}/milestones", f"{base_url}/projects/{project_id}/milestones")
    else:
        print("No data found")
        pass

def call_get_list_project_milestone_comments():
    project_id = 32
    milestone_id = 10
    comments = get_list_project_milestone_comments(project_id, milestone_id)
    if comments is not None:
        for comment in comments:
            d = flatten_dict(comment)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}/milestones/{milestone_id}/comments", f"{base_url}/projects/{project_id}/milestones/{milestone_id}/comments")
    else:
        print("No data found")
        pass

def call_get_list_aseests():
    if get_list_aseests() is not None:
        assets = get_list_aseests()
        for i in assets:
            d = flatten_dict(i)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/assets", f"{base_url}/assets")
    else:
        print("No data found")
        pass

def call_get_list_workstations():
    if get_list_workstations() is not None:
        workstations = get_list_workstations()
        for i in workstations:
            d = flatten_dict(i)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/workstations", f"{base_url}/workstations")
    else:
        print("No data found")
        pass

def call_get_list_solutions():
    if get_list_solutions() is not None:
        solutions = get_list_solutions()
        for i in solutions:
            d = flatten_dict(i)
            for key, value in d.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/solutions", f"{base_url}/solutions")
    else:
        print("No data found")
        pass

def controller_method():
    call_all_requests()
    call_get_request_full_details()
    call_get_request_summary()
    call_get_request_notes_by_id()
    call_get_request_approval_levels_by_id()
    call_get_request_worklogs_by_id()
    call_get_list_promlebs()
    call_get_list_promlem_notes()
    call_get_list_problem_worklogs()
    call_get_list_changes()
    call_get_list_projects()
    call_get_project_by_id()
    call_get_list_project_comments()
    call_get_list_project_milestones()
    call_get_list_project_milestone_comments()
    call_get_list_aseests()
    call_get_list_workstations()
    call_get_list_solutions()

if __name__ == "__main__":
    base_url, api_key = Credentials.itsm_credential()
    createdDateForAppend = datetime.now()
    versionForAppend = 2
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "ITSM"
    virtualalizationEnvironmentIp = "172.28.0.30"

    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    # engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    #
    # connectionForPostgres = psycopg2.connect(
    #     host="10.14.45.69",
    #     port="7100",
    #     database="karcin_pfms",
    #     user="postgres",
    #     password="Cekino.123!")
    # cursorForPostgres = connectionForPostgres.cursor()

    controller_method()

    dataFrameForInsert.to_csv("itsm_disc.csv", index=False)

    #dataFrameForInsert.to_sql("itsm_disc", engineForPostgres, chunksize=5000, index=False, method=None,if_exists='append')
