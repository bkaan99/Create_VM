import base64
import re
import sys

def get_id_list() -> list or None:
    try:
        mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
        mystring = mystring.replace("[", "").replace("]", "")
        li = list(mystring.replace(' ', '').split(","))
        return li

    except (IndexError, ValueError, TypeError) as e:
        print("Argümanları işlerken bir hata oluştu:", e)
        return None

def get_powerOpsCode_from_id() -> int or None:
    try:
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

    except (IndexError, ValueError, TypeError, re.error) as e:
        print("Argümanları işlerken bir hata oluştu:", e)
        return None
