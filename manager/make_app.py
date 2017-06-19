from app.models.app_model import AppModel
from app import session
import json
from requests import post, get
from config import *
from sqlalchemy.ext.declarative import DeclarativeMeta
from app.models.app_setting import AppSetting

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
    temp = 20
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'T1H':
            temp = i['obsrValue']
    return temp
def getHumi():
    temp = 20
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'REH':
            temp = i['obsrValue']
    return temp
def getSKY():
    temp = None
    str = ''
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'SKY':
            temp = i['obsrValue']
    if temp == 1:
        str += '1(맑음)'
    elif temp == 2:
        str += '2(구름 조금)'
    elif temp == 3:
        str += '3(구름 많음)'
    elif temp == 4:
        str += '4(흐림)'
    return str
def getPTY():
    temp = None
    str = ''
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'PTY':
            temp = i['obsrValue']
    if temp == 0:
        str += '0(없음)'
    elif temp == 1:
        str += '1(비)'
    elif temp == 2:
        str += '2(비/눈)'
    elif temp == 3:
        str += '3(눈)'
    return str
def mise(cate):
    res = get('https://api.moem.io/outside/mise')
    js = json.loads(res.text)
    first = js['json_list'][0]
    return str(first[cate])

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

    # utf-8 setting
    pre = '#-*- coding: utf-8 -*-\n\n'

    app_input = ''
    input_detail = ''
    output = ''
    output_meta = ''
    output_detail = None

    log = None
    output_log = None
    # input
    if app_content.count('temperatureFromSky()'):
        pre += open('pre/temp_pre.py', 'r').read() + '\n\n'
        app_input += '기상청 온도 및 습도'
        input_detail = "[{'icon': 'sun icon', 'value': '온도 : " + str(
            getTemp()) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(getHumi()) + "%'}]"
        log = 'log_kind = '+'"기상청 온도"'
    elif app_content.count('humidityFromSky()'):
        pre += open('pre/humi_pre.py', 'r').read() + '\n\n'
        app_input += '기상청 온도 및 습도'
        input_detail = "[{'icon': 'sun icon', 'value': 온도 : '" + str(
            getTemp()) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(getHumi()) + "%'}]"
        log = 'log_kind = '+'"기상청 습도"'
    elif app_content.count('SKYFromSky()'):
        pre += open('pre/sky_pre.py', 'r').read() + '\n\n'
        app_input += '하늘 상태 및 강수 형태'
        input_detail = "[{'icon': 'sun icon', 'value': '하늘 : " + getSKY() + "'}, {'icon': 'umbrella  icon', 'value': '강수 : " + getPTY() + "'}]"
        log = 'log_kind = '+'"하늘 상태"'
    elif app_content.count('PTYFromSky()'):
        pre += open('pre/pty_pre.py', 'r').read() + '\n\n'
        app_input += '하늘 상태 및 강수 형태'
        input_detail = "[{'icon': 'sun icon', 'value': '하늘 : " + getSKY() + "'}, {'icon': 'umbrella  icon', 'value': '강수 : " + getPTY() + "'}]"
        log = 'log_kind = '+'"강수 형태"'

    elif app_content.count('PM10FromSky()'):
        pre += open('pre/PM10_pre.py', 'r').read() + '\n\n'
        app_input += '미세먼지(10㎛)'
        input_detail = "[{'icon': 'certificate icon', 'value': ' : " + mise('PM10') + "㎍/㎥'}]"
        log = 'log_kind = '+'"미세먼지"'
    elif app_content.count('PM25FromSky()'):
        pre += open('pre/PM25_pre.py', 'r').read() + '\n\n'
        app_input += '초미세먼지(2.5㎛)'
        log = 'log_kind = '+'"초미세먼지"'
        input_detail = "[{'icon': 'certificate icon', 'value': '" + mise('PM25') + "㎍/㎥'}]"
    elif app_content.count('O3FromSky()'):
        pre += open('pre/O3_pre.py', 'r').read() + '\n\n'
        app_input += '오존농도(ppm)'
        input_detail = "[{'icon': 'certificate icon', 'value': '" + mise('O3') + "ppm'}]"
        log = 'log_kind = ' + '"오존농도"'

    # sensor
    elif app_content.count('soilHumidity()'):
        pre += open('pre/soil_pre.py', 'r').read() + '\n\n'
        app_input += '토양 습도 센서'
        input_detail = "[{'icon': 'theme icon', 'value': '습도 : " + str(getTemp()) + "%'}]"
        log = 'log_kind = ' + '"토양습도"'
    elif app_content.count('illuminationSensing()'):
        pre += open('pre/illum_pre.py', 'r').read() + '\n\n'
        app_input += '조도 센서'
        input_detail = "[{'icon': 'sun icon', 'value': '조도 : " + str(getTemp()) + "lux'}]"
        log = 'log_kind = ' + '"조도"'
    elif app_content.count('temperatureFromSensor()'):
        pre += open('pre/temp_sensor_pre.py', 'r').read() + '\n\n'
        app_input += '온습도 센서'
        input_detail = "[{'icon': 'sun icon', 'value': '온도 : " + str(
            getTemp()) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(getHumi()) + "%'}]"
        log = 'log_kind = ' + '"센서 온도"'
    elif app_content.count('humidityFromSensor()'):
        pre += open('pre/humi_sensor_pre.py', 'r').read() + '\n\n'
        app_input += '온습도 센서'
        input_detail = "[{'icon': 'sun icon', 'value': '온도 : " + str(
            getTemp()) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(getHumi()) + "%'}]"
        log = 'log_kind = ' + '"센서 습도"'

    #
    elif app_content.count('recognizeHuman()'):
        pre += open('pre/recog_human_pre.py', 'r').read() + '\n\n'
        app_input += '사람 인식'
        input_detail = "[{'icon': 'add user icon', 'value': '사람" + '' + " 인식'}]"
        log = 'log_kind = ' + '"사람"'
    elif app_content.count('clapCount()'):
        pre += open('pre/clap_cnt_pre.py', 'r').read() + '\n\n'
        app_input += '박수 횟수'
        input_detail = "[{'icon': 'sign language icon', 'value': '횟수 : " + "1번'}, {'icon': 'bullseye icon', 'value': '세기 : " + str(getHumi()) + "%'}]"
        log = 'log_kind = ' + '"박수"'
    elif app_content.count('checkButtonCount()'):
        pre += open('pre/btn_cnt_pre.py', 'r').read() + '\n\n'
        app_input += '버튼 눌림 횟수'
        input_detail = "[{'icon': 'hand pointer icon', 'value': '횟수 : " + str(1) + "번'}]"
        log = 'log_kind = ' + '"버튼 눌림"'
    elif app_content.count('pressureDetect()'):
        pre += open('pre/pressure_pre.py', 'r').read() + '\n\n'
        app_input += '압력 감지'
        input_detail = "[{'icon': 'angle double down icon', 'value': '세기 : " + str(1) + "Pa'}]"
        log = 'log_kind = ' + '"압력"'

    # output
    if app_content.count('motorRun'):
        pre += open('pre/motor_pre.py', 'r').read() + '\n\n'
        output += '서보 모터'
        output_detail = '0'
        output_log = 'output_log_kind = ' + '"서보 모터"'
    elif app_content.count('remoteControl'):
        pre += open('pre/remote_pre.py', 'r').read() + '\n\n'
        output += '리모컨'
        output_detail = 'off'
        output_log = 'output_log_kind = ' + '"리모컨"'
    elif app_content.count('ledRun'):
        pre += open('pre/led_pre.py', 'r').read() + '\n\n'
        output += 'LED'
        output_detail = '000000'
        output_log = 'output_log_kind = ' + '"LED"'
    elif app_content.count('buzzerRun'):
        pre += open('pre/buzzer_pre.py', 'r').read() + '\n\n'
        output += '부저'
        output_detail = 'stop'
        output_log = 'output_log_kind = ' + '"부저"'

        # add db
        # db_app = session.query(AppModel).filter_by(app_name=app_title).first()
        # if db_app:
            # session.query(AppModel).filter_by(app_name=app_title).delete()

    app_id = app[3]
    session.add(AppModel(app_id, app_title, app_sub, app_switch, app_input, input_detail, output, output_detail))
    session.commit()

    # query = session.query(AppModel).order_by(AppModel.id.desc()).first()
    # print('query.id', query.id)

    session.add(AppSetting(app_id, 0, 0, 0, 0))
    session.commit()

    # final pre
    pre += log + '\n\n'
    pre += output_log + '\n\n'
    pre += 'rabbit_app_id = ' + str(app_id) + '\n\n'
    pre += open('pre/rabbit_pre.py', 'r').read() + '\n\n'

    # 앱 변형
    modi = pre + '\n' + app_content

    # 완료된 앱 저장
    f_modi = open('./app_user/' + str(app_id) + '.py', 'w')
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
