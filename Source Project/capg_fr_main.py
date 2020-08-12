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


global emp_id
global usr_name
cap = cv2.VideoCapture(0)

def reademp(id):
    name = 'unknown'
    with open('data/Emp_details.csv') as csvfile:
       readCSV = csv.reader(csvfile, delimiter=',')
       for row in readCSV:
        if row[0]==id:
            name=row[1]
    return name

def detect_face(frame):
    images = os.listdir('src_images')
    known_face_encodings = []
    known_face_names = []

    for image in images:
        current_image = face_recognition.load_image_file("src_images/" + image)
        current_image_encoded = face_recognition.face_encodings(current_image)[0]
        known_face_encodings.append(current_image_encoded)
        name = reademp(str(image).replace('.jpg',''))
        known_face_names.append(name)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        frame = cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        frame = cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


def register():
    os.startfile("capg_fr_reg.exe")
    mainWindow.quit()

def show_frame():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detect_face(rgb)
    prevImg = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
mainWindow = tk.Tk(screenName="Capgemini Face Recognition")
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
lmain.grid(row = 0,column = 1,padx=20, pady=20)

submitbtn = tk.Button(mainWindow, text ="Register",  
                      bg ='green',fg='white', command=register) 
submitbtn.grid(row=1,column=1,padx=10, pady=10)
show_frame()
mainWindow.title('Capgemini Face Recognition system')
# Title Bar Icon
mainWindow.iconbitmap('capg_icon.ico')
mainWindow.mainloop()