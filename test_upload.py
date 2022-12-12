import requests
import sys


fileobj = open(sys.argv[1], 'rb')
if len (sys.argv) > 2:
    print('server url present')
    url = sys.argv[2]
else:
    url = 'http://httpbin.org/post'

r = requests.post(url, data={"mysubmit":"Go"}, files={"file": (sys.argv[1], fileobj)})
print(r.content)