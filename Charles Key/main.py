import requests
import random
import json
import time

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def generate_username(username_length, username_type):
    username = ''
    estr_0 = '0123456789zxcvbnmasdfghjklqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM'
    estr_1 = 'zxcvbnmasdfghjklqwertyuiop'
    for i in range(0,username_length):
        if username_type == 0:
            username += estr_0[random.randint(0, len(estr_0)-1)]
        elif username_type == 1:
            username += estr_1[random.randint(0, len(estr_1)-1)]
    return(username)

def log(content):
    line = ', '.join(content)
    line += '\n'
    with open('./log.txt', 'a') as f:
        f.write(line)

if __name__ == '__main__':
    url = 'https://charles.wrbug.com/api/licenseKey/generate'
    for i in range(0, 1024):
        user_name = generate_username(random.randint(6, 10), random.randint(0, 1))
        payload = {'username': user_name}
        r = requests.post(url, headers=headers, data=payload)
        license_key = json.loads(r.text)['data']
        print(license_key, user_name)
        log([user_name, license_key])
        # time.sleep(0.1)