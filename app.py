from flask import Flask, render_template
from flask_socketio import SocketIO
from camera import camera
import plug

app = Flask(__name__)
app.config["SECRET_KEY"] = 'jihye'
socketio = SocketIO(app)
activeCamara = camera.Camara()
activePlug = plug.PlugService()

@app.route('/')
def index():
    socketio.start_background_task(activeCamara.streaming, socketio)
    return render_template('index.html', plugStat = activePlug.plugStatus())

@socketio.on('capture')
def capture():
    activeCamara.sense = True
    socketio.emit('active', {'active': activeCamara.sense})
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9090, debug=True)
