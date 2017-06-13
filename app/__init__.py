from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import *

engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8'.format(id_db, ps_db, host_db, app_db))
Base = declarative_base()
Session = sessionmaker(bind=engine)

from app.models import *

Base.metadata.create_all(engine) # table 생성
session = Session()

# from app.models.nodes import Nodes
# n = Nodes(1, 1, 'home', 'warning', True)
# session.add(n)
# session.commit()
# from app.models.sensor import Sensors
# s = Sensors(1, 'typeC', 'error', False, 1)
# session.add(s)
# session.commit()