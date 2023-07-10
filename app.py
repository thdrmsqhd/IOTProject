from flask import Flask, render_template
from flask_socketio import SocketIO
import camera
import plug
from models import db, FirePrevention

app = Flask(__name__)
app.config["SECRET_KEY"] = 'jihye'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///firePrevention.db"
socketio = SocketIO(app)
activeCamara = camera.Camara()
activePlug = plug.PlugService()
db.init_app(app)

with app.app_context():
    db.create_all()

socketio.start_background_task(activeCamara.streaming, socketio, app=app)


@app.route('/')
def index():
    datas = FirePrevention.query.all()
    return render_template('index.html', plugStat=activePlug.plugStatus(), datas=datas)


@socketio.on('capture')
def capture():
    activeCamara.sense = True
    socketio.emit('active', {'active': activeCamara.sense})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9090, debug=True, allow_unsafe_werkzeug=True )
