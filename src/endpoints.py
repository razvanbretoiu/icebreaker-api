from flask import Flask
from flask_cors import CORS

app = Flask(__name__,)
CORS(app)


@app.route('/')
def ok():
    return 'Ok'


if __name__ == '__main__':
    app.run(port=8000)
