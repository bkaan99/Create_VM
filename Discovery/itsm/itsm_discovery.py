from datetime import datetime
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from Discovery import Credentials
from Discovery.itsm.utils_itsm import *


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[str(key),str(value), is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def flatten_dict(d, parent_key='', sep='_'):
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
    all_requests = get_all_requests(numberOfData=100)
    if all_requests:
        for request in all_requests:
            flattened_request = flatten_dict(request)
            request_id = int(flattened_request['id'])
            for key, value in flattened_request.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests", f"{base_url}/requests")

def call_get_request_full_details():
    request_info = get_info_by_request_id(258497)
    if request_info:
        flattened_request_info = flatten_dict(request_info)
        request_id = int(flattened_request_info['id'])
        for key, value in flattened_request_info.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}", f"{base_url}/requests/{request_id}")
    else:
        print("No data found")

def call_get_request_summary():
    request_id = 258497
    request_summary = get_request_summary_by_id(request_id)
    if request_summary:
        flattened_request_summary = flatten_dict(request_summary)
        for key, value in flattened_request_summary.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/summary", f"{base_url}/requests/{request_id}/summary")
    else:
        print("No data found")

def call_get_request_notes_by_id():
    request_id = 258497
    request_notes = get_request_notes_by_id(request_id)
    if request_notes:
        flattened_request_notes = flatten_dict(request_notes)
        for key, value in flattened_request_notes.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/notes", f"{base_url}/requests/{request_id}/notes")
    else:
        print("No data found")

def call_get_request_approval_levels_by_id():
    request_id = 258497
    if get_request_approval_levels_by_id(request_id) is not None:
        d = flatten_dict(get_request_approval_levels_by_id(request_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/approval_level", f"{base_url}/requests/{request_id}/approval_levels")
    else:
        print("No data found")

def call_get_request_worklogs_by_id():
    request_id = 258497
    if get_request_worklogs_by_id(request_id):
        d = flatten_dict(get_request_worklogs_by_id(request_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/requests/{id}/worklogs", f"{base_url}/requests/{request_id}/worklogs")
    else:
        print("No data found")

def call_get_list_promlebs():
    promlems = get_list_promlebs()
    if promlems:
        for problem in promlems:
            flattened_problem = flatten_dict(problem)
            for key, value in flattened_problem.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/promlebs", f"{base_url}/promlebs")
    else:
        print("No data found")

def call_get_list_promlem_notes():
    promlems_id = 60
    if get_list_promlem_notes(promlems_id):
        d = flatten_dict(get_list_promlem_notes(promlems_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, promlems_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/promlebs/{id}/notes", f"{base_url}/promlebs/{promlems_id}/notes")
    else:
        print("No data found")

def call_get_list_problem_worklogs():
    promlems_id = 60
    if get_list_problem_worklogs(promlems_id):
        d = flatten_dict(get_list_problem_worklogs(promlems_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, promlems_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/promlebs/{id}/worklogs", f"{base_url}/promlebs/{promlems_id}/worklogs")
    else:
        print("No data found")

def call_get_list_changes():
    changes = get_list_changes()
    if get_list_changes():
        for change in changes:
            flattened_change = flatten_dict(change)
            for key, value in flattened_change.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/changes", f"{base_url}/changes")
    else:
        print("No data found")

def call_get_change_by_id():
    change_id = 2317
    if get_changes_by_id(change_id):
        d = flatten_dict(get_changes_by_id(change_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, change_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/changes/{id}", f"{base_url}/changes/{change_id}")
    else:
        print("No data found")
        pass

def call_get_list_projects():
    projects = get_list_projects()
    if projects:
        for project in projects:
            flattened_project = flatten_dict(project)
            for key, value in flattened_project.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects", f"{base_url}/projects")
    else:
        print("No data found")

def call_get_project_by_id():
    project_id = 32
    if get_project_by_id(project_id):
        d = flatten_dict(get_project_by_id(project_id))
        for key, value in d.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}", f"{base_url}/projects/{project_id}")
    else:
        print("No data found")

def call_get_list_project_comments():
    project_id = 32
    comments = get_list_project_comments(project_id)
    if comments:
        for comment in comments:
            flattened_comment = flatten_dict(comment)
            for key, value in flattened_comment.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}/comments", f"{base_url}/projects/{project_id}/comments")
    else:
        print("No data found")

def call_get_list_project_milestones():
    project_id = 32
    milestones = get_list_project_milestones(project_id)
    if milestones:
        for milestone in milestones:
            flattened_milestone = flatten_dict(milestone)
            for key, value in flattened_milestone.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}/milestones", f"{base_url}/projects/{project_id}/milestones")
    else:
        print("No data found")

def call_get_list_project_milestone_comments():
    project_id = 32
    milestone_id = 10
    comments = get_list_project_milestone_comments(project_id, milestone_id)
    if comments:
        for comment in comments:
            flattened_comment = flatten_dict(comment)
            for key, value in flattened_comment.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/projects/{id}/milestones/{milestone_id}/comments", f"{base_url}/projects/{project_id}/milestones/{milestone_id}/comments")
    else:
        print("No data found")

def call_get_list_aseests():
    assets = get_list_aseests()
    if get_list_aseests():
        for asset in assets:
            flattened_asset = flatten_dict(asset)
            for key, value in flattened_asset.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/assets", f"{base_url}/assets")
    else:
        print("No data found")

def call_get_list_workstations():
    workstations = get_list_workstations()
    if workstations:
        for workstation in workstations:
            flattened_workstation = flatten_dict(workstation)
            for key, value in flattened_workstation.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/workstations", f"{base_url}/workstations")
    else:
        print("No data found")

def call_get_list_solutions():
    solutions = get_list_solutions()
    if solutions:
        for solution in solutions:
            flattened_solution = flatten_dict(solution)
            for key, value in flattened_solution.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "/solutions", f"{base_url}/solutions")
    else:
        print("No data found")

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
