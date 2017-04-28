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
get_temp(1)
#
print('기상청 온도로 문 닫기')
while True:
    if (temp) < 18:
        print('모터 ON')
    else:
        print('모터 OFF')