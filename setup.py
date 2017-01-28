#!/usr/bin/env python3

from sqlalchemy import create_engine

from models import Base
from settings import DATABASE_URI


def setup():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    setup()
