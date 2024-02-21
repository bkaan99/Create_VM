import base64
import re
import sys

def get_id_list():
    global flowUUID
    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")
    li = list(mystring.replace(' ', '').split(","))

    #TODO: flowUUID tekrar eklenecek. Yorumda olan yerler açılacak.
    if len(li) > 0:
        #flowUUID = li[0];
        #li.pop(0)
        print(f"Removed value: {li}")
    else:
        print("List is empty.")

    return li #, flowUUID


def get_powerOpsCode_from_id():
    powerOpsCode = base64.b64decode(sys.argv[2]).decode('UTF-8')
    match = re.match(r"\[([^:]+):(\d+)\]", powerOpsCode)

    if match:
        powerOpsCode_key = match.group(1)
        powerOpsCode_value = int(match.group(2))  # Eğer sayı olarak almak istiyorsanız int dönüşümü yapabilirsiniz
        print(f"Key: {powerOpsCode_key}, Value: {powerOpsCode_value}")

        return powerOpsCode_value

    else:
        print("Gelen değer istenen formatta değil.")
        return None