
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return '首页'

@app.route('/1', methods=['GET'])
def index1():
    return '1'


@app.route('/2', methods=['GET'])
def index2():
    return '2'


@app.route('/3', methods=['GET'])
def index3():
    return '3'


@app.route('/4', methods=['GET'])
def index4():
    return '4'

@app.route('/5', methods=['GET'])
def index5():
    return '5'

@app.route('/6', methods=['GET'])
def index6():
    return '6'

@app.route('/7', methods=['GET'])
def index7():
    return '7'

@app.route('/8', methods=['GET'])
def index8():
    return '8'

@app.route('/9', methods=['GET'])
def index9():
    return '9'


if __name__ == '__main__':
        
    app.run('127.0.0.1', port=5000)
