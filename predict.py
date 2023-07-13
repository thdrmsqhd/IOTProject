import cv2

def pred_img(resnet50_pre, img, imagenet_utils):

  img_resized = cv2.resize(img, (224,224))
  pred = resnet50_pre.predict(img_resized.reshape([1,224,224,3]))
  decoded_pred = imagenet_utils.decode_predictions(pred)

  predictions = list(map(lambda x: {"type": x[1],"per":"{:.2f}%".format(x[2]*100)},list(decoded_pred[0])))

  cat_predictions = [prediction for prediction in predictions if 'cat' in prediction['type']]

  if cat_predictions:
      highest_per = max(cat_predictions, key=lambda x: float(x['per'][:-1]))
      print("type에 'cat'이 포함되고 per의 수치가 가장 높은 예측값:", highest_per)
      return True
  else:
      print("type에 'cat'이 포함된 예측값이 없습니다.")
      return False