from paho.mqtt import client as mqtt_client
import random
import json
import time

#Correo
import smtplib
from email.mime.text import MIMEText

#Mensaje de CPU
import psutil

#Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "pruebatopico"
TOPIC_ALERT = "pruebatopico"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

#Envio a correo electronico
# Configurar los detalles del correo electrónico
remite = 'brunosapedro123@gmail.com'
destinatario = 'bnsampedro@uce.edu.ec'
asunto = 'Proyecto Arquitectura'

# Configurar los detalles del servidor SMTP
servidor_smtp = 'smtp.gmail.com'
puerto_smtp = 587
usuario_smtp = 'brunosapedro123@gmail.com'
contraseña_smtp = 'ynnnuuwgtzlbreze'

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    #print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
        publish(client,TOPIC_ALERT)               

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    #client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

#Enviar mensajes
def publish(client,TOPIC,msg): 
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)

# Definir la función para enviar el correo electrónico
def enviar_correo(run):
    # Crear el objeto de mensaje MIMEText
    mensaje = f'El resultado actual del contador es: {run}'
    msg = MIMEText(mensaje)
    msg['From'] = remite
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Establecer la conexión SMTP y enviar el correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(usuario_smtp, contraseña_smtp)
        smtp.send_message(msg)
        print('Correo electrónico enviado exitosamente')

#La parte del envio del correo y al mqtt

client = connect_mqtt()
def run():
    counter = 0
    while True:
        client.loop_start()
        time.sleep(5)
        if FLAG_CONNECTED:
            # Agregar el contador aquí
            counter += 1
            publish(client, TOPIC_ALERT, counter) 
            enviar_correo(counter)
        else:
            client.loop_stop()

if __name__ == '__main__':
    run()