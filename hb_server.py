#!/usr/bin/env python3
import time
import json
from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def device_list():
    return(json.dumps(device_pool, indent=1))

@app.route('/raw')
def device_raw_list():
    return(json.dumps(device_raw_pool, indent=1))


@app.route('/heartbeat/<device>', methods=['POST'])
def get_device(device):
    try:
        addr_raw = request.form['addr_raw']
        log(device, addr_raw)
        addr_6 = json.loads(request.form['addr_6'])
        addr_4= json.loads(request.form['addr_4'])
        sign_device(device, addr_4, addr_6, addr_raw)
        return(json.dumps({'status_code': 0, 'status': 'success'}))
    except Exception as e:
        print(e)
        return (json.dumps({'status_code': 1, 'status': 'key err'}))

def sign_device(device, addr_4, addr_6, addr_raw):
    global device_pool, device_raw_pool
    device_pool[device] = {
        'addr_4': addr_4,
        'addr_6': addr_6,
        'update_time': time.ctime(time.time())
    }
    device_raw_pool[device] = addr_raw

def log(device, content):
    with open("./log.txt", 'a') as f:
        content = '%s %s\n %s \n\n'%(time.ctime(time.time()), device, content)
        f.write(content)

if __name__ == '__main__':

    device_pool = {}
    device_raw_pool = {}


    app.run(port=8848)