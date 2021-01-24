import cv2
import random
import numpy as np
import uuid

record = False
frames = []
random = False

# "q" Quit
# "s" - Save Current Frame as PNG and Quit

img = np.zeros((512,512,3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'RANDOM',(50,220), font, 3,(255,255,255),2,cv2.LINE_AA)
cv2.putText(img,'TURING',(90,370), font, 3,(255,255,255),2,cv2.LINE_AA)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rx, ry = 7, 7

while True:
    temp_img = img
    if random:   
        rx, ry = random.uniform(1,3), random.uniform(1,3)
        
    # Reaction-diffussion filters
    img = cv2.GaussianBlur(img, (0,0), rx, sigmaY=ry)
    img = img - cv2.GaussianBlur(img, (0,0), sigmaX=rx, sigmaY=ry) + 115
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite("out" + str(uuid.uuid4()) + ".png", img)
        break
    if key==ord('q'):
        break
    if record:
        frames.append(img)
    # cv2.imshow("RD", cv2.subtract(img, temp_img))
    cv2.imshow("RD", img)
    

if record:
    out = cv2.VideoWriter("out.mov",
    cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
    23,
    (img.shape[1], img.shape[0]))
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()

cv2.destroyAllWindows()
