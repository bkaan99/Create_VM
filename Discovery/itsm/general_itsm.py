import json
import math
from urllib.error import HTTPError
from urllib.parse import urlencode
import requests
from Discovery import Credentials


def get_response(endpoint='', params = None):
    base_url, api_key = Credentials.itsm_credential()

    url = f"{base_url}{endpoint}"
    api_key = "A919767F-C901-4874-B0D4-0D3EE04CD3F2"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authtoken': api_key
    }

    if params:
        url += "?" + urlencode({"input_data": params})

    response = requests.get(url, headers=headers)
    return response

def get_all_requests(startIndex=0, numberOfData = ''):

    if numberOfData == '':
        numberOfData = 200

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

            input_data_str = json.dumps(input_data)

            response = get_response('/requests', params=input_data_str)

            if response.status_code == 200:
                data = response.json()
                all_requests.append(data['requests'])
                for request in data['requests']:
                    print(request)
            else:
                print(f"Veri çekme hatası: {response.status_code}")
                print(response.json())

            startIndex += batchSize

        except HTTPError as e:
            print(f"HTTP hatası: {e.code}")
            print(e.read())
            break

    return all_requests

def get_all_request_ids(startIndex=0):
    numberOfData = 156612
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
        input_data_str = json.dumps(input_data)

        response = get_response('/requests', params=input_data_str)

        if response.status_code == 200:
            data = response.json()
            for request in data['requests']:
                print(request['id'])
                requests_ids.append(request['id'])

        else:
            print(f"Talep id'leri alınamadı. Hata kodu: {response.status_code}")
            print(response.json())

        startIndex += batchSize

        # Yüzdelik hesaplama
        completed_percentage = ((i + 1) / total_batches) * 100
        print(f"Tamamlanan: %{completed_percentage:.2f}")

    # with open('request_ids.json', 'w') as file:
    #     json.dump(requests_ids, file, indent=2)

    return requests_ids

def get_info_by_request_id(id=''):
    #get request id from get_all_requests

    response = get_response(f'/requests/{id}')

    if response.status_code == 200:
        data = response.json()
        print("Summary başarıyla alındı:")
        summary = data['request']
        for key in summary:
            print(f"{key}: {summary[key]}")

    else:
        print(f"Summary alınamadı. Hata kodu: {response.status_code}")
        print(response.json())

    return summary

def get_request_summary_by_id(id=''):
    response = get_response(f'/requests/{id}/summary')
    if response.status_code == 200:
        data = response.json()
        print("Summary başarıyla alındı:")
        summary = data['request_summary']
        for key in summary:
            print(f"{key}: {summary[key]}")

    else:
        print(f"Summary alınamadı. Hata kodu: {response.status_code}")
        print(response.json())

def add_request(summary, description, requester_id, assignee_id, priority):
    url = "https://supporttest.glasshouse.com.tr/api/v3/requests"
    api_key = "A919767F-C901-4874-B0D4-0D3EE04CD3F2"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authtoken': api_key
    }

    input_data = '''{
        "request": {
            "summary": "Unable to fetch mails",
            "description": "I am unable to fetch mails from the mail server",
            "requester_id": "4",
            "assignee_id": "1",  # Örnek olarak 1 verildi. Gerçek kullanıcı kimliğine göre değiştirilmeli.
            "priority": "High",
            "impact_details": "Routine tasks are pending due to mail server problem",
            "resolution": {
                "content": "Mail Fetching Server problem has been fixed"
            },
            "status": {
                "name": "Open"
            }
        }
    }'''

    data = json.loads(input_data)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("İstek başarıyla eklendi:")
        print(response.json())
    else:
        print(f"İstek eklenirken hata oluştu. Hata kodu: {response.status_code}")
        print(response.json())


if __name__ == "__main__":

    #get_all_requests()
    #get_all_request_ids()
    get_info_by_request_id('258497')
    #get_request_summary_by_id('258471')
    #add_request('bkaandeneme', 'Test açıklama', '1', '1', 'High')