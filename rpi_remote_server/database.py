# pylint: disable=global-statement

from os import path
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
    port = Column(Integer)
    polled_time = Column(Integer)
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

    username = Column(String(50), primary_key=True)
    password = Column(String(50))
    salt = Column(String(50))


table_objects = [RpiOrder.__table__, Authentication.__table__, RpiMetric.__table__]


def init_db():
    global ENGINE
    db_path = path.abspath(path.join(path.dirname(__file__), path.pardir, "data/database.db"))
    ENGINE = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(ENGINE, tables=table_objects)


def get_session():
    ses = sessionmaker(bind=ENGINE)
    return ses()
