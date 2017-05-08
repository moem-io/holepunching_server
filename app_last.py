# weather_pre
from requests import get
import json
import threading
import time
# 기상청 온도는 1시간 단위로 변함(30~40분 사이에 뜸)
# 대기 타다가 정각에 가져오는걸로 만들자
weatherFirst = True
def temperatureFromSky():
    global weatherFirst
    temp = 0
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'T1H':
            # print('temp:'+str(i['obsrValue']))
            temp = i['obsrValue']
    if weatherFirst:
        weatherFirst = False
        return temp
    else:
        time.sleep(600)
        return temp


# motor_pre
import threading

motor_end = False


def get_motor(second=10):
    threading.Timer(second, get_motor, [second]).start()


get_motor(1)

# db
from app.models.nodes import Nodes
from app.models.sensor import Sensors
from app import session


# motor
def motorRun(angle=90):
    print('motor angle', angle)
    db = session.query(Sensors).all()
    print(db)

    # todo 모터의 번호를 설정디비에서 가저옴
    # todo 3번 모터의 값이 입력값과 같은지 확인
    # todo 만약 같지 않으면 래빗엠큐로 보내고, 디비에 저장하든말든 함
    # todo 같으면 아무것도 안함


print('기상청 온도로 문 닫기')
while True:
    if temperatureFromSky() < 18:
        motorRun(0)
    else:
        motorRun(180)
