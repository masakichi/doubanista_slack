# coding: utf-8

from flask import Flask, request, abort, jsonify

from config import SLACK_TOKEN, TEAM_ID

from translate import translate as t

app = Flask(__name__)

@app.route("/translator/translate", methods=['POST'])
def translate():
    if not validate_request(request):
        abort(403)
    text = request.form.get('text')
    rv = t(text)
    return wrap_resp(rv)

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
