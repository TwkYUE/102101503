import requests
import re
import random
import time
import xml.etree.ElementTree as ET
import openpyxl
import json
import pandas as pd

#请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

content = input("请输入你要检索的内容: ")
keyword = content

#获得cookies
cookies = requests.get('https://www.bilibili.com/', headers=headers).cookies.get_dict()
bvids = []
#获取多少个页面的信息，一个页面有20个，共需要15页
for page in range(0, 15):
    url = f"https://api.bilibili.com/x/web-interface/wbi/search/type?keyword={keyword}&search_type=video&page={page + 1}"
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:#只有是200才能算请求成功
        #print(f"正在获取页面bvid，现在已进行到 {page+1}/15")
        print(f"请求状态码：{response.status_code}")
        #使用 JSON 解析方式提取 BV 号
        response_dict = response.json()
        result_list = response_dict.get('data', {}).get('result', [])
        for result in result_list:
            bvid = result.get('bvid')
            if bvid:
                bvids.append(bvid)
        #模拟人类的行为模式，给请求之间增加一定的随机性和间隔，以减轻对服务器的负载压力
        time.sleep(round(random.uniform(0, 3), 3))
    else:
        print(f"请求失败，状态码：{response.status_code}")
    
print(bvids)检验BV号是否正确提取出来
