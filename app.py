from flask import Flask, render_template
from flask_socketio import SocketIO
from camera import camera

app = Flask(__name__)
app.config["SECRET_KEY"] = 'jihye'
socketio = SocketIO(app)


# 서버가 올라오면서 스레드로 카메라 감시 기능을 켠다.
# socketio.start_background_task(camera.streaming, socketio)


# @socketio.on('disconnect')
# def disconnSocket():
#     camera.capRelease()


@app.route('/')
def index():
    activeCamara = camera.Camara()
    socketio.start_background_task(activeCamara.streaming, socketio)
    return render_template('index.html')


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', debug=True)
    socketio.run(app, host='0.0.0.0', port=9090, debug=True)
