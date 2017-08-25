# coding: utf-8

import time

from slackclient import SlackClient

from config import SLACK_BOT_API_TOKEN, ORIGIN_CHANNEL_ID, TARGET_CHANNEL_NAME
from translate import translate

slack_token = SLACK_BOT_API_TOKEN
sc = SlackClient(slack_token)

def need_translate(text):
    text = text.strip()
    if text.startswith(':') and text.endswith(':'):
        return False
    return True

if sc.rtm_connect():
    while True:
        rv = sc.rtm_read()
        print(rv)
        for event in rv:
            if event.get('type') == 'message' and event['channel'] == ORIGIN_CHANNEL_ID:
                text = event.get('text')
                if not text:
                    continue
                if not need_translate(text):
                    continue
                print(text)
                sc.rtm_send_message(ORIGIN_CHANNEL_ID, translate(text), event['ts'])
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
