from flask import (Flask, render_template)

app = Flask(__name__)

if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'none'
    with app.app_context():
        print(render_template('index.html').replace('http://none', ''))
