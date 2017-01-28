#!/usr/bin/env python3

from collections import OrderedDict

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from models import Measurement, Sensor
from settings import DATABASE_URI, HUB_ID


COLUMNS = OrderedDict([
    ('ordinal', 'Lp.'),
    ('timestamp', 'Data/godzina'),
    ('temperature', 'Temperatura [°C]'),
    ('moisture', 'Wilgotność [%]'),
    ('light', 'Oświetlenie'),
    ('rssi', 'Sygnał'),
    ('vcc', 'Napięcie [V]'),
    ('posted', 'Wysłane?'),
])


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.debug = True
db = SQLAlchemy(app)


@app.route('/')
def root():
    sensors = db.session.query(Sensor).all()
    return render_template(
        'sensors.html',
        hub_id=HUB_ID,
        sensors=sensors,
    )


@app.route('/<int:sensor_pk>/')
def measurement(sensor_pk):
    sensor = db.session.query(Sensor).filter_by(pk=sensor_pk).first()
    measurements = db.session.query(Measurement).filter_by(sensor=sensor).order_by(desc(Measurement.timestamp)).all()

    return render_template(
        'measurements.html',
        columns=COLUMNS.values(),
        measurements=[[getattr(m, k) for k in COLUMNS.keys()] for m in measurements],
        sensor=sensor,
    )


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
