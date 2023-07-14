## IOT Project

# 고양이를 감지하면 전원을 차단하는 프로젝트 

```
 pip install -r requirements.txt

 python app.py
```

```
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
                        socketio.emit("plugStatus", {"plugStatus": plugService.plugStatus()})
                        
                
            except Exception as e:
                print(e)
                pass

```