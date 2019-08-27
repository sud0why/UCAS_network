import json
import requests

entrance_url = "http://210.77.16.21/"

r = requests.get(entrance_url, allow_redirects=False)

print(r.url)
print(r.headers["Location"])

r = requests.get(r.headers["Location"], allow_redirects=False)

print(r.url)
print(r.headers["Location"])

r = requests.get(r.headers["Location"], allow_redirects=False)

print(r.url)
print(r.status_code)
print(r.cookies.get_dict())

queryString = r.url.split("?")[1]
queryString = queryString.replace("=", "%253D")
queryString = queryString.replace("&", "%2526")
print(queryString)

payload = {'userId': 'xxxxx', 'password': '22261X', "service": "", "queryString": queryString,
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

print(r.status_code)

login_response = json.loads(r.text)
print(login_response)
info_payload = {"userIndex": login_response["userIndex"]}

info_url = "http://210.77.16.21/eportal/InterFace.do?method=getOnlineUserInfo"

r = requests.post(info_url, data=info_payload, cookies=login_cookie)

info_response = json.loads(r.text)

print(info_response["maxFlow"])
print(info_response["userId"])

print("done")
