import requests
import psycopg2
import pandas as pd
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

#statusId = 1202
dataFrameColumns = ["title", "description", "vmlist_id", "status", "createdate", "is_deleted", "version","matchedpytocode","tcode"]
dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
connectionBerko = psycopg2.connect(user="postgres",
                                   password="Cekino.123!",
                                   host="10.14.45.69",
                                   port="7100",
                                   database="karcin_pfms"
                                   )
cursorForExecute = connectionBerko.cursor()

def getIdList(cookie,description):
    url = "https://supporttest.glasshouse.com.tr/api/v3/tasks?input_data=%7B%22list_info%22%3A%7B%22row_count%22%3A%22500%22%2C%22sort_field%22%3A%22id%22%2C%22sort_order%22%3A%22D%22%2C%22filter%22%3A%220%22%7D%2C%22fields_required%22%3A%5B%22id%22%2C%22title%22%2C%22status%22%2C%22priority%22%2C%22group%22%2C%22owner%22%2C%22scheduled_start_time%22%2C%22description%22%5D%7D&SUBREQUEST=XMLHTTP&_=1707406665"
    #url = "https://supporttest.glasshouse.com.tr/api/v3/tasks?input_data=%7B%22list_info%22%3A%7B%22row_count%22%3A%2250%22%2C%22sort_field%22%3A%22id%22%2C%22sort_order%22%3A%22D%22%2C%22filter%22%3A%220%22%7D%2C%22fields_required%22%3A%5B%22id%22%2C%22title%22%2C%22status%22%2C%22priority%22%2C%22group%22%2C%22owner%22%2C%22scheduled_start_time%22%2C%22description%22%5D%7D&SUBREQUEST=XMLHTTP&_=1707406665"
    #url ="https://supporttest.glasshouse.com.tr/api/v3/tasks?input_data=%7B%22list_info%22%3A%7B%22row_count%22%3A%2225%22%2C%22sort_field%22%3A%22id%22%2C%22sort_order%22%3A%22D%22%2C%22filter%22%3A%220%22%7D%2C%22fields_required%22%3A%5B%22id%22%2C%22title%22%2C%22status%22%2C%22priority%22%2C%22group%22%2C%22owner%22%2C%22scheduled_start_time%22%5D%7D&SUBREQUEST=XMLHTTP&_=1707406666"
    #url = "https://supporttest.glasshouse.com.tr/api/v3/tasks?input_data=%7B%22list_info%22%3A%7B%22row_count%22%3A%2225%22%2C%22start_index%22%3A%221%22%2C%22search_fields%22%3A%7B%22owner%22%3A%22%C3%87ekinoITSMUser%22%7D%2C%22sort_field%22%3A%22id%22%2C%22sort_order%22%3A%22A%22%2C%22filter%22%3A%220%22%7D%2C%22fields_required%22%3A%5B%22id%22%2C%22title%22%2C%22status%22%2C%22priority%22%2C%22group%22%2C%22owner%22%2C%22scheduled_start_time%22%5D%7D&SUBREQUEST=XMLHTTP&_=1705490084780"
    headers = {
        "Cookie": cookie
    }
    correctIdList = []
    response = requests.get(url, headers=headers, allow_redirects=False)
    jsonResponse = response.json()
    print(description)
    for t in range(len(jsonResponse.get("tasks"))):
        if response.json().get("tasks")[t].get("description").__eq__(description):
            idToUpdateTask = response.json().get("tasks")[t].get("id")
            correctIdList.append(idToUpdateTask)



    #idList = [task['id'] for task in jsonResponse.get('tasks', [])]
    return idToUpdateTask
def findTask(cookie, idList, description):
    for id in idList:
        url = "https://supporttest.glasshouse.com.tr/TaskDefAction.do?submitaction=viewTask&TASKID="+id+"&from=QuickLink"
        headers = {
            "Cookie": cookie
        }
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.text.find(description) > 0:
            return id
        else:
            return id
