from flask import Flask, render_template
from flask_socketio import SocketIO
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def send_numbers():
    num = 1
    while True:
        socketio.sleep(1)
        socketio.emit('number', {'num': num})
        num += 1

if __name__ == '__main__':
    socketio.start_background_task(send_numbers)
    socketio.run(app, debug=True)
