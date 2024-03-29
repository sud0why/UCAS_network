import json
import random
import time
import requests


def login(userid, password):
    entrance_url = "http://210.77.16.21/"

    r = requests.get(entrance_url, allow_redirects=False)

    # print(r.url)
    # print(r.headers["Location"])

    r = requests.get(r.headers["Location"], allow_redirects=False)

    # print(r.url)
    # print(r.headers["Location"])

    r = requests.get(r.headers["Location"], allow_redirects=False)

    # print(r.url)
    # print(r.status_code)
    # print(r.cookies.get_dict())

    queryString = r.url.split("?")[1]
    queryString = queryString.replace("=", "%253D")
    queryString = queryString.replace("&", "%2526")
    # print(queryString)

    payload = {'userId': userid, 'password': password, "service": "", "queryString": queryString,
               "operatorPwd": "", "operatorUserId": "", "validcode": "", "passwordEncrypt": "false"}

    login_cookie = r.cookies.get_dict()
    login_cookie["EPORTAL_COOKIE_USERNAME"] = ""
    login_cookie["EPORTAL_COOKIE_PASSWORD"] = ""
    login_cookie["EPORTAL_COOKIE_SERVER"] = ""
    login_cookie["EPORTAL_COOKIE_SERVER_NAME"] = ""
    login_cookie["EPORTAL_COOKIE_OPERATORPWD"] = ""
    login_cookie["EPORTAL_COOKIE_DOMAIN"] = ""
    login_cookie["EPORTAL_COOKIE_SAVEPASSWORD"] = "false"
    login_cookie["EPORTAL_AUTO_LAND"] = "false"
    login_cookie["EPORTAL_USER_GROUP"] = "null"

    login_url = "http://210.77.16.21/eportal/InterFace.do?method=login"

    r = requests.post(login_url, data=payload, cookies=login_cookie)

    # print(r.status_code)

    login_response = json.loads(r.text)
    # print(login_response)
    info_payload = {"userIndex": login_response["userIndex"]}

    info_url = "http://210.77.16.21/eportal/InterFace.do?method=getOnlineUserInfo"

    result = ""
    while result != "success":
        r = requests.post(info_url, data=info_payload, cookies=login_cookie)
        info_response = json.loads(r.text)
        result = info_response["result"]
        if result == "fail":
            break

    if result == "fail":
        return ""
    
    return result


if __name__ == "__main__":
    with open('available.json', 'r') as f:
        datas = json.load(f)

    with open('used.json', 'r') as f:
        used = json.load(f)

    for id in datas.keys():
        if int(datas[id]["flow"].split(".")[0]) < 3500:
            datas.pop(id)

    id = random.choice(list(datas.keys()))
    print(id)
    result = login(id, datas[id]["password"])
    print(result)

    if id not in used:
        used.append(id)

    with open('used.json', 'w') as f:
        json.dump(used, f)

