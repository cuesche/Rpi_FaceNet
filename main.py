# System
import time
import datetime
import requests
import json
import numpy as np
import platform
import webbrowser
import os
import pyautogui
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

#bilderkennung
import os
import time
import pathlib
import numpy as np
import io

from picamera import PiCamera
from PIL import Image

from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.adapters import detect


#pfade noch anpassen wenn fertig mit testen

mobileNet_path ='/home/pi/Desktop/PAIND_raspi/model_merged/co_compiled_verification_edgetpu.tflite'
mobileNet_label_file ='/home/pi/Desktop/PAIND_raspi/model_merged/labels_pers.txt'
face_model= '/home/pi/Desktop/PAIND_raspi/model_merged/co_compiled_face_edgetpu.tflite'


# Initialisierung des TensorFlow Lite Interpreters
interpreter_face = edgetpu.make_interpreter(face_model)
interpreter_face.allocate_tensors()

# Größe für das Eingabebild des Modells
size_input_face_mod = common.input_size(interpreter_face)


##########################Functions############################################

def detect_faces(image):
    
    global state
    state=0
    
    image.show()
    _, scale = common.set_resized_input(
        interpreter_face, image.size, lambda size: image.resize(size, Image.LANCZOS))
    
    interpreter_face.invoke()
    objs = detect.get_objects(interpreter_face, score_threshold=0.5, image_scale=scale)    
    
    if len(objs) == 0:
        print("Kein Gesicht gefunden")
        state=0
        return
       
    elif len(objs)==1:
        bbox = objs[0].bbox
        face_image = image.crop((bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax))           
        face_image = face_image.resize((224, 224), Image.LANCZOS)
        face_image.show()
        state=2
        return face_image
        
    
    else:
        print("mehrer personen erkannt")
        state=1
        return    

def validate_faces(image):
    
    global state
    
    interpreter_mobileNet = edgetpu.make_interpreter(mobileNet_path)
    interpreter_mobileNet.allocate_tensors()
    
    common.set_input(interpreter_mobileNet, image)
    interpreter_mobileNet.invoke()
    
    classes = classify.get_classes(interpreter_mobileNet, top_k=1)
    labels = dataset.read_label_file(mobileNet_label_file)

    if classes:
        class_id=classes[0].id        
        class_score=classes[0].score
        person=labels.get(class_id,class_id)
        print(person,class_score)
        state=3
        return person
    
    else:
        state=4
        return

def pers_inhalt():
    
    print("Persöhnlicher inhalt has to be done")
    
    return


def initialise():
    
    global state
    root.geometry('400x150+300+300')
    speicher=io.BytesIO()
    
    with PiCamera() as camera:
        camera.resolution = (400, 400)
        camera.start_preview()
        time.sleep(2)
        camera.capture(speicher, format='jpeg')
        camera.stop_preview()
        
    speicher.seek(0)
    
    image=Image.open(speicher)
    image=detect_faces(image)
      
    #No face detected
    if state==0:
        button_cancel.grid()
        button_retry.grid()
        button_personal_content.grid_remove()
        
        label_no_face.grid()
        
    #multiple faces detected
    elif state==1:
        button_cancel.grid()
        button_retry.grid()
        button_personal_content.grid_remove()
        
        label_multible_persons.grid()   
            
    #face detected
    elif state==2:
        authenticated_person=validate_faces(image)
        
        if state==3:
            button_cancel.grid()
            button_login.grid()
            button_personal_content.grid_remove() 
            
            label_person_recognized.grid()           
        
        elif state==4:
            button_cancel.grid()
            button_retry.grid()
            button_personal_content.grid_remove()
            
            label_no_person_recognized.grid()
                
    speicher.close()   
    return

def state_zero():
    
    root.geometry('200x80+10+10')
    
    button_personal_content.grid()
    button_cancel.grid_remove()
    button_retry.grid_remove()
    button_login.grid_remove()

    label_no_face.grid_remove()
    label_no_person_recognized.grid_remove()
    label_person_recognized.grid_remove()
    
    return
##########################Program############################################

"""
# Prüfen Internetverbindung
timeout=5
try:
    request = requests.get('https://app.powerbi.com', timeout=timeout)
    print("WLAN erfolgreich geprüft - " + datetime.now().isoformat())
except (requests.ConnectionError, requests.Timeout) as exception:
    print("kein Internet! - " + datetime.now().isoformat())

# Vollbild mit Klick
print("Dashboard öffnen")
pyautogui.FAILSAFE = False
webbrowser.open('https://app.powerbi.com/groups/me/dashboards/6d041d20-836a-4a16-a5b1-5a38d9cf464c?chromeless=1')
time.sleep(10)
#pyautogui.hotkey('f11')
time.sleep(30)
#pyautogui.click(1800, 65)
time.sleep(2)
#pyautogui.click(1901, 44)
#pyautogui.click(1815, 1020)


"""

# Create the main window
root = tk.Tk()
root.title("Persönlicher Inhalt")
root.geometry('200x60+10+10')
root.attributes('-topmost',1)

# Definieren Sie einen Container-Frame für die Nachrichten
message_frame = tk.Frame(root, borderwidth=2, relief="groove")
message_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Definieren Sie einen Container-Frame für die Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Nachrichten-Label, anfänglich nicht sichtbar
label_no_face = tk.Label(message_frame, text="No face detected", fg="white", bg="red", width=40)
label_no_person_recognized = tk.Label(message_frame, text="No person recognized", fg="white", bg="red", width=40)
label_person_recognized = tk.Label(message_frame, text="Person recognized", fg="white", bg="red", width=40)
label_multible_persons = tk.Label(message_frame, text="Multiple persons recognized - please try again", fg="white", bg="red", width=40)

# Verstecke alle Labels anfangs
label_no_face.grid(row=0, column=0, sticky="ew")
label_no_person_recognized.grid(row=0, column=0, sticky="ew")
label_person_recognized.grid(row=0, column=0, sticky="ew")
label_multible_persons.grid(row=0, column=0, sticky="ew")
label_no_face.grid_remove()
label_no_person_recognized.grid_remove()
label_person_recognized.grid_remove()
label_multible_persons.grid_remove()

# Definieren der Buttons
button_personal_content = tk.Button(button_frame, text="Personal Content", bg="red", fg="white",command=initialise )
button_cancel = tk.Button(button_frame, text="Cancel",command=state_zero )
button_retry = tk.Button(button_frame, text="Retry", command=initialise )
button_login = tk.Button(button_frame, text="Login", command=pers_inhalt)

# Platziere Buttons in einem Grid
button_personal_content.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
button_cancel.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
button_retry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
button_login.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# Verstecke alle Buttons anfangs

button_cancel.grid_remove()
button_retry.grid_remove()
button_login.grid_remove()

# Stellen Sie sicher, dass die Spalten sich ausdehnen und anpassen
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)


root.mainloop()


# Run the application
root.mainloop()



