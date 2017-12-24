# coding: utf-8

import random
import hashlib
import requests
import html.parser as htmlparser
parser = htmlparser.HTMLParser()

__all__ = ['translate']

# Imports the Google Cloud client library
from google.cloud import translate
from config import YOUDAO_APP_KEY, YOUDAO_SECRET_KEY

# Instantiates a client
google_client = translate.Client()


class Youdao:

    API_URL = 'https://openapi.youdao.com/api'

    def translate(self, text, target_language):
        query_data = {
            'q': text,
            'from': 'auto',
            'to': target_language,
            'appKey': YOUDAO_APP_KEY,
            'salt': str(random.randint(1, 65536))
        }
        sign = self.sign(query_data)
        query_data.update(sign=sign)
        r = requests.get(self.API_URL, params=query_data)
        return dict(translatedText=r.json()['translation'][0])

    @staticmethod
    def sign(query_data):
        tmp_str = (YOUDAO_APP_KEY + query_data['q'] + query_data['salt'] + YOUDAO_SECRET_KEY).encode('utf-8')
        return hashlib.md5(tmp_str).hexdigest()

youdao_client = Youdao()

def translate(text, target='en', source='google'):

    if source == 'youdao':
        client = youdao_client
        target = 'zh-CHS' if target in ('zh-CN', 'zh-TW') else target
    else:
        client = google_client

    # Translates some text into Russian
    translation = client.translate(text, target_language=target)

    result = translation['translatedText']
    return parser.unescape(result)

if __name__ == "__main__":
    text = '天気がいいから散歩しましょう！'
    target_text = translate(text)
    print(translate(text, 'zh-CN'))
    print(translate(text, 'en'))
    print(translate(text, 'zh-CN', 'youdao'))
    print(translate(text, 'en', 'youdao'))
