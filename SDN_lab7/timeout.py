#!/usr/bin/python
import requests
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    url = 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/1'
    with open("/home/thy/Ubuntu/102101503/lab777/public/flowtable.json") as f:
        jstr = f.read()
    headers = {'Content-Type': 'application/json'}
    res = requests.put(url, jstr, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))
    print (res.content)
