from flask import Flask, abort, jsonify, request, redirect
import json
from db import DB
import random, string, re

app = Flask(__name__)
db = DB()

@app.route('/', methods=['GET'])
def homepage() :
    return "Homepage"

@app.route('/', methods=['POST'])
def newURL():
    data = JSONStringer(request)

    code = ''.join(random.choices(string.ascii_uppercase 
                + string.digits, k=random.randint(2, 5)))

    result = db.search('urls', 'short_code', where="url = '{}'".format(data['url']))

    if not result :
        while db.add('urls', " '{}', '{}' ".format(code, data['url'])) :
            code = ''.join(random.choices(string.ascii_uppercase 
                    + string.digits, k=random.randint(2, 5)))
    else :
        code = result[0][0]
    return code

@app.route('/<url>', methods=['GET'])
def redirect_url(url=''):
    result = db.search('urls', 'url', where="short_code = '{}'".format(url))

    if result :
        if not re.search(r"(?:f|ht)(?:tp|tps):\/\/", result[0][0]) :
            return redirect("http://"+result[0][0], code=301)
        else :
            return redirect(result[0][0], code=301)
    else :
        return "404 Error", 404

def JSONStringer(req):
    try:
        data = json.loads(req.data, strict=False)
        return data
    except json.decoder.JSONDecodeError:
        return "Decoding Error"

if __name__ == '__main__':
    app.run(port=8001)