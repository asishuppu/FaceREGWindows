import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def Is_single_faces(imagepath):
    img = cv2.imread(imagepath) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if(len(faces) == 1):
      return True
    else:
      return False
      
      