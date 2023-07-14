import cv2


cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3,640) # 너비
cap.set(4,480) # 높이

ret, frame = cap.read()
cv2.imwrite("file_name.jpg", frame)
    
cap.release()
cv2.destroyAllWindows()