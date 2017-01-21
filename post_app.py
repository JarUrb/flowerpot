from json import dumps
from random import randrange
from time import sleep

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Measurement, Sensor
from settings import POST_URL, HUB_ID, DATABASE_URI


DEVICE_TYPE = 'pot'
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


def measurement_to_dict(measurement):
    return {
        'c_id': HUB_ID,
        'm_id': measurement.sensor.name,
        'device_type': DEVICE_TYPE,
        'rssi': measurement.rssi,
        'vcc': measurement.vcc,
        'temp': measurement.temperature,
        'moisture': measurement.moisture,
        'light': measurement.light,
        'num': measurement.ordinal,
    }


def fake_measurement_generator(m_id, rssi, vcc, temp, moisture, light, num):
    def fluctuate(num):
        return num + randrange(-1, 2)

    while True:
        yield Measurement(
            light=fluctuate(light),
            moisture=fluctuate(moisture),
            ordinal=num,
            rssi=fluctuate(rssi),
            sensor=Sensor(name=m_id),
            temperature=fluctuate(temp),
            vcc=fluctuate(vcc),
        )
        num += 1


def post_measurements(list_of_measurements):
    list_of_dicts = list(map(measurement_to_dict, list_of_measurements))
    print(list_of_dicts)
    return requests.post(POST_URL, data='payload=' + dumps(list_of_dicts), headers=HEADERS)


def post_fake_measurements(interval=10):
    for measurement in fake_measurement_generator(m_id=2, rssi=100, vcc=4, temp=20, moisture=50, light=100, num=1):
        r = post_measurements([measurement])
        sleep(interval)


def post_unposted_measurements():
    engine = create_engine(DATABASE_URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    measurements_to_post = session.query(Measurement).filter_by(posted=False)
    if measurements_to_post:
        try:
            response = post_measurements(measurements_to_post)
        except requests.exceptions.ConnectionError:
            response = None
        if response and response.status_code == 200:
            if response.json().get('result'):
                for measurement in measurements_to_post:
                    measurement.posted = True
                    session.add(measurement)
                session.commit()


if __name__ == '__main__':
    while True:
        post_unposted_measurements()
        sleep(60)
