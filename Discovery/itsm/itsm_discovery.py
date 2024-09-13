from datetime import datetime
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, DateTime, MetaData, inspect, Boolean, Integer
from Discovery import Credentials
from Discovery.itsm.utils_itsm import *
from sqlalchemy.orm import declarative_base



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
    all_requests = get_all_requests()
    if all_requests:
        for request in all_requests:
            flattened_request = flatten_dict(request)
            request_id = int(flattened_request['id'])
            for key, value in flattened_request.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/requests", f"{base_url}/requests")


def call_get_request_full_details():
    request_info = get_info_by_request_id(258497)
    if request_info:
        flattened_request_info = flatten_dict(request_info)
        request_id = int(flattened_request_info['id'])
        for key, value in flattened_request_info.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/requests/{id}", f"{base_url}/requests/{request_id}")
    else:
        print("No data found")

def call_get_request_summary():
    request_id = 258497
    request_summary = get_request_summary_by_id(request_id)
    if request_summary:
        flattened_request_summary = flatten_dict(request_summary)
        for key, value in flattened_request_summary.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/requests/{id}/summary", f"{base_url}/requests/{request_id}/summary")
    else:
        print("No data found")

def call_get_request_notes_by_id():
    request_id = 258497
    request_notes = get_request_notes_by_id(request_id)
    if request_notes:
        flattened_request_notes = flatten_dict(request_notes)
        for key, value in flattened_request_notes.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/requests/{id}/notes", f"{base_url}/requests/{request_id}/notes")
    else:
        print("No data found")

def call_get_request_approval_levels_by_id():
    request_id = 258497
    approval_level_info = get_request_approval_levels_by_id(request_id)
    if approval_level_info:
        flattened_approval_level_info = flatten_dict(approval_level_info)
        for key, value in flattened_approval_level_info.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/requests/{id}/approval_level", f"{base_url}/requests/{request_id}/approval_levels")
    else:
        print("No data found")

def call_get_request_worklogs_by_id():
    request_id = 258497
    worklog_info = get_request_worklogs_by_id(request_id)
    if worklog_info:
        flattened_worklog_info = flatten_dict(worklog_info)
        for key, value in flattened_worklog_info.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, request_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/requests/{id}/worklogs", f"{base_url}/requests/{request_id}/worklogs")
    else:
        print("No data found")

def call_get_list_promlebs():
    promlems = get_list_promlebs()
    if promlems is not None:
        for problem in promlems:
            flattened_problem = flatten_dict(problem)
            for key, value in flattened_problem.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/promlebs", f"{base_url}/promlebs")
    else:
        print("No data found")

def call_get_list_promlem_notes():
    promlems_id = 60
    problem_notes = get_list_promlem_notes(promlems_id)
    if problem_notes:
        flattened_problem_notes = flatten_dict(problem_notes)
        for key, value in flattened_problem_notes.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, promlems_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/promlebs/{id}/notes", f"{base_url}/promlebs/{promlems_id}/notes")
    else:
        print("No data found")

def call_get_list_problem_worklogs():
    promlems_id = 60
    problem_worklogs = get_list_problem_worklogs(promlems_id)
    if problem_worklogs:
        flattened_problem_worklogs = flatten_dict(problem_worklogs)
        for key, value in flattened_problem_worklogs.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, promlems_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/promlebs/{id}/worklogs", f"{base_url}/promlebs/{promlems_id}/worklogs")
    else:
        print("No data found")

def call_get_list_changes():
    changes = get_list_changes()
    if get_list_changes():
        for change in changes:
            flattened_change = flatten_dict(change)
            for key, value in flattened_change.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/changes", f"{base_url}/changes")
    else:
        print("No data found")

def call_get_change_by_id():
    change_id = 2317
    change_info = get_changes_by_id(change_id)
    if change_info:
        flattened_change_info = flatten_dict(change_info)
        for key, value in flattened_change_info.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, change_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/changes/{id}", f"{base_url}/changes/{change_id}")
    else:
        print("No data found")
        pass

def call_get_list_projects():
    projects = get_list_projects()
    if projects:
        for project in projects:
            flattened_project = flatten_dict(project)
            for key, value in flattened_project.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/projects", f"{base_url}/projects")
    else:
        print("No data found")

