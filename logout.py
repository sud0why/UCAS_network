import json
import time
import requests


def logout():
    entrance_url = "http://210.77.16.21/"

    r = requests.get(entrance_url, allow_redirects=False)

    print(r.url)
    # print(r.headers["Location"])

    r = requests.get(r.headers["Location"], allow_redirects=False)

    print(r.url)
    # print(r.headers["Location"])

    r = requests.get(r.headers["Location"], allow_redirects=False)

    print(r.url)
    print(r.status_code)
    print(r.cookies.get_dict())

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

    info_payload = {"userIndex": r.url.split("=")[-1:]}

    info_url = "http://210.77.16.21/eportal/InterFace.do?method=getOnlineUserInfo"

    result = ""
    while result != "success":
        r = requests.post(info_url, data=info_payload, cookies=login_cookie)
        info_response = json.loads(r.text)
        print(info_response["userId"])
        result = info_response["result"]

    logout_url = "http://210.77.16.21/eportal/InterFace.do?method=logout"
    result = ""
    while result != "success":
        r = requests.post(logout_url, data=info_payload, cookies=login_cookie)
        result = json.loads(r.text)["result"]

    return result


if __name__ == "__main__":
    logout()
