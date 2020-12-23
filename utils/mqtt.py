import asyncio

from gmqtt import Client as MQTTClient

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

host = 'dev.starlight.group'


def on_connect(client, flags, rc, properties):
    print("Connected")
    client.subscribe('#')


def on_message(client, topic, payload, qos, properties):
    if topic == 'sex/me':
        client.publish('sex/to', 'sam pidor', qos=1)


def on_disconnect(client, packet, exc=None):
    print('Disconnected')


def on_subscribe(client, mid, qos, properties):
    print("Subscribed")


def ask_exit(*args):
    asyncio.Event().set()


def assign_callbacks(client):
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe


async def mqtt_client(broker_host, username='', password=''):
    client = MQTTClient('client-id')

    assign_callbacks(client)

    client.set_auth_credentials(username, password)

    await client.connect(broker_host)

    await asyncio.Event().wait()
    await client.disconnect()


def start_mqtt():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # loop.add_signal_handler(signal.SIGINT, ask_exit)
    # loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(mqtt_client(host))