def call_get_project_by_id():
    project_id = 32
    project_info = get_project_by_id(project_id)
    if project_info:
        flattened_project_info = flatten_dict(project_info)
        for key, value in flattened_project_info.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/projects/{id}", f"{base_url}/projects/{project_id}")
    else:
        print("No data found")

def call_get_list_project_comments():
    project_id = 32
    comments = get_list_project_comments(project_id)
    if comments:
        for comment in comments:
            flattened_comment = flatten_dict(comment)
            for key, value in flattened_comment.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/projects/{id}/comments", f"{base_url}/projects/{project_id}/comments")
    else:
        print("No data found")

def call_get_list_project_milestones():
    project_id = 32
    milestones = get_list_project_milestones(project_id)
    if milestones:
        for milestone in milestones:
            flattened_milestone = flatten_dict(milestone)
            for key, value in flattened_milestone.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/projects/{id}/milestones", f"{base_url}/projects/{project_id}/milestones")
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
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, project_id, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/projects/{id}/milestones/{milestone_id}/comments", f"{base_url}/projects/{project_id}/milestones/{milestone_id}/comments")
    else:
        print("No data found")

def call_get_list_aseests():
    assets = get_list_aseests()
    if assets:
        for asset in assets:
            flattened_asset = flatten_dict(asset)
            for key, value in flattened_asset.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/assets", f"{base_url}/assets")
    else:
        print("No data found")

def call_get_list_workstations():
    workstations = get_list_workstations()
    if workstations:
        for workstation in workstations:
            flattened_workstation = flatten_dict(workstation)
            for key, value in flattened_workstation.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/workstations", f"{base_url}/workstations")
    else:
        print("No data found")

def call_get_list_solutions():
    solutions = get_list_solutions()
    if solutions:
        for solution in solutions:
            flattened_solution = flatten_dict(solution)
            for key, value in flattened_solution.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/solutions", f"{base_url}/solutions")
    else:
        print("No data found")

def call_get_all_sites():
    sites = get_all_sites()
    if sites:
        for site in sites:
            flattened_site = flatten_dict(site)
            site_id = int(flattened_site['id'])
            for key, value in flattened_site.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, int(site_id), virtualizationEnvironmentType, virtualizationEnvironmentIp, "/sites", f"{base_url}/sites")
    #     sites_data = [
    #         {
    #             **flatten_dict(site),
    #             "environment_ip": None,
    #             "environment_type": "ITSM",
    #             "endpoint_name": "/sites",
    #             "notes": None
    #         }
    #         for site in sites
    #     ]
    #
    #     #Table Config
    #     TABLE_NAME = "kr_discovery_itsm_sites"
    #     metadata = MetaData()
    #     inspector = inspect(engineForPostgres)
    #     if not inspector.has_table(TABLE_NAME):
    #         itsm_site = Table(
    #             TABLE_NAME, metadata,
    #             Column("email_id", String),
    #             Column("country", String),
    #             Column("created_time_display_value", String),
    #             Column("created_time_value", String),
    #             Column("city", String),
    #             Column("timezone", String),
    #             Column("timezone_name", String),
    #             Column("timezone_id", String),
    #             Column("description", String),
    #             Column("deleted", Boolean),
    #             Column("web_url", String),
    #             Column("street", String),
    #             Column("name", String),
    #             Column("door_no", String),
    #             Column("id", Integer),  # site_id olarak tanımladık
    #             Column("state", String),
    #             Column("landline", String),
    #             Column("region", String),
    #             Column("region_name", String),
    #             Column("region_id", String),
    #             Column("landmark", String),
    #             Column("postal_code", String),
    #             Column("fax", String),
    #             Column("environment_ip", String),
    #             Column("environment_type", String),
    #             Column("endpoint_name", String),
    #             Column("notes", String)
    #         )
    #
    #         # Veritabanında tabloyu oluşturma
    #         metadata.create_all(engineForPostgres)
    #         print(f"Table {TABLE_NAME} created successfully.")
    #     else:
    #         print(f"Table {TABLE_NAME} already exists. Data will be inserted. \n")
    #
    #     dataFrameForInsertSites = pd.DataFrame(sites_data)
    #
    #     column_order = [
    #         "email_id", "country", "created_time_display_value", "created_time_value", "city",
    #         "timezone", "timezone_name", "timezone_id", "description", "deleted", "web_url", "street",
    #         "name", "door_no", "id", "state", "landline", "region", "region_name", "region_id",
    #         "landmark", "postal_code", "fax", "environment_ip", "environment_type", "endpoint_name", "notes"
    #     ]
    #
    #     dataFrameForInsertSites = dataFrameForInsertSites[column_order]
    #
    #     dataFrameForInsertSites.to_sql("kr_discovery_itsm_sites", engineForPostgres, chunksize=5000, index=False, if_exists='replace')
    # else:
    #     print("No data found")

