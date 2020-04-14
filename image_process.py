import io
import base64
from PIL import Image

import inference
import numpy as np
from keras.models import load_model
from keras import backend as K
import cv2
from statistics import mode
import threading
import sys
import os
from datetime import datetime
import pandas as pd


def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x


def frame_process(base64_string_list):
    # starting lists for calculating modes

    ls = []


###############################################

    detection_model_path = os.getcwd(
    ) + '/trained_models/detection_models/haarcascade_frontalface_default.xml'

    emotion_model_path = os.getcwd() + \
        '/trained_models/emotion_models/emotion_modelsfer2013_mini_XCEPTION.82-0.80.hdf5'

    emotion_labels = {0: 'confused', 1: 'neutral', 2: 'confident'}

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # loading models

    face_detection = inference.load_detection_model(detection_model_path)

    emotion_classifier = load_model(emotion_model_path, compile=False)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
#################################################################
    for base64_string in base64_string_list:
        imgdata = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(imgdata))

        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        rgb_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        faces = inference.detect_faces(face_detection, gray_image)

        for face_coordinates in faces:
            print(face_coordinates)
            x1, x2, y1, y2 = inference.apply_offsets(
                face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))

            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = emotion_labels[emotion_label_arg]
            ls.append(emotion_text)

    K.clear_session()

    return ls
