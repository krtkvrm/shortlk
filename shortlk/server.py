from flask import (Flask, request, redirect, render_template)
import json
from db import DB
import random
import string
import requests
import os
import re

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def newURL():
    db = DB()

    print(request.data)

    data = JSONStringer(request)

    payload = "secret={0}&response={1}&remoteip={2}".format(
        os.environ.get('CAPTCHA_KEY_SERVER'),
        data['token'],
        request.remote_addr
    )
    res = json.loads(
        requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data=payload,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'}).text)
    print(res['success'])
    if str(res['success']) == 'False':
        return json.dumps({'error': 'reCaptcha Error!'})

    code = ''.join(random.choices(string.ascii_uppercase
                                  + string.digits, k=random.randint(2, 5)))
    print(data)
    result = db.search(
        'urls',
        'short_code',
        where="url = '{0}'".format(
            data['url']))

    if not result:
        while db.add('urls', " '{}', '{}' ".format(code, data['url'])):
            code = ''.join(
                random.choices(
                    string.ascii_uppercase +
                    string.digits,
                    k=random.randint(
                        2,
                        5)))
    else:
        code = result[0][0]

    res = {'code': code}
    return json.dumps(res)


@app.route('/<url>', methods=['GET'])
def redirect_url(url=''):
    db = DB()
    result = db.search('urls', 'url', where="short_code = '{}'".format(url))

    if result:
        if not re.search(r"(?:f|ht)(?:tp|tps):\/\/", result[0][0]):
            return redirect("http://" + result[0][0], code=301)
        else:
            return redirect(result[0][0], code=301)
    else:
        return "404 Error", 404


def JSONStringer(req):
    try:
        data = json.loads(req.data, strict=False)
        return data
    except json.decoder.JSONDecodeError:
        return "Decoding Error"


if __name__ == '__main__':
    app.debug = True
    app.run(port=8001, host='0.0.0.0')
