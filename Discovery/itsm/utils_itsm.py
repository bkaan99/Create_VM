import json
import math
from typing import Union

import requests
from urllib.error import HTTPError
from Discovery import Credentials

def get_response(endpoint : str ='', params=None) -> requests.Response:
    base_url, api_key = Credentials.itsm_credential()
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authtoken': api_key
    }
    response = requests.get(url, headers=headers, params={"input_data": params} if params else None)
    try:
        response.raise_for_status()  # HTTPError varsa bir exception fırlatır
        return response
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        raise
    except Exception as err:
        print(f"Other error occurred: {err}")
        raise

def make_request_and_handle_errors(endpoint: str, params: dict) -> dict:
    try:
        response = get_response(endpoint=endpoint, params=json.dumps(params))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Hata oluştu: {e}")

def get_all_requests(startIndex : int =0 , numberOfData : int = 200) -> list:
    batchSize = 100
    print("Tüm talepler alınıyor...")
    total_batches = math.ceil(numberOfData / batchSize)

    all_requests = []

    for i in range(0, total_batches):
        try:
            input_data = {
                "list_info": {
                    "row_count": batchSize,
                    "start_index": startIndex,
                    "sort_field": "due_by_time",
                    "sort_order": "desc",
                    "get_total_count": True
                }
            }

            data = make_request_and_handle_errors('/requests', params=input_data)

            if data:
                all_requests.extend(data.get('requests', []))
                for request in data.get('requests', []):
                    print(request)
            else:
                break

            startIndex += batchSize

        except HTTPError as e:
            print(f"HTTP hatası: {e}")
            break

        except Exception as e:
            print(f"Beklenmedik hata: {e}")
            break

    return all_requests

def get_all_request_ids(startIndex: int =0) -> list:
    numberOfData = 200
    batchSize = 100
    requests_ids = []

    print("Tüm talep id'leri başarıyla alındı:")

    total_batches = math.ceil(numberOfData / batchSize)

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batchSize,
                "start_index": startIndex,
                "sort_field": "due_by_time",
                "sort_order": "desc",
                "get_total_count": True
            }
        }

        data = make_request_and_handle_errors('/requests', params=input_data)

        if data:
            for request in data.get('requests', []):
                request_id = request.get('id')
                if request_id:
                    print(request_id)
                    requests_ids.append(request_id)
        else:
            break

        startIndex += batchSize

        # Yüzdelik hesaplama
        completed_percentage = ((i + 1) / total_batches) * 100
        print(f"Tamamlanan: %{completed_percentage:.2f}")

    # with open('request_ids.json', 'w') as file:
    #     json.dump(requests_ids, file, indent=2)

    return requests_ids

def get_info_by_request_id(request_id: Union[str, int]='') -> dict:
    data = make_request_and_handle_errors(f'/requests/{request_id}', params={})
    if data:
        return data['request']
    else:
        return None

def get_request_summary_by_id(request_id: Union[str, int]='') -> dict:
    data = make_request_and_handle_errors(f'/requests/{request_id}/summary', params={})
    if data:
        for key in data['request_summary']:
            print(f"{key}: {data['request_summary'][key]}")
        return data['request_summary']
    else:
        print(f"Summary alınamadı. Hata kodu: {data['status_code']}")
        return None

def get_request_notes_by_id(request_id: Union[str, int]='') -> dict:
    data = make_request_and_handle_errors(f'/requests/{request_id}/notes', params={})
    if data:
        print("Notlar başarıyla alındı:")
        for note in data['notes']:
            print(note)
        return data['notes']
    else:
        print(f"Notlar alınamadı. Hata kodu: {data['status_code']}")
        return None

def get_request_approval_levels_by_id(request_id: Union[str, int]='') -> dict:
    data = make_request_and_handle_errors(f'/requests/{request_id}/approval_levels', params={})
    if data:
        print("Onay seviyeleri başarıyla alındı:")
        for level in data['approval_levels']:
            print(level)
        return data['approval_levels']
    else:
        print(f"Onay seviyeleri alınamadı. Hata kodu: {data['status_code']}")
        return None

def get_request_approval_by_id(request_id: Union[str, int]='', approval_level_id: Union[str, int] = '') -> dict:
    data = make_request_and_handle_errors(f'/requests/{request_id}/approval_levels/{approval_level_id}', params={})
    if data:
        print("Onay başarıyla alındı:")
        for approval in data['approvals']:
            print(approval)
        return data['approvals']
    else:
        print(f"Onay alınamadı. Hata kodu: {data['status_code']}")
        return None

