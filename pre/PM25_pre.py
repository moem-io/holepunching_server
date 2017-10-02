# PM25FromSky
from requests import get
import json
import time
from app import session
from app.models.app_setting import AppSetting
from app.models.app_log import AppLog
import datetime
from requests import post
from manager.make_app import AlchemyEncoder
from app.models.app_model import AppModel

# 기상청 온도는 1시간 단위로 변함(30~40분 사이에 뜸)
# 대기 타다가 정각에 가져오는걸로 만들자
weatherFirst = True

def PM25FromSky():
    global weatherFirst
    global SW
    global rabbit_app_id
    global log_kind
    global api_url
    temp = 0
    if weatherFirst:
        weatherFirst = False
    else:
        time.sleep(10)
    if not SW:
        return 0
    res = get(api_url+'outside/mise')
    js = json.loads(res.text)
    temp = js['json_list'][0]['PM25']

    # app_model save
    model = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
    model.app_input_detail = "[{'icon': 'certificate icon', 'value': '" + str(temp) + "㎍/㎥'}]"

    # log
    sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
    in_node = sett.in_node
    in_sensor = sett.in_sensor
    # content = 'App ' + str(rabbit_app_id) + ' : Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
    #           log_kind + ' ' + str(kind[2]) + ' 감지'
    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
              log_kind + ' ' + str(temp) + ' 감지'
    print(content)
    item = AppLog(content, rabbit_app_id, str(in_node), str(in_sensor),
                  str(datetime.datetime.utcnow()).split('.')[0])
    session.add(item)
    session.commit()
    c = session.query(AppLog).order_by('id').all()
    res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))

    return temp