from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    print(request.form['code'])
    print(request.form['id'])
    return 'OK'

if __name__ == '__main__':
    app.run()
