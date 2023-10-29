 import requests
import json

if __name__ == "__main__":
    url = 'http://127.0.0.1:8080/stats/flowentry/add'
    headers = {'Content-Type': 'application/json'}
    flow1 = {
        "dpid": 1,
        "priority": 1,
        "match":{
            "in_port": 1
        },
        "actions":[
            {
                "type": "PUSH_VLAN",    
                "ethertype": 33024      
            },
            {
                "type": "SET_FIELD",
                "field": "vlan_vid",    
                "value": 4096           
            },
            {
                "type": "OUTPUT",
                "port": 3
            }
        ]
    }
    flow2 = {
        "dpid": 1,
        "priority": 1,
        "match":{
            "in_port": 2
        },
        "actions":[
            {
                "type": "PUSH_VLAN",     
                "ethertype": 33024      
            },
            {
                "type": "SET_FIELD",
                "field": "vlan_vid",     
                "value": 4097           
            },
            {
                "type": "OUTPUT",
                "port": 3
            }
        ]
    }
    flow3 = {
        "dpid": 1,
        "priority": 1,
        "match":{
            "vlan_vid": 0
        },
        "actions":[
            {
                "type": "POP_VLAN",    
                "ethertype": 33024     
            },
            {
                "type": "OUTPUT",
                "port": 1
            }
        ]
    }
    flow4 = {
        "dpid": 1,
        "priority": 1,
        "match": {
            "vlan_vid": 1
        },
        "actions": [
            {
                "type": "POP_VLAN", 
                "ethertype": 33024  
            },
            {
                "type": "OUTPUT",
                "port": 2
            }
        ]
    }
    flow5 = {
        "dpid": 2,
        "priority": 1,
        "match": {
            "in_port": 1
        },
        "actions": [
            {
                "type": "PUSH_VLAN", 
                "ethertype": 33024 
            },
            {
                "type": "SET_FIELD",
                "field": "vlan_vid", 
                "value": 4096  
            },
            {
                "type": "OUTPUT",
                "port": 3
            }
        ]
    }
    flow6 = {
        "dpid": 2,
        "priority": 1,
        "match": {
            "in_port": 2
        },
        "actions": [
            {
                "type": "PUSH_VLAN",  
                "ethertype": 33024  
            },
            {
                "type": "SET_FIELD",
                "field": "vlan_vid",  
                "value": 4097 
            },
            {
                "type": "OUTPUT",
                "port": 3
            }
        ]
    }
    flow7 = {
        "dpid": 2,
        "priority": 1,
        "match": {
            "vlan_vid": 0
        },
        "actions": [
            {
                "type": "POP_VLAN", 
                "ethertype": 33024  
            },
            {
                "type": "OUTPUT",
                "port": 1
            }
        ]
    }
    flow8 = {
        "dpid": 2,
        "priority": 1,
        "match": {
            "vlan_vid": 1
        },
        "actions": [
            {
                "type": "POP_VLAN", 
                "ethertype": 33024  
            },
            {
                "type": "OUTPUT",
                "port": 2
            }
        ]
    }
    res1 = requests.post(url, json.dumps(flow1), headers=headers)
    res2 = requests.post(url, json.dumps(flow2), headers=headers)
    res3 = requests.post(url, json.dumps(flow3), headers=headers)
    res4 = requests.post(url, json.dumps(flow4), headers=headers)
    res5 = requests.post(url, json.dumps(flow5), headers=headers)
    res6 = requests.post(url, json.dumps(flow6), headers=headers)
    res7 = requests.post(url, json.dumps(flow7), headers=headers)
    res8 = requests.post(url, json.dumps(flow8), headers=headers)
