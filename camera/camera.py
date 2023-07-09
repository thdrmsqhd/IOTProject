import numpy as np
import cv2
import time
from flask_socketio import SocketIO
import base64

cap = None

def setCap():
    global cap
    cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
    cap.set(3,640) # 너비
    cap.set(4,480) # 높이


def capture ():

    # cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
    cap.set(3,640) # 너비
    cap.set(4,480) # 높이

    ret, frame = cap.read() # 사진 촬영
    frame = cv2.flip(frame, 1) # 좌우 대칭

    cv2.imwrite('self camera test.jpg', frame) # 사진 저장

    return frame


def streaming(socektio: SocketIO):
    while True:
        _, frame = cap.read()
        
        # 프레임을 인코딩하여 JPEG 파일 형식으로 변환
        ret, buffer = cv2.imencode('.jpg', frame)

        # 이미지 데이터를 base64 문자열로 인코딩
        jpg_as_text = base64.b64encode(buffer)
        
        # 소켓으로 html에 화면을 전송한다.
        socektio.emit("streaming", {"frame": jpg_as_text})

        # if (객체감지) :
        #    capture()     
        #    AI_분석_함수()
        
        time.sleep(1)


def capRelease():
    cap.release()