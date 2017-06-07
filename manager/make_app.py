from app.models.app_model import AppModel
from app import session
import json
from requests import post
from config import *
from sqlalchemy.ext.declarative import DeclarativeMeta

from pre.temp_pre import *
from pre.humi_pre import *

api_url = API_URL


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

def getTemp():
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'T1H':
            temp = i['obsrValue']
    return temp

def getHumi():
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'REH':
            temp = i['obsrValue']
    return temp

def getAppModi(app_origin):
    # 가져온 정보
    app = app_origin.split(',')
    app_title = app[0]
    app_sub = app[1]
    # app_sub = app[2]

    app_content = app[2]
    # print('app_title', app_title)
    print('app_content', app_content)

    # 앱 제작 중
    app_switch = False

    # 만약 특정 변수가 발견되면 그 변수에 맞는거 가져옴
    pre = '#-*- coding: utf-8 -*-\n\n'

    app_input = ''
    input_detail = ''
    output = ''
    output_meta = ''
    output_detail = False

    # input
    if app_content.count('temperatureFromSky()'):
        pre += open('pre/temp_pre.py', 'r').read() + '\n\n'
        app_input += '기상청 온도 및 습도'
        input_detail = "[{'icon': 'sun icon', 'value': " + "'" + str(
            getTemp()) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(getHumi()) + "%'}]"

    elif app_content.count('humidityFromSky()'):
        pre += open('pre/humi_pre.py', 'r').read() + '\n\n'
        app_input += '기상청 온도 및 습도'
        input_detail = "[{'icon': 'sun icon', 'value': " + "'" + str(
            getTemp()) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(getHumi()) + "%'}]"

    # output
    if app_content.count('ledRun'):
        pre += open('pre/led_pre.py', 'r').read() + '\n\n'
        output += 'LED'
    elif app_content.count('motorRun'):
        pre += open('pre/motor_pre.py', 'r').read() + '\n\n'
        output += '서보 모터'

    # add db
    db_app = session.query(AppModel).filter_by(app_name=app_title).first()
    if db_app:
        session.query(AppModel).filter_by(app_name=app_title).delete()
    session.add(AppModel(app_title, app_sub, app_switch, app_input, input_detail, output, output_detail))
    session.commit()

    query = session.query(AppModel).order_by(AppModel.id.desc()).first()
    # print('query.id', query.id)

    # final pre
    pre += 'rabbit_app_id = ' + str(query.id) + '\n\n'
    pre += open('pre/rabbit_pre.py', 'r').read() + '\n\n'

    # 앱 변형
    modi = pre + '\n' + app_content

    # 완료된 앱 저장
    f_modi = open('./app_user/' + str(query.id) + '.py', 'w')
    f_modi.write(modi)
    f_modi.close()

    query = session.query(AppModel).all()
    # print('query', (query))
    c = query
    res = post(api_url + 'app/save', data=json.dumps(c, cls=AlchemyEncoder))

    session.close()
    return app_title



    # print(app_origin.count('temp')
    # if app_content.count('temperatureFromSky()'):
    #     pre += open('pre/temp_pre.py', 'r').read() + '\n\n'
    #     app_input += '기상청 온도'
    #     input_detail = "[{'icon': 'sun icon', 'value': '24°C'}]"
    # pre += open('pre/humi_pre.py', 'r').read() + '\n\n'
    # app_input += '기상청 온도 및 습도'
    # input_detail = "[{'icon': 'sun icon', 'value': '24°C'}, {'icon': 'theme icon', 'value': '습도 : 15%'}]"

    # input_detail = "[{'icon': 'angle double down icon', 'value': '24 Pa'}]"
    # input_detail = "[{'icon': 'sun icon', 'value': '24°C'}, {'icon': 'theme icon', 'value': '습도 : 15%'}]"
    # input_detail = "[{'icon': 'hand rock icon', 'value': '두 번'}, {'icon': 'bullseye icon', 'value': '세기 : 45%'}]"

    # 18도 이하일때..
    # if app_content.count('temperatureFromSky()'):
    #     pre += open('pre/temp_pre.py', 'r').read() + '\n\n'
    #     app_input += '기상청 온도'
    #
    #     fir_str = ''
    #     fir = app_content.find('temperatureFromSky') + len('temperatureFromSky()') + 3
    #     fir_in = 0
    #     for i in range(4):
    #         try:
    #             fir_str += app_content[fir]
    #             fir += 1
    #             fir_in = int(fir_str)
    #         except ValueError as e:
    #             print(e)
    #
    #     if app_content[app_content.find('temperatureFromSky') + len('temperatureFromSky()') + 1] == '>':
    #         in_str = '온도가 ' + str(fir_in) + '°C 이상일 때'
    #     else:
    #         in_str = '온도가 ' + str(fir_in) + '°C 이하일 때'
    #     input_detail += "[{'icon': 'sun icon', 'value': " + "'" + in_str + "'}]"