def get_request_tasks_by_id(request_id: Union[str, int]='') -> dict:

    input_data = {
        "list_info": {
            "row_count": 100,
            "start_index": 0,
            "sort_field": "created_time",
            "sort_order": "desc",
        }
    }

    data = make_request_and_handle_errors(f'/requests/{request_id}/tasks', params=input_data)

    if data:
        print("Görevler başarıyla alındı:")
        for task in data['tasks']:
            print(task)
        return data['tasks']
    else:
        print(f"Görevler alınamadı. Hata kodu: {data['status_code']}")
        return None

def get_request_worklogs_by_id(request_id: Union[str, int]='') -> dict:
    data = make_request_and_handle_errors(f'/requests/{request_id}/worklogs', params={})
    if data:
        print("Çalışma günlükleri başarıyla alındı:")
        for worklog in data['worklogs']:
            print(worklog)
        return data['worklogs']
    else:
        print(f"Çalışma günlükleri alınamadı. Hata kodu: {data['status_code']}")
        return None

def get_list_promlebs(startIndex=0, numberOfData = None):

    if numberOfData is None:
        numberOfData = 200

    batchSize = 100
    print("Tüm talepler alınıyor...")
    total_batches = math.ceil(numberOfData / batchSize)
    all_problems = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batchSize,
                "start_index": startIndex,
                "sort_field": "due_by_time",
                "sort_order": "desc",
                "get_total_count": True
            }
        }
        input_data_str = json.dumps(input_data)

        response = get_response('/problems', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Problemler başarıyla alındı:")
            for problem in data['problems']:
                print(problem)
            all_problems.extend(data['problems'])
            startIndex += batchSize
        else:
            print(f"Problemler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())
            return None

    return all_problems
def get_list_promlem_notes(problem_id):
    response = get_response(f'/problems/{problem_id}/notes')
    if response.status_code == 200:
        data = response.json()
        print("Problemler başarıyla alındı:")
        for note in data['notes']:
            print(note)
        return data['notes']

    else:
        print(f"Problemler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None
def get_list_problem_tasks(problem_id):
    response = get_response(f'/problems/{problem_id}/tasks')
    if response.status_code == 200:
        data = response.json()
        print("Problemler başarıyla alındı:")
        for task in data['tasks']:
            print(task)
        return data['tasks']
    else:
        print(f"Problemler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_problem_worklogs(problem_id):
    response = get_response(f'/problems/{problem_id}/worklogs')
    if response.status_code == 200:
        data = response.json()
        print("Problemler başarıyla alındı:")
        for worklog in data['worklogs']:
            print(worklog)
        return data['worklogs']
    else:
        print(f"Problemler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_problem_task_worklogs(problem_id, task_id):
    response = get_response(f'/problems/{problem_id}/tasks/{task_id}/worklogs')
    if response.status_code == 200:
        data = response.json()
        print("Problemler başarıyla alındı:")
        for worklog in data['worklogs']:
            print(worklog)
        return data['worklogs']
    else:
        print(f"Problemler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_changes(startIndex=0, numberOfData = None):

    if numberOfData is None:
        numberOfData = 200

    batchSize = 100
    print("Tüm talepler alınıyor...")
    total_batches = math.ceil(numberOfData / batchSize)
    all_changes = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batchSize,
                "start_index": startIndex,
                "sort_order": "desc",
                "get_total_count": True
            }
        }
        input_data_str = json.dumps(input_data)

        response = get_response('/changes', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Değişiklikler başarıyla alındı:")
            for change in data['changes']:
                print(change)
            all_changes.extend(data['changes'])
            startIndex += batchSize
        else:
            print(f"Değişiklikler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())
            return None

    return all_changes

def get_changes_by_id(change_id: int):
    response = get_response(f'/changes/{change_id}')
    if response.status_code == 200:
        data = response.json()
        print("Değişiklik başarıyla alındı:")
        for key in data['change']:
            print(f"{key}: {data['change'][key]}")
        return data['change']
    else:
        print(f"Değişiklik alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_change_approval_levels(change_id: int):
    response = get_response(f'/changes/{change_id}/approval_levels')
    if response.status_code == 200:
        data = response.json()
        print("Onay seviyeleri başarıyla alındı:")
        for level in data['approval_levels']:
            print(level)
        return data['approval_levels']
    else:
        print(f"Onay seviyeleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_change_approval():
    response = get_response('/changes/{change_id}/approval_levels/{approval_level_id}/')
    if response.status_code == 200:
        data = response.json()
        print("Onay başarıyla alındı:")
        for approval in data['approvals']:
            print(approval)
        return data['approvals']
    else:
        print(f"Onay alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_change_notes(change_id: int):
    response = get_response(f'/changes/{change_id}/notes')
    if response.status_code == 200:
        data = response.json()
        print("Notlar başarıyla alındı:")
        for note in data['notes']:
            print(note)
        return data['notes']
    else:
        print(f"Notlar alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_changes_tasks(change_id: int):
    response = get_response(f'/changes/{change_id}/tasks')
    if response.status_code == 200:
        data = response.json()
        print("Görevler başarıyla alındı:")
        for task in data['tasks']:
            print(task)
        return data['tasks']
    else:
        print(f"Görevler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_change_worklogs(change_id: int):
    response = get_response(f'/changes/{change_id}/worklogs')
    if response.status_code == 200:
        data = response.json()
        print("Çalışma günlükleri başarıyla alındı:")
        for worklog in data['worklogs']:
            print(worklog)
        return data['worklogs']
    else:
        print(f"Çalışma günlükleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_change_task_worklogs(change_id: int, task_id: int):
    response = get_response(f'/changes/{change_id}/tasks/{task_id}/worklogs')
    if response.status_code == 200:
        data = response.json()
        print("Çalışma günlükleri başarıyla alındı:")
        for worklog in data['worklogs']:
            print(worklog)
        return data['worklogs']
    else:
        print(f"Çalışma günlükleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_projects():

    input_data = {
        "list_info": {
            "row_count": 100,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "desc",
            "get_total_count": True
        }
    }

    input_data_str = json.dumps(input_data)
    #FIXME: total count olayını normal haline getir.
    #total_count = get_response('/projects', params=input_data_str).json()['list_info']['total_count']
    total_count = 100
    batch_size = 100
    total_batches = math.ceil(total_count / batch_size)

    all_projects = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batch_size,
                "start_index": i * batch_size,
                "sort_field": "id",
                "sort_order": "asc",
                "get_total_count": True
            }
        }

        input_data_str = json.dumps(input_data)

        response = get_response('/projects', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Projeler başarıyla alındı:")
            for project in data['projects']:
                print(project)
                all_projects.append(project)
        else:
            print(f"Projeler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())

    return all_projects

def get_project_by_id(project_id):
    response = get_response(f'/projects/{project_id}')
    if response.status_code == 200:
        data = response.json()
        print("Proje başarıyla alındı:")
        for key in data['project']:
            print(f"{key}: {data['project'][key]}")
        return data['project']
    else:
        print(f"Proje alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_project_members(project_id):
    response = get_response(f'/projects/{project_id}/project_members')
    if response.status_code == 200:
        data = response.json()
        print("Proje üyeleri başarıyla alındı:")
        for member in data['members']:
            print(member)
        return data['members']
    else:
        print(f"Proje üyeleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_project_comments(project_id):
    response = get_response(f'/projects/{project_id}/comments')
    if response.status_code == 200:
        data = response.json()
        print("Proje yorumları başarıyla alındı:")
        for comment in data['comments']:
            print(comment)
        return data['comments']
    else:
        print(f"Proje yorumları alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_project_tasks(project_id):
    response = get_response(f'/projects/{project_id}/tasks')
    if response.status_code == 200:
        data = response.json()
        print("Proje görevleri başarıyla alındı:")
        for task in data['tasks']:
            print(task)
        return data['tasks']
    else:
        print(f"Proje görevleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_project_milestones(project_id):
    response = get_response(f'/projects/{project_id}/milestones')
    if response.status_code == 200:
        data = response.json()
        print("Proje kilometre taşları başarıyla alındı:")
        for milestone in data['milestones']:
            print(milestone)
        return data['milestones']
    else:
        print(f"Proje kilometre taşları alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_project_milestone_comments(project_id, milestone_id):
    response = get_response(f'/projects/{project_id}/milestones/{milestone_id}/comments')
    if response.status_code == 200:
        data = response.json()
        print("Proje kilometre taşı yorumları başarıyla alındı:")
        for comment in data['comments']:
            print(comment)
        return data['comments']
    else:
        print(f"Proje kilometre taşı yorumları alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_project_milestone_tasks(project_id, milestone_id):
    response = get_response(f'/projects/{project_id}/milestones/{milestone_id}/tasks')
    if response.status_code == 200:
        data = response.json()
        print("Proje kilometre taşı görevleri başarıyla alındı:")
        for task in data['tasks']:
            print(task)
        return data['tasks']
    else:
        print(f"Proje kilometre taşı görevleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_releases():
    response = get_response('/releases')
    if response.status_code == 200:
        data = response.json()
        print("Sürümler başarıyla alındı:")
        for release in data['releases']:
            print(release)
        return data['releases']
    else:
        print(f"Sürümler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())
        return None

def get_list_aseests():

    input_data = {
        "list_info": {
            "row_count": 100,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "desc",
            "get_total_count": True
        }
    }

    input_data_str = json.dumps(input_data)

    #FIXME: total count olayını normal haline getir.
    #total_count = get_response('/assets', params=input_data_str).json()['list_info']['total_count']
    total_count = 100
    batch_size = 100
    total_batches = math.ceil(total_count / batch_size)

    all_assets = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batch_size,
                "start_index": i * batch_size,
                "sort_field": "id",
                "sort_order": "asc",
                "get_total_count": True
            }
        }

        input_data_str = json.dumps(input_data)

        response = get_response('/assets', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Projeler başarıyla alındı:")
            for asset in data['assets']:
                print(asset)
                all_assets.append(asset)
        else:
            print(f"Projeler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())

    return all_assets

def get_list_workstations():
    input_data = {
        "list_info": {
            "row_count": 100,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "desc",
            "get_total_count": True
        }
    }

    input_data_str = json.dumps(input_data)
    #FIXME: total count olayını normal haline getir.
    #total_count = get_response('/workstations', params=input_data_str).json()['list_info']['total_count']
    total_count = 100
    batch_size = 100
    total_batches = math.ceil(total_count / batch_size)

    all_workstations = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batch_size,
                "start_index": i * batch_size,
                "sort_field": "id",
                "sort_order": "asc",
                "get_total_count": True
            }
        }

        input_data_str = json.dumps(input_data)

        response = get_response('/workstations', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Projeler başarıyla alındı:")
            for workstation in data['workstations']:
                print(workstation)
                all_workstations.append(workstation)
        else:
            print(f"Projeler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())

    return all_workstations

def get_list_tasks():
    response = get_response('/tasks')
    if response.status_code == 200:
        data = response.json()
        print("Projeler başarıyla alındı:")
        for task in data['tasks']:
            print(task)
    else:
        print(f"Projeler alınamadı. Hata kodu: {response.status_code}")
        print(response.json())

def get_list_purchase_orders():
    response = get_response('/purchase_orders')
    if response.status_code == 200:
        data = response.json()
        print("Satın alma siparişleri başarıyla alındı:")
        for order in data['purchase_orders']:
            print(order)
    else:
        print(f"Satın alma siparişleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())

def get_list_solutions():

    input_data = {
        "list_info": {
            "row_count": 100,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "desc",
            "get_total_count": True
        }
    }

    input_data_str = json.dumps(input_data)
    #FIXME: total count olayını normal haline getir.
    #total_count = get_response('/solutions', params=input_data_str).json()['list_info']['total_count']
    total_count = 100
    batch_size = 100
    total_batches = math.ceil(int(total_count) / batch_size)

    all_solutions = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batch_size,
                "start_index": i * batch_size,
                "sort_field": "id",
                "sort_order": "asc",
                "get_total_count": True
            }
        }

        input_data_str = json.dumps(input_data)

        response = get_response('/solutions', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Çözümler başarıyla alındı:")
            for solution in data['solutions']:
                print(solution)
                all_solutions.append(solution)
        else:
            print(f"Çözümler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())

    return all_solutions

def get_list_admin_project_types():
    response = get_response('/project_types')
    if response.status_code == 200:
        data = response.json()
        print("Proje tipleri başarıyla alındı:")
        for project_type in data['project_types']:
            print(project_type)
    else:
        print(f"Proje tipleri alınamadı. Hata kodu: {response.status_code}")
        print(response.json())

def get_list_admin_project_statuses():
    response = get_response('/project_statuses')
    if response.status_code == 200:
        data = response.json()
        print("Proje durumları başarıyla alındı:")
        for project_status in data['project_statuses']:
            print(project_status)
    else:
        print(f"Proje durumları alınamadı. Hata kodu: {response.status_code}")
        print(response.json())

def get_list_products():

    input_data = {
        "list_info": {
            "row_count": 100,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "desc",
            "get_total_count": True
        }
    }

    input_data_str = json.dumps(input_data)

    #FIXME: total count olayını normal haline getir.
    #total_count = get_response('/products', params=input_data_str).json()['list_info']['total_count']
    total_count = 100
    batch_size = 100
    total_batches = math.ceil(int(total_count) / batch_size)

    all_products = []

    for i in range(0, total_batches):
        input_data = {
            "list_info": {
                "row_count": batch_size,
                "start_index": i * batch_size,
                "sort_field": "id",
                "sort_order": "asc",
                "get_total_count": True
            }
        }

        input_data_str = json.dumps(input_data)

        response = get_response('/products', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            print("Ürünler başarıyla alındı:")
            for product in data['products']:
                print(product)
                all_products.append(product)
        else:
            print(f"Ürünler alınamadı. Hata kodu: {response.status_code}")
            print(response.json())

if __name__ == '__main__':
    get_request_summary_by_id('258497')