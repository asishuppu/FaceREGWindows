import time
import numpy as np
import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from tkinter import messagebox as mb
import face_recognition
import dlib
import csv
import sys

def getUser():
    name = 'unknown'
    images = os.listdir('src_images')
    if(images):
        name = str(images[0]).replace('.jpg','')
    else:
        tk.Tk().withdraw()
        mb.showwarning('Alert!','Please Register to run recognition' ,icon = 'warning')
        sys.exit()
    return name

global emp_id
global usr_name
tk.Tk().withdraw()
user = getUser()
da = mb.showwarning('Alert!','This machine belongs to '+user+', please identifiy yourself' ,icon = 'warning')
print(da)
if da != 'ok':
    print('quit')
    sys.exit()

def Show_img():
    img = cv2.imread('temp_images/temp.jpg')
    screen_res = 600, 400
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    cv2.namedWindow('Capgemini Face Recognition', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Capgemini Face Recognition', window_width, window_height)
    cv2.imshow('Capgemini Face Recognition', img)

def Compare_face():
    images = os.listdir('src_images')
    source_image = face_recognition.load_image_file("src_images/"+images[0])
    source_image_encoded = face_recognition.face_encodings(source_image)[0]
    try:
      current_image = face_recognition.load_image_file("temp_images/temp.jpg")
      current_image_encoded = face_recognition.face_encodings(current_image)[0]
    except:
        tk.Tk().withdraw()
        da = mb.showwarning ('Warning!','low light or blur image, please capture proper image' ,icon = 'warning')
        if da != 'ok':
            print('quit')
            sys.exit()
        else:
            return False

    result = face_recognition.compare_faces(
          [source_image_encoded], current_image_encoded)
    r = 'Sorry! unable to recognise you as '+ user + ', you can not continue to use this machine.'
    if result[0] == True:
        r = 'You are identitfied as '+ user + ', you can contiune.'
    tk.Tk().withdraw()
    da = mb.showinfo('Output!',r)
    if da != 'ok':
        cv2.destroyAllWindows()
        sys.exit()
    else:
        cv2.destroyAllWindows()
        sys.exit()

def take_pic():
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    while(True):
        ret, frame = cap.read()
        faces = face_cascade.detectMultiScale(frame, 1.2, 5)
        if faces == ():
            tk.Tk().withdraw()
            da = mb.showwarning ('Warning!','No face found, please face the camera and click ok' ,icon = 'warning')
            if da != 'ok':
               print('quit')
               sys.exit()
               return False
            else:
               take_pic()
               return False
               
        else:
            for (x, y, w, h) in faces:
                crop_img = frame
                cv2.imwrite("temp_images/temp.jpg", crop_img)
                Show_img()
                cap.release()
                Compare_face()
                return False

cap = cv2.VideoCapture(0)
take_pic()
