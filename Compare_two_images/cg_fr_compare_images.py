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
# Function for opening the 
# file explorer window 

is_src_img_selected = False
src_image = ''	

def matchimages(img1,img2):
    try:
      source_image = face_recognition.load_image_file(img1)
      source_image_encoded = face_recognition.face_encodings(source_image)[0]
    except:
        da = mb.showwarning ('Warning!','low light or blur image, please choose proper image' ,icon = 'warning')
        if da != 'ok':
            print('ok')
        else:
            return False
        label_file_explorer.configure(text = "Capgemini Face Recognition",fg='blue')
    
    try:
      current_image = face_recognition.load_image_file(img2)
      current_image_encoded = face_recognition.face_encodings(current_image)[0]
    except:
        da = mb.showwarning ('Warning!','low light or blur image, please choose proper image' ,icon = 'warning')
        if da != 'ok':
            print('ok')
        else:
            return False
        label_file_explorer.configure(text = "Capgemini Face Recognition",fg='blue')

    result = face_recognition.compare_faces(
          [source_image_encoded], current_image_encoded)
    if result[0] == True:
       label_file_explorer.configure(text="Matched",fg='green')
    else:
       label_file_explorer.configure(text="Not Matched",fg='red')

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
    image = image.resize((150, 150), Image.ANTIALIAS)
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
    image1 = image1.resize((150, 150), Image.ANTIALIAS)
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
window.bind('<Escape>', lambda e: mainWindow.quit())

#Set window background color 
window.config(background = "white") 

# Create a File Explorer label 
label_file_explorer = Label(window, 
							text = "Capgemini Face Recognition", 
							width = 50, height = 4, 
                            font=("Helvetica", 18),
							fg = "blue") 

frmMain = Frame(window,bg="white")
lmain_src = Label(frmMain, compound=CENTER, anchor=CENTER, relief=RAISED)
lmain_match = Label(frmMain, compound=CENTER, anchor=CENTER, relief=RAISED)
src_button_explore = Button(frmMain, 
						text = "Browse Source Image", 
						command = browseSrcFile) 
match_button_explore = Button(frmMain, 
						text = "Browse Tobe Match Image", 
						command = browseMatchFile) 
src_img_label = Label(frmMain, text = "Source Image", 
							width = 20, height = 2, 
							fg = "blue") 
match_img_label = Label(frmMain, text = "To be Match Image", 
							width = 20, height = 2, 
							fg = "blue") 


# Grid method is chosen for placing 
# the widgets at respective positions 
# in a table like structure by 
# specifying rows and columns 
label_file_explorer.grid(column = 1, row = 1) 
frmMain.grid(row =4,column = 1,padx=5, pady=5)
src_button_explore.grid(column = 1, row = 0) 
match_button_explore.grid(column = 2, row = 0)
src_img_label.grid(row = 1,column = 1,padx=10, pady=10)
match_img_label.grid(row = 1,column = 2,padx=10, pady=10)
lmain_src.grid(row = 2,column = 1,padx=10, pady=10)
lmain_match.grid(row = 2,column = 2,padx=10, pady=10)

# Let the window wait for any events 
window.mainloop() 
