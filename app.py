from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import camera
import plug
from models import db, FirePrevention
import base64
import cv2

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
    datas = sorted(FirePrevention.query.all(), key=lambda x: x.id, reverse= True)[:10]
    result = list(
        map(
            lambda x: {
                "id":x.id, 
                "time": x.time.strftime('%Y-%m-%d %H:%M:%S'), 
                "picture_file": x.picture_file
                }
            , datas
            )
        )
    return render_template('index2.html', plugStat=activePlug.plugStatus(), datas=result)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9090, allow_unsafe_werkzeug=True )
