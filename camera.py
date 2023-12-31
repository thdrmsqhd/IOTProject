import numpy as np
import cv2
import time
from flask_socketio import SocketIO
import base64
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from models import db, FirePrevention
import plug

import tensorflow as tf
from tensorflow import keras
from keras.applications import imagenet_utils
import predict
import datetime

class Camara:
    cap = None
    sense = False
    resnet50_pre = None
    isOFF = False
    offTime = None
    restartTime = 5

    def __init__(self):
        self.setCap()
        self.resnet50_pre = tf.keras.applications.resnet.ResNet50(weights='imagenet', input_shape=(224,224,3))
        self.offTime = datetime.datetime.now()

    def setCap(self):
        self.cap = cv2.VideoCapture(0)  # 노트북 웹캠을 카메라로 사용
        self.cap.set(3, 320)  # 너비
        self.cap.set(4, 240)  # 높이
        pass

    def capture(self, jpg_as_text, app, socketio):
        # cv2.imwrite('self camera test.jpg', frame)  # 사진 저장
        fp = FirePrevention()
        fp.picture_file = jpg_as_text
        with app.app_context():
            db.session.add(fp)
            db.session.commit()
            datas = sorted(FirePrevention.query.all(), key=lambda x: x.id, reverse= True)[:10]

            # JSON으로 직렬화하여 반환하기
            serialized_data = []
            for data in datas:
                serialized_data.append({
                    'id': data.id,
                    'time': data.time.strftime('%Y-%m-%d %H:%M:%S'),
                    'picture_file': data.picture_file
                })

            socketio.emit("refreshData", {"datas": serialized_data})
            print("save file")
        pass

    def streaming(self, socketio: SocketIO, app):
        plugService = plug.PlugService()
        while True:
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)  # 좌우 대칭

            # 프레임을 인코딩하여 JPEG 파일 형식으로 변환
            try:
                _, buffer = cv2.imencode('.jpg', frame)

                # 이미지 데이터를 base64 문자열로 인코딩
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                # 소켓으로 html에 화면을 전송한다.
                socketio.emit("streaming", {"frame": jpg_as_text})
                # if self.sense is True:
                predictResult = predict.pred_img(resnet50_pre=self.resnet50_pre, img=frame, imagenet_utils=imagenet_utils)
                if predictResult:
                    print(predictResult)
                    self.capture(jpg_as_text, app, socketio)
                    plugService.plugOff()
                    self.isOFF = True
                    self.offTime = datetime.datetime.now()
                    socketio.emit("plugStatus", {"plugStatus": plugService.plugStatus()})
                
                if plugService.plugStatus() == "OFF":
                    print(datetime.datetime.now() - self.offTime)
                    delayTime = self.offTime + datetime.timedelta(seconds=self.restartTime)
                    if datetime.datetime.now() >= delayTime:
                        plugService.plugON()
                        # socketio.emit("plugStatus", {"plugStatus": plugService.plugStatus()})
                        
                
            except Exception as e:
                print(e)
                pass
