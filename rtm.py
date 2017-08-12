# coding: utf-8

import time

from slackclient import SlackClient

from config import SLACK_BOT_API_TOKEN, ORIGIN_CHANNEL_ID, TARGET_CHANNEL_NAME
from translate import translate

slack_token = SLACK_BOT_API_TOKEN
sc = SlackClient(slack_token)

if sc.rtm_connect():
    while True:
        rv = sc.rtm_read()
        print(rv)
        for event in rv:
            if event.get('type') == 'message' and event['channel'] == ORIGIN_CHANNEL_ID:
                text = event['text']
                print(text)
                sc.rtm_send_message(TARGET_CHANNEL_NAME, translate(text))
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
