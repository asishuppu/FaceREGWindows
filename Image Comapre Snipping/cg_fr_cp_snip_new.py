# Python program to create 
# a file explorer in Tkinter 

# import all components 
# from the tkinter library 
from tkinter import *
from tkinter import messagebox as mb
# import filedialog module 
from tkinter import filedialog 
import cv2
from PIL import Image, ImageTk
import sys
import face_recognition
import dlib
import importlib
import snip as sn
import os
#import SnippingTool

# Function for opening the 
# file explorer window 

is_src_img_selected = False
src_image = ''	
image_resize_width = 420
image_resize_height = 350

def matchimages(img1,img2):
    try:
      source_image = face_recognition.load_image_file(img1)
      source_image_encoded = face_recognition.face_encodings(source_image)[0]
    except:
        da = mb.showwarning ('Warning!','Bad Image, please choose proper image' ,icon = 'warning')
        if da != 'ok':
            print('ok')
        else:
            return False
        label_file_explorer.configure(text = "Capgemini Face Recognition",fg='blue')
    
    try:
      current_image = face_recognition.load_image_file(img2)
      current_image_encoded = face_recognition.face_encodings(current_image)[0]
    except:
        da = mb.showwarning ('Warning!','Bad Image, please choose proper image' ,icon = 'warning')
        if da != 'ok':
            print('ok')
        else:
            return False
        label_file_explorer.configure(text = "Capgemini Face Recognition",fg='blue')

    result = face_recognition.compare_faces(
          [source_image_encoded], current_image_encoded,0.5)
    if result[0] == True:
       label_file_explorer.configure(text="Matched",fg='green')
    else:
       label_file_explorer.configure(text="Not Matched",fg='red')

def snipsrc():
    print(window.state)
    window.iconify()
    src_filename = 'temp_images/source.jpg'
    sn.Capture(src_filename)
    #os.system(r'snipping_tool.exe source.jpg')
    image = Image.open(src_filename)
    # The (450, 350) is (height, width)
    image = image.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=image)
    lmain_src.imgtk = imgtk
    lmain_src.configure(image=imgtk)
    global is_src_img_selected
    is_src_img_selected = True
    global src_image
    src_image = src_filename
    window.deiconify()

def snipmatch():
    print(window.state)
    if (not is_src_img_selected):
       mb.showwarning('Warning','Please Select Source Image First')
       return False
    match_filename = 'temp_images/match.jpg'
    window.iconify()
    #os.system(r'snipping_tool.exe match.jpg')
    #window.state('zoomed')
    sn.Capture(match_filename)
    if(match_filename == ''):
        mb.showwarning('Warning','No To be Match Image Selected')
        return False
	# Change label contents 
    label_file_explorer.configure(text="Please Wait....",fg="blue")
    image1 = Image.open(match_filename)
    # The (450, 350) is (height, width)
    image1 = image1.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk1 = ImageTk.PhotoImage(image=image1)
    lmain_match.imgtk = imgtk1
    lmain_match.configure(image=imgtk1)
    matchimages(src_image,match_filename)
    window.deiconify()

def browseSrcFile(): 
    
    src_filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a image",
										filetypes = (("Image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                        "*.*")))
	# Change label contents 
    if(src_filename == ''):
        mb.showwarning('Warning','No Source Image Selected')
        return False
    
    label_file_explorer.configure(text="Please Select To be Match Image")
    image = Image.open(src_filename)
    # The (450, 350) is (height, width)
    image = image.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=image)
    lmain_src.imgtk = imgtk
    lmain_src.configure(image=imgtk)
    global is_src_img_selected
    is_src_img_selected = True
    global src_image
    src_image = src_filename
    print('Slected')

def browseMatchFile():
    if (not is_src_img_selected):
       mb.showwarning('Warning','Please Select Source Image First')
       return False
    match_filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a image",
										filetypes = (("Image files", 
                                                        "*.jpg*"), 
                                                       ("all files", 
                                                        "*.*")))
    if(match_filename == ''):
        mb.showwarning('Warning','No To be Match Image Selected')
        return False
	# Change label contents 
    label_file_explorer.configure(text="Please Wait....",fg="blue")
    image1 = Image.open(match_filename)
    # The (450, 350) is (height, width)
    image1 = image1.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk1 = ImageTk.PhotoImage(image=image1)
    lmain_match.imgtk = imgtk1
    lmain_match.configure(image=imgtk1)
    matchimages(src_image,match_filename)
	
																							
# Create the root window 
window = Tk() 

# Set window title 
window.title('CapGemini Face Recognition') 

# Set window size 

window.resizable(width=False, height=False)
window.geometry('850x500')
window.bind('<Escape>', lambda e: mainWindow.quit())

#Set window background color 
window.config(background="white") 

# Create a File Explorer label 
label_file_explorer = Label(window, background = 'white',
							text = "Capgemini Face Recognition", 
							width = 60, height = 3, 
                            font=("Helvetica", 18),
                            highlightbackground='#0070ad',
							fg = "#0070ad") 

frmMain = Frame(window,bg="white",width = 60, height = 2, )
frmimg = Frame(window,bg="white")
lmain_src = Label(frmimg, compound=CENTER, anchor=CENTER, relief=RAISED)
lmain_match = Label(frmimg, compound=CENTER, anchor=CENTER, relief=RAISED)
b_icon = Image.open("res/browse.png")
b_icon = b_icon.resize((20, 20), Image.ANTIALIAS)
brouse_image = ImageTk.PhotoImage(image=b_icon)
s_icon = Image.open("res/snip.png")
s_icon = s_icon.resize((20, 20), Image.ANTIALIAS)
snip_image = ImageTk.PhotoImage(image=s_icon)
src_button_explore = Button(frmMain, 
						text = "Browse Source Image", justify=LEFT,image=brouse_image, compound="left",
                        borderwidth=0,
                        fg='white',bg = '#0070ad',
						command = browseSrcFile) 
match_button_explore = Button(frmMain, 
						text = "Browse Tobe Match Image", justify=LEFT,
                        image=brouse_image, compound="left",
                        borderwidth=0,
                        fg='white',bg = '#0070ad',
						command = browseMatchFile) 
src_button_grab = Button(frmMain, 
						text = "Snip Source Image", justify=LEFT,
                        image=snip_image, compound="left",
                        borderwidth=0,
                        fg='white',bg = '#0070ad',
						command = snipsrc) 
match_button_grab = Button(frmMain, 
						text = "Snip Tobe Match Image",justify=LEFT, 
                        image=snip_image, compound="left",
                        borderwidth=0,
                        fg='white',bg = '#0070ad',
						command = snipmatch) 
# src_img_label = Label(frmMain, text = "Source Image", 
# 							width = 20, height = 2, 
# 							fg = "blue") 
# match_img_label = Label(frmMain, text = "To be Match Image", 
# 							width = 20, height = 2, 
# 							fg = "blue") 


# Grid method is chosen for placing 
# the widgets at respective positions 
# in a table like structure by 
# specifying rows and columns 
label_file_explorer.grid(column = 0, row = 0) 
frmMain.grid(row =1,column = 0, pady=5)
frmimg.grid(row =2,column = 0,pady=10)
src_button_explore.grid(column = 0, row = 0,padx=5,) 
match_button_explore.grid(column = 1, row = 0,padx=5)
src_button_grab.grid(column = 2, row = 0,padx=5) 
match_button_grab.grid(column = 3, row = 0,padx=5)
lmain_src.grid(row = 0,column = 0)
lmain_match.grid(row = 0,column = 1)

# Let the window wait for any events 
window.mainloop() 
