from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app import Base

class AppLog(Base):
    __tablename__ = 'app_log'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = Column(Integer, primary_key=True)
    log_time = Column(String(100), nullable=False )
    log_content = Column(String(100), nullable=False )

    app_id = Column(Integer, ForeignKey('app_model.id'))
    app_model = relationship('AppModel', foreign_keys=[app_id])

    def __init__(self, log_time, log_content, app_id):
        self.log_time = log_time
        self.log_content = log_content
        self.app_id = app_id

    def __repr__(self):
        return "<AppLog('%s', '%s', '%s')>" % (self.id, self.log_time, self.log_content)