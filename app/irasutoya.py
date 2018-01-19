# coding: utf-8

import time
import feedparser

from datetime import datetime, timedelta
from slackclient import SlackClient
from config import SLACK_BOT_API_TOKEN

slack_token = SLACK_BOT_API_TOKEN
sc = SlackClient(slack_token)

FEED_URL = 'http://www.irasutoya.com/feeds/posts/summary'
LAST_TIME_FILE_PATH = '/tmp/irasutoya_last_time'

def conv_struct_time(struct_time):
    return datetime.fromtimestamp(time.mktime(struct_time))

def get_image_url(entry):
    return entry.media_thumbnail[0]['url'].replace('s72-c', 's400')

def get_last_time():
    try:
        with open(LAST_TIME_FILE_PATH) as f:
            timestamp = float(f.read().strip())
            return datetime.fromtimestamp(timestamp)
    except:
        return datetime.fromtimestamp(time.mktime(time.gmtime()))

def set_last_time():
    with open(LAST_TIME_FILE_PATH, 'w') as f:
        f.write(str(time.mktime(time.gmtime())))

def get_latest_items(last_time):
    last_time = last_time
    feed = feedparser.parse(FEED_URL)
    if last_time > conv_struct_time(feed.updated_parsed):
        return []
    entries = [e for e in feed.entries if conv_struct_time(e.updated_parsed) > last_time]
    return [{'title': e.title, 'image': get_image_url(e), 'url': e.link} for e in entries if len(e.media_thumbnail)]

def cronjob():
    last_time = get_last_time()
    set_last_time()
    items = get_latest_items(last_time)
    for item in items:
        text = '\n'.join([item['title'], item['image'], item['url']])
        sc.api_call(
            'chat.postMessage',
            channel='いらすとや',
            text=text,
            icon_emoji=':irasutoya:',
            username='いらすとや'
        )
        time.sleep(1)


if __name__ == '__main__':
    cronjob()