def call_get_all_tasks():
    tasks = get_all_tasks()
    if tasks:
        for task in tasks:
            flattened_task = flatten_dict(task)
            for key, value in flattened_task.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/tasks", f"{base_url}/tasks")
    else:
        print("No data found")

def call_get_all_contracts():
    contracts = get_all_contracts()
    if contracts:
        for contract in contracts:
            flattened_contract = flatten_dict(contract)
            for key, value in flattened_contract.items():
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, 0, virtualizationEnvironmentType, virtualizationEnvironmentIp, "/contracts", f"{base_url}/contracts")
    else:
        print("No data found")

def controller_method(engineForPostgres):
    # call_all_requests()
    # print("call_all_requests tamamlandı")
    # call_get_request_full_details()
    # print("call_get_request_full_details tamamlandı")
    # call_get_request_summary()
    # print("call_get_request_summary tamamlandı")
    # call_get_request_notes_by_id()
    # print("call_get_request_notes_by_id tamamlandı")
    # call_get_request_approval_levels_by_id()
    # print("call_get_request_approval_levels_by_id tamamlandı")
    # call_get_request_worklogs_by_id()
    # print("call_get_request_worklogs_by_id tamamlandı")
    # call_get_list_promlebs()
    # print("call_get_list_promlebs tamamlandı")
    # call_get_list_promlem_notes()
    # print("call_get_list_promlem_notes tamamlandı")
    # call_get_list_problem_worklogs()
    # print("call_get_list_problem_worklogs tamamlandı")
    # call_get_list_changes()
    # print("call_get_list_changes tamamlandı")
    # call_get_list_projects()
    # print("call_get_list_projects tamamlandı")
    # call_get_project_by_id()
    # print("call_get_project_by_id tamamlandı")
    # call_get_list_project_comments()
    # print("call_get_list_project_comments tamamlandı")
    # call_get_list_project_milestones()
    # print("call_get_list_project_milestones tamamlandı")
    # call_get_list_project_milestone_comments()
    # print("call_get_list_project_milestone_comments tamamlandı")
    # call_get_list_aseests()
    # print("call_get_list_aseests tamamlandı")
    # call_get_list_workstations()
    # print("call_get_list_workstations tamamlandı")
    # call_get_list_solutions()
    # print("call_get_list_solutions tamamlandı")
    #
    call_get_all_sites()
    print("call_get_all_sites tamamlandı")
    # call_get_all_tasks()
    # print("call_get_all_tasks tamamlandı")
    # call_get_all_contracts()
    # print("call_get_all_contracts tamamlandı")

def create_datastore_table_if_not_exists(engine, table_name: str):
    metadata = MetaData()
    datastore_table = Table(
        table_name, metadata,
        Column('key', String),
        Column('value', String),
        Column('is_deleted', Boolean),
        Column('version', Integer),
        Column('created_date', DateTime),
        Column('vm_id', Integer),
        Column('virtualization_environment_type', String),
        Column('virtualization_environment_ip', String),
        Column('node', String),
        Column('notes', String)
    )
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        metadata.create_all(engine)
        print(f"{table_name} ---> tablosu oluşturuldu.")
    else:
        print("")
        print(f"{table_name} ---> tablosu zaten var.")

if __name__ == "__main__":
    base_url, api_key = Credentials.itsm_live_credential()
    TABLE_NAME = "kr_discovery_itsm"

    createdDateForAppend = datetime.now()
    versionForAppend = 2
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "ITSM"
    virtualizationEnvironmentIp = "172.28.0.30"

    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')

    controller_method(engineForPostgres)

    #dataFrameForInsert.to_csv("itsm_disc.csv", index=False)

    create_datastore_table_if_not_exists(engineForPostgres, TABLE_NAME)
    dataFrameForInsert.to_sql(TABLE_NAME, engineForPostgres, chunksize=5000, index=False, method=None,if_exists='replace')
