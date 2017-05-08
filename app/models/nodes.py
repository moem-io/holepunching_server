from sqlalchemy import Column, Integer, String, Boolean, Enum

from app import Base

class Nodes(Base):
    node_status = ['healthy', 'warning', 'error']
    __tablename__ = 'Nodes'

    id = Column(Integer, primary_key=True)
    depth = Column(Integer, nullable=False, default=0)
    nodeNo = Column(Integer, nullable=False, default=0)
    addr = Column(String(12), nullable=False )
    status = Column(Enum(*node_status), nullable=False, default=node_status[0])
    isActive = Column(Boolean, default=True)

    def __init__(self, depth, nodeNo, addr, status, isActive):
        self.depth = depth
        self.nodeNo = nodeNo
        self.addr = addr
        self.status = status
        self.isActive = isActive

    def __repr__(self):
        return "<Nodes('%s', '%s', '%s')>" % (self.id, self.depth, self.nodeNo)