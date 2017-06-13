from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, Enum
from config import *

from app import Base

class AppSetting(Base):
    __bind_key__ = app_db

    __tablename__ = 'app_setting'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, nullable=False )
    in_node = Column(Integer, nullable=False )
    in_sensor = Column(Integer, nullable=False )
    out_node = Column(Integer, nullable=False )
    out_sensor = Column(Integer, nullable=False )
    created_date = Column(
        String(100),
        default=str(datetime.datetime.utcnow()).split('.')[0],
    )

    def __init__(self, app_id, in_node, in_sensor, out_node, out_sensor):
        self.app_id = app_id
        self.in_node = in_node
        self.in_sensor = in_sensor
        self.out_node = out_node
        self.out_node = out_node
        self.out_sensor = out_sensor

    def __repr__(self):
        return "<app_setting('%s', '%s', '%s')>" % (self.id, self.app_id, self.in_node)