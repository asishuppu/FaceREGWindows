import time
import numpy as np
import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from tkinter import messagebox as mb
import csv

global emp_id
global usr_name
cap = cv2.VideoCapture(0)

def createemp(id,name):
    with open(r'data/Emp_details.csv','a') as csvfile:
        newemp=id+","+name
        csvfile.write(newemp+"\n")


def detect_face(img):
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, 1.2, 5)

    if faces == ():
        return False
    else:
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

def take_pic(id,nm):
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    while(True):
        ret, frame = cap.read()
        faces = face_cascade.detectMultiScale(frame, 1.2, 5)
        if faces == ():
            mb.showwarning('Warning!','No face found')
            return False
        else:
            for (x, y, w, h) in faces:
                crop_img = frame
                cv2.imwrite("src_images/" + str(id)+".jpg", crop_img)
                createemp(id,nm)
                mainWindow.quit()
                return False

def save_img():
    sv_empid = emp_id.get()
    sv_name = usr_name.get()
    if(sv_empid != '' and sv_name != ''):
        if(os.path.isfile('src_images/'+ str(sv_empid) +".jpg")):
            mb.showwarning("Warning!", "Employee Alredy Registered.")
        else:
            take_pic(sv_empid,sv_name)
    else:
        mb.showwarning("Warning!", "Please Enter All fields")


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

frmMain = tk.Frame(mainWindow,bg="white")
frmMain.grid(row =1,column = 1,padx=20, pady=20)
# Definging the first row 
lblfrstrow = tk.Label(frmMain, text ="Empid -", )
lblfrstrow.grid(row = 0, column = 1,padx=10, pady=10 ) 
emp_id= tk.StringVar() 
empid = tk.Entry(frmMain,textvariable=emp_id, width = 35) 
empid.grid(row = 0, column = 2,padx=10, pady=10) 

   
lblsecrow = tk.Label(frmMain, text ="Name -") 
lblsecrow.grid(row = 1, column = 1,padx=10, pady=10 ) 
usr_name = tk.StringVar() 
name = tk.Entry(frmMain,textvariable=usr_name, width = 35) 
name.grid(row = 1, column = 2,padx=10, pady=10 ) 

submitbtn = tk.Button(frmMain, text ="Save Image",  
                      bg ='green',fg='white', command=save_img) 
submitbtn.grid(row=3,column=2,padx=10, pady=10)
show_frame()
mainWindow.title('Capgemini Face Recognition system')
# Title Bar Icon
mainWindow.iconbitmap('capg_icon.ico')
mainWindow.mainloop()