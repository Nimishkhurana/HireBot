# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:49:39 2019

@author: Nimish
"""

import cv2
import imutils
import numpy as np
from collections import defaultdict

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

open_eyes_detector = cv2.CascadeClassifier(
    'haarcascade_eye_tree_eyeglasses.xml')
left_eye_detector = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')
right_eye_detector = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')


video_capture = cv2.VideoCapture(0)
count=0
pos = pos_change = np.array([0,0],dtype=np.float)
while True:
    _, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for c,(x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        count+=1
        if count < 50:
            pos += np.array([x+w/2, y+h/2])
        elif count == 50:
            pos = pos/50
        else:
            pos_change += abs(pos-np.array([x+w/2, y+h/2]))
        cv2.putText(frame, "Count={} Pos={} PosChange={}".format(count,pos,pos_change), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
        cv2.circle(frame,tuple(pos.astype(np.int)),5, ( 255, 0,0), -1)
        cv2.circle(frame,tuple(np.array([x+w/2, y+h/2]).astype(np.int)),5, (0,255,0), -1)
        
        
        face = frame[y:y+h, x:x+w]
        gray_face = gray[y:y+h, x:x+w]
        # Eyes detection
        # check first if eyes are open (with glasses taking into account)
        open_eyes_glasses = open_eyes_detector.detectMultiScale(
            gray_face,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # if open_eyes_glasses detect eyes then they are open
        if len(open_eyes_glasses) == 2:
            for (ex, ey, ew, eh) in (open_eyes_glasses):
                cv2.rectangle(face, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                cv2.circle(face, (int(ex+ew/2), int(ey+eh/2)),5, (0, 255, 0), -1)

        # otherwise try detecting eyes using left and right_eye_detector
        # which can detect open and closed eyes
        
        elif len(open_eyes_glasses) > 2:
            # separate the face into left and right sides
            left_face=frame[y:y+h, x+int(w/2):x+w]
            left_face_gray=gray[y:y+h, x+int(w/2):x+w]

            right_face=frame[y:y+h, x:x+int(w/2)]
            right_face_gray=gray[y:y+h, x:x+int(w/2)]

            # Detect the left eye
            left_eye=left_eye_detector.detectMultiScale(
                left_face_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Detect the right eye
            right_eye=right_eye_detector.detectMultiScale(
                right_face_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            

            # For each eye check wether the eye is closed.
            # If one is closed we conclude the eyes are closed
            for (ex, ey, ew, eh) in right_eye:
                color=(0, 255, 0)
                cv2.rectangle(right_face, (ex, ey), (ex+ew, ey+eh), color, 2)
            for (ex, ey, ew, eh) in left_eye:
                color=(0, 255, 0)
                cv2.rectangle(left_face, (ex, ey), (ex+ew, ey+eh), color, 2)
    
    convas=frame

    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        'Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Video', convas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
print(pos_change/1000)
