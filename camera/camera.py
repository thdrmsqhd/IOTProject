import numpy as np
import cv2
import time
from flask_socketio import SocketIO
import base64


class Camara:
    
    cap = None
    sense = False

    def __init__(self):
        self.setCap()
    
    def setCap(self):
        # self.cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
        # self.cap.set(3,320) # 너비
        # self.cap.set(4,240) # 높이
        pass
    
    def capRelease(self):
        # self.cap.release()
        pass

    def capture (self, frame):

        # cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
        # self.cap.set(3,640) # 너비
        # self.cap.set(4,480) # 높이

        # ret, frame = self.cap.read() # 사진 촬영
        # frame = cv2.flip(frame, 1) # 좌우 대칭

        # cv2.imwrite('self camera test.jpg', frame) # 사진 저장

        # return frame
        pass


    def streaming(self, socektio: SocketIO):
        while True:
            # _, frame = self.cap.read()
            # frame = cv2.flip(frame, 1) # 좌우 대칭

            # 프레임을 인코딩하여 JPEG 파일 형식으로 변환
            # _, buffer = cv2.imencode('.jpg', frame)
            
            # 이미지 데이터를 base64 문자열로 인코딩
            # jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            # 소켓으로 html에 화면을 전송한다.
            # socektio.emit("streaming", {"frame": jpg_as_text})
            print(self.sense)
            if (self.sense is True) :
                print("it work")
                # self.capture(frame)  
                self.sense = False   
            #    AI_분석_함수()

