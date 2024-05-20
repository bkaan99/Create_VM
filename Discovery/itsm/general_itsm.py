import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen,Request
import requests

def get_response(endpoint='', params = None):
    url = f"https://supporttest.glasshouse.com.tr/api/v3{endpoint}"
    api_key = "A919767F-C901-4874-B0D4-0D3EE04CD3F2"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authtoken': api_key
    }
    response = requests.get(url, headers=headers, params=params)
    return response

def get_all_requests():

    response = get_response('/requests')

    if response.status_code == 200:
        data = response.json()
        print("Veriler başarıyla çekildi:")
        for request in data['requests']:
            print(request)

    else:
        print(f"Veri çekme hatası: {response.status_code}")
        print(response.json())

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
    get_all_requests()
    #get_info_by_request_id('66008')
    #get_request_summary_by_id('258471')
    #add_request('bkaandeneme', 'Test açıklama', '1', '1', 'High')


