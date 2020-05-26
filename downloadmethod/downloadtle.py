# 方法1
# import requests

url = 'http://www.celestrak.com/NORAD/elements/active.txt'
# r = requests.get(url)
# with open('activetle.txt','wb') as fi:
#     fi.write(r.content)

# 方法2
import urllib.request

# urllib.request.urlretrieve(url,'active.txt')

# 方法3

f = urllib.request.urlopen(url)
data = f.read()
with open('activetle.txt','wb') as fi:
    fi.write(data)