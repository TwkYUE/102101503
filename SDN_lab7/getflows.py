 import requests
import time
import re


class GetNodes:
    def __init__(self, ip):
        self.ip = ip
        
    def get_switch_id(self):
        url = 'http://' + self.ip + '/stats/switches'
        re_switch_id = requests.get(url=url).json()
        switch_id = []
        for i in re_switch_id:
            switch_id_hex.append(i)

        return switch_id

    def getflow(self):
        url = 'http://' + self.ip + '/stats/flow/%d'
        switch_list = self.get_switch_id()
        ret_flow = []
        for switch in switch_list:
            new_url = format(url % int(switch))
            re_switch_flow = requests.get(url=new_url).json()
            ret_flow.append(re_switch_flow)
        return ret_flow

    def show(self):
        flow_list = self.getflow()
        for flow in flow_list:
            for dpid in flow.keys():
                dp_id = dpid
                switchnum= '{}'.format(int(dp_id))        
                print('s'+switchnum,end = " ")
                switchnum = int(switchnum)
            for list_table in flow.values():
                for table in list_table:          
                    string1 = str(table)
                    if re.search("'dl_vlan': '(.*?)'", string1) is not None:
                       num = re.search("'dl_vlan': '(.*?)'", string1).group(1);
                       if num == '0' and switchnum == 1:
                          print('h1',end = " ")
                       if num == '1' and switchnum == 1:
                          print('h2',end = " ")
                       if num == '0' and switchnum == 2:
                          print('h3',end = " ")
                       if num == '1' and switchnum == 2:
                          print('h4',end = " ")
        print("")
        flow_list = self.getflow()
        for flow in flow_list:
            for dpid in flow.keys():
                dp_id = dpid
                print('switch_name:s{}'.format(int(dp_id)))
            for list_table in flow.values():
                for table in list_table:
                    print(table)
                    
                    
s1 = GetNodes("127.0.0.1:8080")
s1.show()
