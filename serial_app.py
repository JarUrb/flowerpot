#!/usr/bin/env python3

import datetime
import json

import serial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Measurement, get_or_create_sensor
from settings import BAUD_RATE, DATABASE_URI, TTY_DEVICE


DEMO_MODE = b'd\r\n'
NORMAL_MODE = b'n\r\n'


engine = create_engine(DATABASE_URI)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


ser = serial.Serial(TTY_DEVICE, BAUD_RATE, timeout=10)
print(ser.name)
ser.write(NORMAL_MODE)

data = b''

while True:
    data += ser.readline()
    line = data.decode('UTF-8', errors='ignore')
    try:
        measurement_data = json.loads(line)
    except ValueError:
        measurement_data = None
    if measurement_data and isinstance(measurement_data, dict):
        field_transl = {
            'light': 'Light',
            'moisture': 'Moisture',
            'ordinal': 'Nr',
            'rssi': 'Rssi',
            'temperature': 'Temp',
            'vcc': 'Vcc',
        }
        initial_data = {k: measurement_data.get(v) for k, v in field_transl.items()}
        if None not in initial_data.values():
            initial_data['sensor'] = get_or_create_sensor(session, measurement_data.get('ID'))
            measurement = Measurement(**initial_data)
            session.add(measurement)
            session.commit()
            print(datetime.datetime.now(), measurement_data)
        data = b''

ser.close()
