from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()


class Device(Base):
    __tablename__ = 'devices'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    dev_id = Column(String(200), nullable=False)
    dev_type = Column(String(120), nullable=False)


class EndPoints(Base):
    __tablename__ = 'endpoints'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    device_id = Column(Integer, ForeignKey(Device.id, ondelete='CASCADE', onupdate='CASCADE'))
    comment = Column(Text)
