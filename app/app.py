# coding: utf-8

from flask import Flask, request, abort, jsonify, make_response
from slackclient import SlackClient

from config import SLACK_TOKEN, TEAM_ID, SLACK_BOT_API_TOKEN

from translate import translate as t
from irasutoya import get_random_irasutoya_attachments

sc = SlackClient(SLACK_BOT_API_TOKEN)

app = Flask(__name__)

@app.route('/translator/translate', methods=['POST'])
def translate():
    if not validate_request(request):
        abort(403)
    text = request.form.get('text')
    rv = t(text)
    return wrap_resp(rv)

@app.route('/translator/dialog', methods=['POST'])
def translate_dialog():
    if not validate_request(request):
        abort(403)
    trigger_id = request.form.get('trigger_id')
    user_id = request.form.get('user_id')
    open_dialog = sc.api_call('dialog.open', trigger_id=trigger_id, dialog=build_dialog(user_id))
    return ''

@app.route('/irasutoya/random', methods=['POST'])
def irasutoya_random():
    if not validate_request(request):
        abort(403)
    resp = {
        'response_type': 'in_channel',
        'attachments': get_random_irasutoya_attachments(),
        'icon_emoji': ':irasutoya:',
        'username': 'いらすとや'
    }
    return jsonify(resp)

def validate_request(request):
    token = request.form.get('token')
    team_id = request.form.get('team_id')
    if token and token == SLACK_TOKEN and team_id and team_id == TEAM_ID:
        return True
    return False

def wrap_resp(text):
    d = {
        'response_type': 'in_channel',
        'text': text
    }
    return jsonify(d)

def build_dialog(user_id):
    return {
        'title': '翻訳',
        'submit_label': '確認する',
        'callback_id': user_id + 'translation_form',
        'elements': [
            {
                'label': '原文',
                'name': 'source_text',
                'type': 'textarea',
                'placeholder': '天気がいいから散歩しましょう！',
                'max_length': 500,
            },
            {
                'label': '目標言語',
                'type': 'select',
                'name': 'language',
                'placeholder': '中国語',
                'value': 'zh-CN',
                'options': [
                    {
                        'label': '中国語',
                        'value': 'zh-CN',
                    },
                    {
                        'label': '日本語',
                        'value': 'ja'
                    },
                    {
                        'label': '英語',
                        'value': 'en'
                    }
                ]
            }
        ]
    }
