from flask import Flask, render_template
from flask_socketio import SocketIO, emit,send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event')
def handleMessage(msg):
    print(msg)
    emit("response", broadcast=True)


if __name__ == '__main__':
    socketio.run(app, port=2000)
