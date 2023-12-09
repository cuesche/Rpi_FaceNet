import io
import re
import os
import time
from tflite_runtime.interpreter import load_delegate


import numpy as np
import picamera

from PIL import Image
from PIL import ImageDraw
import cv2

#import pyttsx3
#engine = pyttsx3.init()


from tflite_runtime.interpreter import Interpreter

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 960

def main():

  start__time=time.time()
  
  
  people_lables = load_labels('people_labels.txt')

  interpreter = Interpreter(model_path = 'models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite',
    experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
  
  interpreter.allocate_tensors()
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
  
  #get interpreter for face embedding model

  interpreter_emb = Interpreter(model_path = 'models/Mobilenet1_triplet1589223569_triplet_quant_edgetpu.tflite',
    experimental_delegates=[load_delegate('libedgetpu.so.1.0')]) 

  interpreter_emb.allocate_tensors()

  with picamera.PiCamera(
      resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:      
    camera.rotation=270
    camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
    try:
      stream = io.BytesIO()
      
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        image_large = Image.open(stream)
        image = image_large.convert('RGB').resize(
            (input_width, input_height), Image.LANCZOS)
        start_time = time.monotonic()##################fractual seconds flasch nimmt nur die nachkommastellen
        results = detect_objects(interpreter, image, 0.7)#### thereshold face detection
        elapsed_ms = (time.monotonic() - start_time) * 1000

        ymin, xmin, ymax, xmax, score = get_best_box_param(results,CAMERA_WIDTH,CAMERA_HEIGHT)
        if (time.time()-start__time)>10:
            return "unknown"   
        
        if score > 0.96:
            img = np.array(image_large)
            img_cut = img[ymin:ymax,xmin:xmax,:]
            img_cut = cv2.resize(img_cut, dsize=(96, 96), interpolation=cv2.INTER_CUBIC).astype('uint8')
            img_cut = img_cut.reshape(1,96,96,3)/255.

            emb = img_to_emb(interpreter_emb,img_cut)
            
            person=get_person_from_embedding(people_lables,emb)            
            
            return person

        stream.seek(0)
        stream.truncate()
            

    finally:
      camera.stop_preview()

def get_person_from_embedding(people_lables,emb):
    #Comares embedding to embedding of scaned people to determine who is on the picture
    num_emb_check = 20#<-----------------sinnfrei?
    path = 'scanned_people/'
    folders = os.listdir(path)
    folders = sorted(folders)
    averages = np.zeros(len(folders))
    folder_number = 0
    start = time.time()
    for folder in folders:
        average_one_person = 0
        
        files = os.listdir(path + folder + '/embeddings')
        files = sorted(files)
        checked = 0
        for file in files:
            emb2 = np.load(path + folder + '/embeddings' + '/' + file)
            
            norm = np.sum((emb-emb2)**2)
            average_one_person = average_one_person + norm
            
            checked = checked + 1
            if checked == num_emb_check:
                break
        average_one_person = average_one_person/num_emb_check
        averages[folder_number] = averages[folder_number] + average_one_person
        folder_number = folder_number + 1
    who_is_on_pic = 0
    lowest_norm_found = 10
    run = 0
    end = time.time()
    print("time for detection: ", end-start)
    for average in averages:
        run = run + 1
        if average < 0.4 and average < lowest_norm_found: ###<----------The threshold for recognition (0.6 ) lowest_norm_found = average hinzugefügt da dies vermutlich vergessen wurde sonst lowest norm found immer 10
            who_is_on_pic = run
            lowest_norm_found = average
        print(average)
    print("person on pic: ", people_lables[who_is_on_pic])
    if who_is_on_pic > 0:
        
        
        print("\n\n\n")
    return people_lables[who_is_on_pic]
        
def load_labels(path):
  #Loads lables from file
  dict = {}
  with open(path, 'r', encoding='utf-8') as f:
      for line in f:
          key, value = line.strip().split('::')  
          dict[key] = value
        
  return dict


def set_input_tensor(interpreter, image):
  #Sets the input tensor.
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  #Returns the output tensor at the given index.
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor

def set_input_tensor_emb(interpreter, input):
    #Sets input sensor for face embedding model
    input_details = interpreter.get_input_details()[0]
    tensor_index = input_details['index']
    scale, zero_point = input_details['quantization']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = np.uint8(input/scale + zero_point)



def img_to_emb(interpreter,input):
    #returns embedding vector, using the face embedding model
    set_input_tensor_emb(interpreter, input)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    #emb = np.squeeze(interpreter.get_tensor(output_details['index']))
    emb = interpreter.get_tensor(output_details['index'])
    scale, zero_point = output_details['quantization']
    emb = scale * (emb - zero_point)
    return emb

def detect_objects(interpreter, image, threshold):
  #Returns a list of detection results, each a dictionary of object info.
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results

def get_best_box_param(results,CAMERA_WIDTH, CAMERA_HEIGHT):
    #Returns the box parameters for the box with the highest score
    best_boxvalue = 0
    xmin = 0
    xmax = 1
    ymin = 0
    ymax = 1
    for obj in results:
        if obj['score'] > best_boxvalue:
            best_boxvalue = obj['score']
            ymin, xmin, ymax, xmax = obj['bounding_box']
            if xmin < 0:
                xmin = 0
            if xmax > 1:
                xmax = 1
            if ymin < 0:
                ymin = 0
            if ymax > 1:
                ymax = 1
            xmin = int(xmin * CAMERA_WIDTH)
            xmax = int(xmax * CAMERA_WIDTH)
            ymin = int(ymin * CAMERA_HEIGHT)
            ymax = int(ymax * CAMERA_HEIGHT)
    
    return ymin, xmin, ymax, xmax, best_boxvalue

if __name__ == '__main__':
  main()
