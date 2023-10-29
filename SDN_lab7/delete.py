 #!/usr/bin/python
 #delete.py
import requests
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    url = 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/'
    headers = {'Content-Type': 'application/json'}
    res = requests.delete(url, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))
    print (res.content)
