# coding: utf-8

import time

from slackclient import SlackClient

from config import SLACK_BOT_API_TOKEN, ORIGIN_CHANNEL_ID, TARGET_CHANNEL_NAME
from translate import translate

slack_token = SLACK_BOT_API_TOKEN
sc = SlackClient(slack_token)


FLAG_LANG_MAP = {
    'cn': 'zh-CN',
    'tw': 'zh-TW',
    'jp': 'ja',
    'us': 'en',
    'gb': 'en',
    'fr': 'fr',
    'de': 'de',
    'es': 'es',
}

TRANSLATED_POOL = set()

def has_translated(channel, ts, lang):
    key = '{}/{}/{}'.format(channel, ts, lang)
    if key in TRANSLATED_POOL:
        return True
    return False

def need_translate(text):
    text = text.strip()
    if text.startswith(':') and text.endswith(':'):
        return False
    return True


def retrieve_msg_by_ts(channel, ts):
    rv = sc.api_call(
        'channels.history',
        channel=channel,
        latest=ts,
        inclusive=True,
        count=1,
    )
    if rv.get('ok'):
        msgs = rv.get('messages')
        if msgs:
            return msgs[0]


def handle_flag_reaction(event):
    e_type = event.get('type')
    if e_type and e_type == 'reaction_added':
        reaction = event.get('reaction')
        #XXX(Gimo): Slack が勝手に国旗コードをチャージられる。
        if not reaction.startswith('flag-') or reaction not in FLAG_LANG_MAP.keys():
            return
        item = event.get('item')
        if not item or item.get('type') != 'message':
            return
        if reaction in FLAG_LANG_MAP.keys():
            flag = reaction
        else:
            flag = reaction[5:]
        target_lang = FLAG_LANG_MAP.get(flag, 'en')
        channel = item.get('channel')
        ts = item.get('ts')
        if has_translated(channel, ts, target_lang):
            return
        # TODO(Gimo): can be stored locally maybe.
        msg = retrieve_msg_by_ts(channel, ts)
        print(msg)
        if msg:
            text = msg.get('text', '')
            if text and need_translate(text):
                source = 'youdao' if target_lang in ('ja', 'zh-CN') else 'google'
                resp_text = translate(text, target_lang, source)
                sc.api_call(
                    'chat.postMessage',
                    channel=channel,
                    text=resp_text,
                    icon_emoji=':{}:'.format(reaction),
                    thread_ts=ts,
                    username='polyglot'
                )
                TRANSLATED_POOL.add('{}/{}/{}'.format(channel, ts, target_lang))

if sc.rtm_connect():
    while True:
        rv = sc.rtm_read()
        for event in rv:
            print(event)
            handle_flag_reaction(event)
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
