#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import paho.mqtt.client as mqtt

from logging import getLogger, DEBUG, StreamHandler, Formatter
from irsender import IRSender

logger = getLogger(__name__)

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(
    Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


token = 'token_SZOaouh9ySKztCay'

noun_conv = {
    '照明': 'light',
    'ライト': 'light',
    'らいと': 'light',
    'しょうめい': 'light',
    'ショウメイ': 'light',
    '証明': 'light',
    '電気' : 'light',
}

def on_connect(client, userdata, flags, response_code):
    if(response_code == 0):
        logger.info('MQTT subscribe topic')
        client.subscribe('HomeController/light')
    else:
        logger.error('MQTT connect failed!reason:{}'.format(response_code))


def on_message(client, userdata, msg):
    if(msg.topic == 'HomeController/light'):
        emit_light(msg.payload.decode("utf-8"))
    else:
        logger.debug('unknown topic:{0}, payload:{1}'.format(
            msg.topic, str(msg.payload)))


def normalize_device(device):
    logger.debug('input device:[{0}]'.format(device))
    device = device.replace(' ', '')
    if(device.endswith('を')):
        device = device[:-1]
    if not device in set(noun_conv.values()):
        try:
            device = noun_conv[device]
        except:
            device = ''

    logger.debug('out device:[{0}]'.format(device))
    return device


def emit_light(msg):
    payload = json.loads(msg)
    data = payload['data'][0]

    if(data['home'] != 'room'):
        logger.info('unknown place:{}'.format(data['home']))
        return

    if(normalize_device(data['device']) != 'light'):
        logger.info('unknown device:{}'.format(data['device']))
        return

    command = 'light:{}'.format(data['action'])
    logger.info('send command:[{}]'.format(command))

    irsender.emit_cmd(command)


if __name__ == '__main__':
    token = os.getenv('BEEBOTTE_TOKEN')
    
    if(token == None):
        logger.fatal('cannot get beebotte token!')
        exit(-1)
    
    irsender = IRSender('localhost', 17, logger)
    irsender.load('./codes')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('token:{0}'.format(token))
    client.connect('api.beebotte.com', port=1883, keepalive=60)
    client.loop_forever()
