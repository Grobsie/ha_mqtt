import time
import serial
from paho.mqtt import client as mqtt_client

broker = 'IP'
port = 1883
topic = "TOPIC"
#empty client should result in random ID
client_id = ""
username = 'USER'
password = 'PW'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def getTelegram():
    with serial.Serial() as ser:
        ser.baudrate = 115200
        ser.port = '/dev/ttyUSB0'
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.open()
        data = str(ser.read_until(expected=b'*m3', size=1900))
    print("running getTelegram")
    gas = float(data[-13:-4])
    elec_f1 = float(data[-817:-807])
    elec_f2 = float(data[-788:-778])
    terug_f1 = float(data[-759:-749])
    terug_f2 = float(data[-730:-720])
    global telegram 
    telegram = f"\u007b\u0022gas\u0022: {gas:.3f}, \u0022el_f1\u0022: {elec_f1:.3f}, \u0022el_f2\u0022: {elec_f2:.3f}, \u0022terug_f1\u0022: {terug_f1:.3f}, \u0022terug_f2\u0022: {terug_f2:.3f}\u007d"

def publish(client):
    while True:
        try:
            time.sleep(30)
            getTelegram()
            result = client.publish(topic, telegram)
            status = result[0]
            if status == 0:
                print(f"Send `{telegram}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
        except:
            pass
def run():
#    getTelegram()
    client = connect_mqtt()
    client.loop_start()
#    getTelegram()
    publish(client)

if __name__ == '__main__':
    run()

