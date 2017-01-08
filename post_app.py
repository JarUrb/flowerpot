from datetime import datetime
from json import dumps
from random import randrange
from time import sleep

import requests

from settings import POST_URL


headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


def data_gen(c_id, m_id, device_type, rssi, vcc, temp, moisture, light, num):
    def fluctuate(num):
        return num + randrange(-1, 2)

    while True:
        yield {
            'c_id': c_id,
            'm_id': m_id,
            'device_type': device_type,
            'rssi': fluctuate(rssi),
            'vcc': fluctuate(vcc),
            'temp': fluctuate(temp),
            'moisture': fluctuate(moisture),
            'light': fluctuate(light),
            'num': num,
        }
        num += 1


for data in data_gen(c_id='02:42:d5:8f:e3:a1', m_id=2, device_type='pot', rssi=100, vcc=4.5, temp=20, moisture=50, light=100, num=1):
    print(datetime.now())
    print(data)
    r = requests.post(POST_URL, data='payload='+dumps([data]), headers=headers)
    print(r.status_code, r.json())
    sleep(10)
    print()