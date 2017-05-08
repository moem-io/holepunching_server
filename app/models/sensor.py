from sqlalchemy import Column, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app import Base


class Sensors(Base):
    sensor_type = ['typeA', 'typeB', 'typeC']
    sensor_status = ['healthy', 'warning', 'error']
    __tablename__ = 'Sensors'

    id = Column(Integer, primary_key=True)
    sensorNo = Column(Integer, nullable=False, default=0)
    type = Column(Enum(*sensor_type), nullable=False)
    status = Column(Enum(*sensor_status), nullable=False, default=sensor_status[0])
    isActive = Column(Boolean, default=True)
    nodeId = Column(Integer, ForeignKey('Nodes.id'))
    node = relationship('Nodes', foreign_keys=[nodeId])

    def __init__(self, sensorNo, type, status, isActive, nodeId):
        self.sensorNo = sensorNo
        self.type = type
        self.status = status
        self.isActive = isActive
        self.nodeId = nodeId

    def __repr__(self):
        return "<Sensors('%s', '%s', '%s')>" % (self.id, self.sensorNo, self.status)

