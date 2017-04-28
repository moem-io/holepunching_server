
f_origin = open('app_test.txt', 'r')

# while True:
#     line = f.readline()
#     if not line: break
#     print(line)

app_origin = f_origin.read()
print(app_origin)

# 만약 특정 변수가 발견되면 그 변수에 맞는거 가져옴
pre = None
# print(app_origin.count('temp')
if app_origin.count('temp'):
    pre = open('weather_pre.py', 'r').read()
    # location = app_origin.find('temp')
    # print(location)

# 앱 변형
modi = app_origin
if pre:
    modi = pre+'\n'+app_origin


# 완료된 앱
f_modi = open('app_last.py', 'w')
f_modi.write(modi)

f_origin.close()
f_modi.close()
