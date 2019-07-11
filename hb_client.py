#!/usr/bin/env python3
import json
import os
import re
import requests
import time


device_name = 'Mixcro_Xiaoshan'
sckey = 'SCU55002T135fbe55be5a5531bd6df5f4c705e09e5d244b51bd204'

def serverchan(title, content=''):
    url = 'https://sc.ftqq.com/%s.send'%sckey
    payload = {
        'text': title,
        'desp': content,
    }
    r = requests.get(url, params=payload)
    return(r.status_code)


def heartbeat(addr_4, addr_6, addr_raw):
    url = 'http://hb.meow.earth/heartbeat/%s'%device_name
    payload = {
        'addr_6' : addr_6,
        'addr_4' : addr_4,
        'addr_raw' : addr_raw
    }
    r = requests.post(url ,data=payload)
    return(json.loads(r.text)['status_code'])

if __name__ == '__main__':
    timestamp = 0
    pr_addr_6 = []
    pr_addr_4 = []
    while True:
        try:
            cr = os.popen('ifconfig').read()
            addr_6 = re.findall(r'inet6 (.+?) prefixlen', cr)
            addr_6 = [x.split()[0] for x in addr_6]
            for addr in addr_6:
                if addr[:4] in ['fe80', 'fe69']:
                    addr_6.remove(addr)
            addr_6 = json.dumps(addr_6)
            addr_4 = re.findall(r'inet (.+?) netmask', cr)
            if "127.0.0.1" in addr_4:
                addr_4.remove("127.0.0.1")
            addr_4 = json.dumps(addr_4)
            if (time.time()-timestamp>3600) or (addr_4 != pr_addr_4) or (addr_6 != pr_addr_6):
                if (addr_4 != pr_addr_4) or (addr_6 != pr_addr_6):
                    title = '%s Addr Update!'%device_name
                    content = json.dumps({'addr_4': re.sub('"', "'", addr_4),
                                          'addr_6': re.sub('"', "'", addr_6),
                                          'time': time.ctime(time.time())})
                    serverchan(title, content)
                if heartbeat(addr_4, addr_6, cr) == 0:
                    timestamp = time.time()
                    pr_addr_6 = addr_6
                    pr_addr_4 = addr_4
                    print('%s: updated!' % time.ctime(time.time()))
            else:
                print('%s: too lazy, can not move.'%time.ctime(time.time()))
            time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(30)

