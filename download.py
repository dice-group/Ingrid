import requests
import os
from datetime import datetime
# url = 'https://media.uni-paderborn.de/api/v1/session?cookieauth=1'

# r = requests.get(url)
# #print(r.json())
# cookies = r.cookies
# token = r.json()['token']


# url = 'https://media.uni-paderborn.de/api/v1/session/sso/authenticate'

# #r = requests.get(url, params={'token': token})
# r = requests.get(url, cookies=cookies)
# # print(r.text)


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


now = datetime.now().strftime("%Y-%m-%d")
pathName = 'jsonFiles_'+now
os.mkdir(pathName)

# get session token
# GET /api/v1/session
t = requests.get('https://media.uni-paderborn.de/api/v1/session', params={})
token = t.json()['token']


# auth
# POST /api/v1/session/authenticate?token=<token>[&method=<method>][&login=<login>&password=<password>][&success=<success>][&error=<error>][&response_type=<response_type>][&remember_me={1|0}][&log_event={1|0}]
auth = requests.post('https://media.uni-paderborn.de/api/v1/session/authenticate?token='+token, params={'login': '', 'password': ''})
# print(auth.json())

url = 'https://media.uni-paderborn.de/api/v1/search'
num = 0
for x in my_range(0, 130000, 1000):

     r = requests.post(url, params={'token': token}, json={'offset': x})
     #print(r.text)

     f = open(pathName+'/jsonfile'+str(num)+'.json', "w", encoding="utf8")
     f.write(r.text)
     num = num + 1

#r = requests.post(url, params={'token': token}, json={'offset': 1000})
#print(r.text)

url = "https://media.uni-paderborn.de/api/v1/tags"
r = requests.get(url, params={'token': token})
f = open(pathName+'/jsonfile_tags.json', "w", encoding="utf8")
f.write(r.text)

url = "https://media.uni-paderborn.de/api/v1/collection/list"
r = requests.get(url, params={'token': token})
f = open(pathName+'/jsonfile_collection_list.json', "w", encoding="utf8")
f.write(r.text)