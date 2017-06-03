from sqlalchemy import Column, Integer, String, Boolean, Enum

from app import Base

class AppModel(Base):
    __tablename__ = 'app_model'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id = Column(Integer, primary_key=True)
    app_name = Column(String(100), nullable=False )
    app_detail = Column(String(100), nullable=False )
    app_switch = Column(Boolean, default=True)
    app_input = Column(String(100), nullable=False )
    app_input_detail = Column(String(100), nullable=False )
    app_output = Column(String(100), nullable=False )
    app_output_detail = Column(Boolean, default=True)

    def __init__(self, app_name, app_detail, app_switch, app_input, app_input_detail, app_output, app_output_detail):
        self.app_name = app_name
        self.app_detail = app_detail
        self.app_switch = app_switch
        self.app_input = app_input
        self.app_input_detail = app_input_detail
        self.app_output = app_output
        self.app_output_detail = app_output_detail

    def __repr__(self):
        return "<AppModel('%s', '%s', '%s')>" % (self.id, self.app_name, self.app_detail)