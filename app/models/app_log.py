from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app import Base
from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text

from config import *

class AppLog(Base):
    __bind_key__ = app_db

    __tablename__ = 'app_log'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = Column(Integer, primary_key=True)
    log_content = Column(String(100), nullable=False)
    app_id = Column(Integer, nullable=False)
    node = Column(String(100), nullable=False)
    sensor = Column(String(100), nullable=False)

    created_date = Column(
        String(100), nullable=False,
    )

    def __init__(self, log_content, app_id, node, sensor, created_date):
        self.log_content = log_content
        self.app_id = app_id
        self.node = node
        self.sensor = sensor
        self.created_date = created_date

    def __repr__(self):
        return "<AppLog('%s', '%s')>" % (self.id, self.log_content)