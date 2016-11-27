import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Sensor {} {}>'.format(self.id, self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    moisture = Column(Float)
    light = Column(Float)
    rssi = Column(Float)
    vcc = Column(Float)
    ordinal = Column(Integer)
    timestamp = Column(DateTime)
    sensor_id = Column(Integer, ForeignKey(Sensor.id))
    sensor = relationship(Sensor)

    def __init__(self, temperature, moisture, light, rssi, vcc, sensor, ordinal, timestamp=None, *args, **kwargs):
        self.temperature = temperature
        self.moisture = moisture
        self.light = light
        self.rssi = rssi
        self.vcc = vcc
        self.sensor = sensor
        self.ordinal = ordinal
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()
        self.timestamp = timestamp

    def __repr__(self):
        return '<Measurement {} {}>'.format(self.timestamp, self.sensor)
