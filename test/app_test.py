from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format('root', '1234', 'localhost', 'hub_db'))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

Base.metadata.create_all(engine) # table 생성

#
from requests import get
import json
import threading
end = False
temp = 0
def get_temp(second=10):
    global end
    if end:
        return
    print('get_temp')
    global temp
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'T1H':
            # print('temp:'+str(i['obsrValue']))
            temp = i['obsrValue']
            # return i['obsrValue']
    threading.Timer(second, get_temp, [second]).start()
get_temp(10)
#

print('기상청 온도로 문 닫기')
while True:
    if (temp) < 18:
        print('모터 ON')
    else:
        print('모터 OFF')
