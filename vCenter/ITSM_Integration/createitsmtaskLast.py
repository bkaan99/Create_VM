import requests
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
dataFrameColumns = ["title", "description", "vmlist_id", "status", "createdate", "is_deleted", "version","matchedpytocode","tcode"]
dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
connectionBerko = psycopg2.connect(user="postgres",
                                   password="Cekino.123!",
                                   host="10.14.45.69",
                                   port="7100",
                                   database="karcin_pfms"
                                   )
engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
cursorForExecute = connectionBerko.cursor()
def seleniumItsm():
    full_cookie = ""
    firefox_path = "/usr/bin/firefox"
    firefox_options = Options()
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
def append_dataframe_given_values(title, description, vmlistid, status,date,is_deleted,version,pythoncode,tcode):
    #dataFrameForInsert._append(pd.DataFrame([key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes],columns=dataFrameForInsert.columns,ignore_index=True))
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[title, description, vmlistid, status,date, is_deleted, version,pythoncode,tcode]
def createTaskItsm(vmid, cookie):
    #cookie = seleniumItsm()
    query = """select
                            kstd.description ,
                            ktd.taskname,
                            ktd.matchedpytocode
                            from kr_service_task_definition kstd
                            inner join
                            kr_task_definition ktd
                            on kstd.id = ktd.service_task_definition_id
                            where kstd.id in ( select kvl.servicetaskdefinition_id
                            from kr_vm_list kvl where
                            kvl.id = %s
                            and kvl.is_deleted =false
                            limit 1
                            )
                            and ktd.is_deleted=false
                            and kstd.is_deleted =false
                            """ % str(vmid)
    cursorForExecute.execute(query)
    resultList = cursorForExecute.fetchall()
    # @TODO 0 TITLE 1 DESCRIPTION
    #createTaskItsm("pyhtondan ekledim 14.49", "titleBülo3")
    #deleteTask("silinecek veri")
    for i, item in enumerate(resultList):
        TCODE = str(time.time()).replace(".","")
        append_dataframe_given_values(item[1], item[0]+"|"+TCODE, vmid, "STARTED", datetime.now(),
                                      False, 1,str(item[2]),TCODE)
        start_index = cookie.find("_zcsr_tmp=") + len("_zcsr_tmp=")
        end_index = cookie.find(";", start_index)
        zcsr_tmp_value = cookie[start_index:end_index]
        zcsr_tmp_value = str(zcsr_tmp_value).replace("'", "")
        url = "https://supporttest.glasshouse.com.tr/TaskDefAction.do"
        data = {
            "sdpcsrfparam": zcsr_tmp_value.strip("'"),
            "TASKID": "",
            "from": "QuickLink",
            "module": "general",
            "associatedEntityID": None,
            "scopeid": None,
            "TASKTEMPLATEID": "1822",
            "TITLE": item[1],
            "STATUSID": "1",
            "DESCRIPTION": item[0]+"|"+TCODE,
            "MOD_IND": "task",
            "FORMNAME": "TaskForm",
            "EstimatedEffort": "0",
            "Estimated_Effort_Days": "0",
            "Estimated_Effort_Hours": "4",
            "Estimated_Effort_Minutes": "0",
            "taskPriority": "4",
            "OWNERID_Disp": "27901",
            "MarkedStatus": "Assign",
            "MarkedOwnerID": None,
            "OWNERID": "27901",
            "Task_SCHEDULEDSTARTTIME": "",
            "Task_SCHEDULEDSTARTTIME_Display": "From",
            "Task_SCHEDULEDENDTIME": "",
            "Task_SCHEDULEDENDTIME_Display": "To",
            "taskType": "332",
            "Task_ACTUALSTARTTIME": "",
            "Task_ACTUALSTARTTIME_Display": "From",
            "Task_ACTUALENDTIME": "",
            "Task_ACTUALENDTIME_Display": "To",
            "perOfCompletion": "",
            "taskAddtionalCost": "0.0",
            "COMMENTS": "",
            "files": "",
            "submitaction": "AddTask"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie
        }
        try:
            response = requests.post(url, data=data, headers=headers, allow_redirects=False)
            time.sleep(0.01)
        except Exception as e:
            pass
    dataFrameForInsert.to_sql("kr_create_task", engineForPostgres, chunksize=5000, index=False, method=None,
                              if_exists='append')