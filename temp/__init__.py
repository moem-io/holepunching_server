# motor_pre
# import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import *

engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(id_db, ps_db, host_db, name_db))
Base = declarative_base()
Session = sessionmaker(bind=engine)

from app.models import *

Base.metadata.create_all(engine) # table 생성
session = Session()

from app.models.nodes import Nodes
n = Nodes(1, 1, 'home', 'warning', True)
session.add(n)
session.commit()


from app.models.sensor import Sensors
s = Sensors(1, 'typeC', 'error', False, 1)
session.add(s)
session.commit()

# end = False
# def get_motor(second=10):
#
#     threading.Timer(second, get_motor, [second]).start()
# get_motor(1)

# print('all node', session.query(Nodes).all())

def motor(angle=90):
    print('motor angle', angle)

    #todo 모터의 번호를 설정디비에서 가저옴
    #todo 3번 모터의 값이 입력값과 같은지 확인
    #todo 만약 같지 않으면 래빗엠큐로 보내고, 디비에 저장하든말든 함
    #todo 같으면 아무것도 안함