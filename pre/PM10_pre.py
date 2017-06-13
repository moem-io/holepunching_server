# PM10FromSky
from requests import get
import json
import time

# 기상청 온도는 1시간 단위로 변함(30~40분 사이에 뜸)
# 대기 타다가 정각에 가져오는걸로 만들자
weatherFirst = True

def PM10FromSky():
    global weatherFirst
    global SW
    temp = 0
    if weatherFirst:
        weatherFirst = False
    else:
        time.sleep(10)
    if not SW:
        return 0
    res = get('https://api.moem.io/outside/mise')
    js = json.loads(res.text)
    temp = js['json_list'][0]['PM10']
    print('pm10 : ', temp)
    return temp