def seleniumItsm():
    full_cookie = ""
    firefox_path = "/usr/bin/firefox"
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.headless = True
    firefox_options.add_argument("--display=:99")
    driver = webdriver.Firefox(options=firefox_options)
    try:
        driver.get("https://supporttest.glasshouse.com.tr/")
        username = "cekinoitsmuser"
        password = "Cekino123!!"
        username_input = driver.find_element(By.XPATH,
                                             "/html/body/div[1]/div[2]/div/div/div[2]/div/form/div/div[2]/div/div/div/div[1]/div/input")
        password_input = driver.find_element(By.XPATH,
                                             "/html/body/div[1]/div[2]/div/div/div[2]/div/form/div/div[2]/div/div/div/div[2]/div/input")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = driver.find_element(By.XPATH,
                                           "/html/body/div[1]/div[2]/div/div/div[2]/div/form/div/div[2]/div/div/div/div[17]/button")
        login_button.click()
        #  time.sleep(8)
        cookies = driver.get_cookies()
        for cookie in cookies:
            full_cookie += f"{cookie['name']}={cookie['value']};"
    except Exception as e:
        print(e)
        return None
    finally:
        driver.quit()
    return full_cookie
def updateTaskItsm(description, title, statusId, vmid, cookie):
    #cookie = seleniumItsm()
    start_index = cookie.find("_zcsr_tmp=") + len("_zcsr_tmp=")
    end_index = cookie.find(";", start_index)
    zcsr_tmp_value = cookie[start_index:end_index]
    zcsr_tmp_value = str(zcsr_tmp_value).replace("'", "")
    idList = getIdList(cookie,description)
    print(idList)
    #burada bizim userımızın açtığı bütün taskların id listesi alınıyor.
    #taskId = findTask(cookie, idList, description)



    #burada da unique olan descriptiona göre aranıp id si bulunuyor ve update işlemi için gönderiliyor.
    #taskLong = int(taskId)
    url = "https://supporttest.glasshouse.com.tr/TaskDefAction.do"
    # data = {
    #     "sdpcsrfparam": str(zcsr_tmp_value).replace("'", ""),
    #     "TASKID": taskLong,
    #     "from": "QuickLink",
    #     "module": "general",
    #     "associatedEntityID": None,
    #     "scopeid": None,
    #     "TASKTEMPLATEID": "1822",
    #     "TITLE": title,
    #     "STATUSID": statusId,
    #     "DESCRIPTION": description,
    #     "MOD_IND": "task",
    #     "FORMNAME": "TaskForm",
    #     "EstimatedEffort": "0",
    #     "Estimated_Effort_Days": "0",
    #     "Estimated_Effort_Hours": "4",
    #     "Estimated_Effort_Minutes": "0",
    #     "taskPriority": "4",
    #     "OWNERID_Disp": "27901",
    #     "MarkedStatus": "Assign",
    #     "MarkedOwnerID": None,
    #     "OWNERID": "27901",
    #     "Task_SCHEDULEDSTARTTIME": "",
    #     "Task_SCHEDULEDSTARTTIME_Display": "From",
    #     "Task_SCHEDULEDENDTIME": "",
    #     "Task_SCHEDULEDENDTIME_Display": "To",
    #     "taskType": "332",
    #     "Task_ACTUALSTARTTIME": "",
    #     "Task_ACTUALSTARTTIME_Display": "From",
    #     "Task_ACTUALENDTIME": "",
    #     "Task_ACTUALENDTIME_Display": "To",
    #     "perOfCompletion": "",
    #     "taskAddtionalCost": "0.0",
    #     "COMMENTS": "",
    #     "files": "",
    #     "submitaction": "updateTask"
    # }
    data = {
        "sdpcsrfparam": str(zcsr_tmp_value).replace("'", ""),
        "submitaction": "updateTask",
        "TASKID": idList,
        "from": "InlineSubmit",
        "files": "",
        "site":"",
        "STATUSID": statusId,
        "Inline_selectattribute": "STATUSID"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie
    }
    try:
        print("===========")
        response = requests.post(url, data=data, headers=headers, allow_redirects=False)
        queryToExecute = "update kr_create_task set status = 'COMPLETE' where vmlist_id = "+str(vmid)+" and title ='"+ str(title)+"'"
        cursorForExecute.execute(queryToExecute)
        #cursorForExecute.fetchall()
        connectionBerko.commit()
        print(response.headers)
        print("Response Code:", response.status_code)
        if response.status_code == 200:
            print("CEMCEMCEM")



    except Exception as e:
        print(e)