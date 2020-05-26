from urllib import request
import requests
import os
import sys
import urllib

'''几种下载文件的方式'''

url = 'http://www.celestrak.com/NORAD/elements/active.txt'

# request方法
# resp = request.urlopen('http://www.celestrak.com/NORAD/elements/active.txt')
# tlestr = resp.read().decode()
# print(type(tlestr))
# with open('activetle.txt','w') as fi:
#     fi.write(tlestr)

# requests方法
resp = requests.get(url)
# print(resp.headers['Content-Length'])
# resp.headers.get('content-length')
# print(resp.text)
# print(resp.headers)
# print(resp.status_code)
# print(tuple(resp.cookies))
# with open('activetle.txt','wb') as fi:
# fi.write(resp.content)

# urllib 方法
# request.urlretrieve(url, 'activetle.txt')
