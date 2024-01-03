# pylint: disable=global-statement

from os import path, environ
from time import sleep
from sqlalchemy import String, Integer, Column
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import (
  sessionmaker, relationship, Mapped,
  mapped_column, declarative_base
)


ENGINE = None
Base = declarative_base()


class RpiOrder(Base):
    __tablename__ = 'rpi_order'

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    host = Column(String(50))
    username = Column(String(50))
    port = Column(Integer)
    from_port = Column(Integer)
    to_port = Column(Integer)
    polled_time = Column(Integer)
    passwd = Column(String(50))
    metric: Mapped["RpiMetric"] = relationship(back_populates="rpi_order",
                                               cascade="all, delete-orphan")



class RpiMetric(Base):
    __tablename__ = 'rpi_metric'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(ForeignKey("rpi_order.name",
                                                 ondelete='CASCADE',
                                                 onupdate='CASCADE'))
    rpi_order: Mapped["RpiOrder"] = relationship(back_populates="metric")
    uptime = Column(Integer)
    cpu_usage = Column(Integer)
    memory_usage = Column(Integer)
    disk_usage = Column(Integer)
    temperature = Column(Integer)


class Authentication(Base):
    __tablename__ = 'authentication'

    username = Column(String(100), primary_key=True)
    password = Column(String(100))
    salt = Column(String(100))

table_objects = [RpiOrder.__table__, Authentication.__table__, RpiMetric.__table__]

def init_db():
    global ENGINE
    ENGINE = create_engine("mysql+pymysql://{user}:{passwd}@{host}/{dbname}?charset=utf8mb4".format(
        user=environ.get("MYSQL_USER"),
        passwd=environ.get("MYSQL_PASSWORD"),
        host=environ.get("MYSQL_HOST"),
        dbname=environ.get("MYSQL_DATABASE")
    ))
    Base.metadata.create_all(ENGINE, tables=table_objects)


def get_session():
    ses = sessionmaker(bind=ENGINE)
    return ses()
