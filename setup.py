#!/usr/bin/env python3

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Sensor
from settings import DATABASE_URI


def setup():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    dummy_sensor = Sensor(name=datetime.datetime.now().isoformat(' '))
    session.add(dummy_sensor)
    session.commit()


if __name__ == '__main__':
    setup()
