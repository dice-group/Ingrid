import requests
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


token='example'

url = 'https://media.uni-paderborn.de/api/v1/search'
num = 0
for x in my_range(0, 100000, 1000):

     r = requests.post(url, params={'token': token}, json={'offset': x})
     #print(r.text)

     f = open('jsonFiles/jsonfile'+str(num)+'.json', "w")
     f.write(r.text)
     num = num + 1

#r = requests.post(url, params={'token': token}, json={'offset': 1000})
#print(r.text)

