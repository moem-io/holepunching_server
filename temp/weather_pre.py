# weather_pre
from requests import get
import json
import threading
weather_end = False
temp = 0
def get_temp(second=10):
    global weather_end
    if weather_end:
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