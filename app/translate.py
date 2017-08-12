# coding: utf-8

import html.parser as htmlparser
parser = htmlparser.HTMLParser()

__all__ = ['translate']

# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

def translate(text, target='en'):

    # Translates some text into Russian
    translation = translate_client.translate(text, target_language=target)

    result = translation['translatedText']
    return parser.unescape(result)

if __name__ == "__main__":
    text = '天気がいいから散歩しましょう！'
    target_text = translate(text)
    print(target_text)
