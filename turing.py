import cv2
import random
import numpy as np
import uuid
import sys

# "q"       Quit
# "r"       Reset simulation
# "p" -     Save Current Frame as PNG and Quit
# "w"/"s" - Increase/Decrease high-pass level

cv2.namedWindow("Main")
cv2.namedWindow("Difference")
cv2.moveWindow("Difference", 0,550)


# Create image as input
w, h = 512, 512
input_image = np.zeros((h, w), np.uint8)
cv2.putText(input_image, 'RANDOM', (50, 220), 0, 3, (255))
# video frames
frames = []
# Options
record = False
random = False
# Parameters
rx, ry = 6, 6
highpass_level = 127
iteration = 0
frame = input_image # hold input_image for reset.
while True:
    key = cv2.waitKey(33)
    temp_frame = frame
    if random:   
        rx, ry = random.uniform(1,3), random.uniform(1,3)
    # Apply Reaction-diffussion filters
    frame = cv2.GaussianBlur(frame, (0,0), rx, sigmaY=ry)
    frame = frame - cv2.GaussianBlur(frame, (0,0), sigmaX=rx, sigmaY=ry) + highpass_level
    ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    # show
    cv2.imshow("Difference", cv2.subtract(frame, temp_frame))
    cv2.imshow("Simulation", frame)
    
    if key == ord('p'):
        cv2.imwrite("test/out_" + str(uuid.uuid4()) + ".png", frame)
        break
    if key==ord('q'):
        break
    if key==ord('r'): #reset simulation
        frame = input_image
    if key==ord('w'):
        highpass_level += 1
        print(highpass_level)
    if key==ord('s'):
        highpass_level -= 1
        print(highpass_level)
    if record:
        frames.append(frame)
    iteration += 1
if record:
    out = cv2.VideoWriter("out.mov",
    cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
    23,
    (frame.shape[1], frame.shape[0]))
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()

cv2.destroyAllWindows()
