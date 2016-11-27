#!/usr/bin/env python3

import datetime
import json

import serial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Measurement, Sensor
from settings import BAUD_RATE, DATABASE_URI, TTY_DEVICE


DEMO_MODE = b'd\r\n'


def get_or_create_sensor(session, name):
    sensor = session.query(Sensor).filter_by(name=name).first()
    if sensor:
        return sensor
    else:
        sensor = Sensor(name)
        session.add(sensor)
        return sensor


engine = create_engine(DATABASE_URI)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


ser = serial.Serial(TTY_DEVICE, BAUD_RATE, timeout=10)
print(ser.name)
ser.write(DEMO_MODE)

data = b''

while True:
    data += ser.readline()
    line = data.decode('UTF-8')
    try:
        measurement_data = json.loads(line)
    except json.JSONDecodeError:
        measurement_data = None
    if measurement_data:
        sensor = get_or_create_sensor(session, measurement_data.get('ID'))
        measurement = Measurement(
            light=measurement_data.get('Light'),
            moisture=measurement_data.get('Moisture'),
            ordinal=measurement_data.get('Nr'),
            rssi=measurement_data.get('Rssi'),
            sensor=sensor,
            temperature=measurement_data.get('Temp'),
            vcc=measurement_data.get('Vcc'),
        )
        session.add(measurement)
        session.commit()
        print(datetime.datetime.now(), measurement_data)
        data = b''

ser.close()
