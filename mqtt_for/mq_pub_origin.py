import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")      # MQTT Client 오브젝트 생성
# mqttc.connect("test.mosquitto.org", 1883)    # MQTT 서버에 연결
mqttc.connect("13.124.19.161", 1883)    # MQTT 서버에 연결
mqttc.publish("hello/world", "123")  # 'hello/world' 토픽에 "Hello World!"라는 메시지 발행
mqttc.loop(2)