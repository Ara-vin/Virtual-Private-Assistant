import cv2
import numpy as np
import face_recognition
import os
import subprocess
import time

path = r'<path to database>'
images =[]
Names =[]
name=''
myList = os.listdir(path)
for cls in myList:
 cur_img = cv2.imread(f'{path}/{cls}')
 images.append(cur_img)
 Names.append(os.path.splitext(cls)[0])

def GetEncodings(images):
 encodelist =[]
 for img in images:
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  encoding = face_recognition.face_encodings(img)[0]
  encodelist.append(encoding)
 return encodelist

encodeknownlist = GetEncodings(images)
print('Encoding Completed!!')
cam = cv2.VideoCapture(0)

while True:
    success, img = cam.read()
    small_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
    facecurframe = face_recognition.face_locations(small_img)
    encodecurframe = face_recognition.face_encodings(small_img, facecurframe)
    if(len(encodecurframe)+len(facecurframe)!=0):
        for encodeface, faceloc in zip(encodecurframe, facecurframe):
            matches = face_recognition.compare_faces(encodeknownlist, encodeface)
            face_dist = face_recognition.face_distance(encodeknownlist, encodeface)
            matchindex = np.argmin(face_dist)

        if matches[matchindex]:
            name = Names[matchindex]
            y1, x2, y2, x1 = faceloc
            y1 = y1 * 4
            x2 = x2 * 4
            y2 = y2 * 4
            x1 = x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2 + 40), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            time.sleep(2)
            if name in Names:
                cam.release()
                cv2.destroyAllWindows()
                exec(open("GUIASSISTANT.py").read())

        else:
            name = 'Unknown!!'
            y1, x2, y2, x1 = faceloc
            y1 = y1 * 4
            x2 = x2 * 4
            y2 = y2 * 4
            x1 = x1 * 4
            cv2.rectangle(img, (x1, y1), (x2+20, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2+20, y2 + 40), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    else:
        name = 'Face Not Found!'
        y1, x2, y2, x1 = (20, 118, 72, 66)
        y1 = y1 * 4
        x2 = x2 * 4
        y2 = y2 * 4
        x1 = x1 * 4
        cv2.rectangle(img, (x1, y2 - 35), (x2+85, y2 + 40), (255, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
