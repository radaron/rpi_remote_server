# pylint: disable=global-statement

from os import path
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


ENGINE = None
Base = declarative_base()


class RpiOrders(Base):
    __tablename__ = 'rpi_orders'

    name = db.Column(db.String(50), primary_key=True)
    host = db.Column(db.String(50))
    username = db.Column(db.String(50))
    port = db.Column(db.Integer)
    polled_date = db.Column(db.DateTime)
    passwd = db.Column(db.String(50))


class Authentication(Base):
    __tablename__ = 'authentication'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    salt = db.Column(db.String(50))

table_objects = [RpiOrders.__table__, Authentication.__table__]

def init_db():
    global ENGINE
    db_path = path.abspath(path.join(path.dirname(__file__), "data/database.db"))
    ENGINE = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(ENGINE, tables=table_objects)


def get_session():
    ses = sessionmaker(bind=ENGINE)
    return ses()
