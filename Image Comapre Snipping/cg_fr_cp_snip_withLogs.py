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
import datetime
import shutil

#import SnippingTool

# Function for opening the 
# file explorer window 

is_src_img_selected = False
src_image = ''	
image_resize_width = 420
image_resize_height = 350


def setup():
    if(not os.path.isdir('Logs')):
        os.mkdir('Logs')
    if(not os.path.isdir('temp_images')):
        os.mkdir('temp_images')

def copyImages(folder_name,timestamp):
    if(not os.path.isdir('Logs/'+folder_name+'/'+timestamp)):
        os.mkdir('Logs/'+folder_name+'/'+timestamp)
    target = r'Logs/'+folder_name+'/'+timestamp
    shutil.copyfile(src, target+'/source.jpg')
    Log("Copy Images -> Source Images Copied",False)
    shutil.copyfile(trg, target+'/target.jpg')
    Log("Copy Images -> Target Images Copied",False)

def Log(Msg,isRes):
    folder_name = datetime.datetime.today().strftime('%d-%m-%Y')
    log_filename = folder_name+'.txt'
    timestamp = datetime.datetime.today().strftime('%Y-%m-%d %H %M %S')
    if(isRes):
        copyImages(folder_name,timestamp)
    if(os.path.isdir('Logs/'+folder_name)):
        f = open('Logs/'+folder_name+'/'+log_filename, "a")
        f.write('Log('+timestamp+'):--> '+Msg+'\n')
        f.close()
    else:
        os.mkdir('Logs/'+folder_name) 
        f = open('Logs/'+folder_name+'/'+log_filename, "a")
        f.write('Log('+timestamp+'):--> '+Msg+'\n')
        f.close()
       
def checkfileSize(src_img,target_img):
    src_sz = os.stat(src_img).st_size
    trg_sz = os.stat(target_img).st_size
    src_invalid = False 
    trg_invalid = False 
    if(src_sz < 5000):
        src_invalid = True
        img = src
        Log('Source -> File size is less than 5KB',False)
    if(trg_sz < 5000):
        trg_invalid = True
        Log('Target -> File size is less than 5KB',False)
    return [src_invalid,trg_invalid]

    

def matchimages(img1,img2):
    global src
    global trg
    src = img1
    trg = img2
    Log("Copy Images -> Images Copied",True)
    invalid_files = checkfileSize(img1,img2)
    if(invalid_files[0] or invalid_files[1]):
        da = mb.showwarning ('Warning!','Bad Image, Image Size should be greator 5KB' ,icon = 'warning')
        return False

    try:
      source_image = face_recognition.load_image_file(img1)
      source_image_encoded = face_recognition.face_encodings(source_image)[0]
    except:
        da = mb.showwarning ('Warning!','Bad Image, please choose proper image' ,icon = 'warning')
        Log('Warning -> Bad Image, please choose proper image',False)
        if da != 'ok':
            print('ok')
        else:
            return False
        label_file_explorer.configure(text = "Capgemini Face Comparision",fg='blue')
    
    try:
      current_image = face_recognition.load_image_file(img2)
      current_image_encoded = face_recognition.face_encodings(current_image)[0]
    except:
        da = mb.showwarning ('Warning!','Bad Image, please choose proper image' ,icon = 'warning')
        Log('Warning -> Bad Image, please choose proper image',False)
        if da != 'ok':
            print('ok')
        else:
            return False
        label_file_explorer.configure(text = "Capgemini Face Comparision",fg='blue')

    result = face_recognition.compare_faces(
          [source_image_encoded], current_image_encoded,0.5)
    res = ""
    if result[0] == True:
       res='Result -> Matched\n -----------------------------------------------------------------------\n'
       label_file_explorer.configure(text="Matched",fg='green')
    else:
       label_file_explorer.configure(text="Not Matched",fg='red')
       res='Result ->Not Matched\n -----------------------------------------------------------------------\n'
    Log(res,False)

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
    Log('Source -> source Image Snipped',False)

def snipmatch():
    print(window.state)
    if (not is_src_img_selected):
       mb.showwarning('Warning','Please Select Source Image First')
       return False
    match_filename = 'temp_images/target.jpg'
    window.iconify()
    #os.system(r'snipping_tool.exe match.jpg')
    #window.state('zoomed')
    sn.Capture(match_filename)
    if(match_filename == ''):
        mb.showwarning('Warning','No Target Image Selected')
        return False
	# Change label contents 
    label_file_explorer.configure(text="Please Wait....",fg="blue")
    image1 = Image.open(match_filename)
    # The (450, 350) is (height, width)
    image1 = image1.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk1 = ImageTk.PhotoImage(image=image1)
    lmain_match.imgtk = imgtk1
    lmain_match.configure(image=imgtk1)
    Log('Target -> target Image Snipped',False)
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
    
    label_file_explorer.configure(text="Please Select Target Image")
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
    Log('Source -> source Image browsed',False)
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
        mb.showwarning('Warning','No Target Image Selected')
        return False
	# Change label contents 
    label_file_explorer.configure(text="Please Wait....",fg="blue")
    image1 = Image.open(match_filename)
    # The (450, 350) is (height, width)
    image1 = image1.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk1 = ImageTk.PhotoImage(image=image1)
    lmain_match.imgtk = imgtk1
    lmain_match.configure(image=imgtk1)
    Log('Target -> target Image browsed',False)
    matchimages(src_image,match_filename)

def setdefaultimages():
    image = Image.open('res/Source_person.jpg')
    # The (450, 350) is (height, width)
    image = image.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=image)
    lmain_src.imgtk = imgtk
    lmain_src.configure(image=imgtk)
    image1 = Image.open('res/Target_person.jpg')
    # The (450, 350) is (height, width)
    image1 = image1.resize((image_resize_width, image_resize_height), Image.ANTIALIAS)
    imgtk1 = ImageTk.PhotoImage(image=image1)
    lmain_match.imgtk = imgtk1
    lmain_match.configure(image=imgtk1)
	
																							
# Create the root window 
window = Tk() 

# Set window title 
window.title('Capgemini Face Recognition') 

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
lmain_src = Label(frmimg, compound=CENTER, anchor=CENTER, relief=RAISED,highlightbackground='#0070ad')
lmain_match = Label(frmimg, compound=CENTER, anchor=CENTER, relief=RAISED,highlightbackground= '#0070ad')
lmain_src.config(highlightbackground = "#0070ad", highlightcolor= "#0070ad")
lmain_src.config(highlightbackground = "#0070ad", highlightcolor= "#0070ad")
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
						text = "Browse Target Image", justify=LEFT,
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
						text = "Snip Target Image",justify=LEFT, 
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
setdefaultimages()
setup()
# Let the window wait for any events 
window.mainloop() 
