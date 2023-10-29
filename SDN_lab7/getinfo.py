 #getinfo.py
 import requests as rq
from requests.auth import HTTPBasicAuth

if __name__ == '__main__':
	url = 'http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes'
	headers = {'Content-Type': 'application/json'}
	response = rq.get(url, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))
	print(response.content)
