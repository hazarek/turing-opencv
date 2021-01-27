import cv2
import random
import numpy as np
import uuid
import sys
from PIL import Image
# "q"       Quit
# "r"       Reset simulation
# "p" -     Save Current Frame as PNG and Quit
# "z"/"x" - Increase/Decrease high-pass level
# "w"/"s" - Increase/Decrease high-pass
# "d"/"a" - Increase/Decrease blur

def highpass(img, hpass_x, hpass_y, level):
    if not hpass_x % 2:
        hpass_x += 1
    if not hpass_y % 2:
        hpass_y += 1
    # print(hpass_x, hpass_y)
    if (hpass_x and hpass_y < 1):
        hpass_x, hpass_y = 1, 1
    return img - cv2.GaussianBlur(img, (0, 0), hpass_x, sigmaY=hpass_y) + level

def blur(img, blur_x, blur_y):
    if not blur_x % 2:
        blur_x += 1
    if not blur_y % 2:
        blur_y += 1
    if (blur_x and blur_y < 1):
        blur_x, blur_y = 1, 1
    return cv2.GaussianBlur(img, (0, 0), blur_x, sigmaY=blur_y)



# Create image as input
w, h = 512, 512
input_image = np.zeros((h, w, 4), np.uint8)
cv2.putText(input_image, 'RANDOM', (50, 220), 0, 3, (255, 255, 255, 255))
# video frames
frames = []
# Options
record = False
random = False
# Parameters
blur_x, blur_y = 6, 6
hpass_y, hpass_x = 6, 6
level = 127
iteration, max_iter = 0, 255
frame = input_image  # hold input_image for reset.
radius = 3
# cv2.namedWindow("Main")
cv2.namedWindow("Difference")
cv2.moveWindow("Difference", 0, 550)
output = Image.fromarray(input_image)

while True:
    key = cv2.waitKey(33)
    prior_frame = frame
    if random:
        rx, ry = random.uniform(1, 3), random.uniform(1, 3)
        
    # Apply Reaction-diffussion filters
    # cv2.putText(frame, str(blur_x), (50, 220), 0, 10, (255, 255, 255),thickness=6)
    frame = blur(frame, blur_x, blur_y)
    frame = highpass(frame, hpass_x, hpass_y, level)
    ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    
    diff = cv2.subtract(frame, prior_frame)
    diff[np.where((diff == [0, 0, 0, 255]).all(axis=2))] = [0, 0, 0, 0]
    diff[np.where((diff == [255, 255, 255, 255]).all(axis=2))] = [iteration, iteration, iteration, 255]
    cv2.imwrite("test/" + str(iteration) + "o.png", diff)

    output = Image.alpha_composite(output, Image.fromarray(diff))
    # show
    cv2.imshow("Difference", np.array(output))
    # cv2.imshow("Simulation", frame)
    # print(iteration)
    if iteration == max_iter:
        iteration == 0
    iteration += 32
    
    if key == ord('p'):
        cv2.imwrite("test/diff_" + str(uuid.uuid4()) + ".png", diff)
        cv2.imwrite("test/frame_" + str(uuid.uuid4()) + ".png", frame)
        break
    if key == ord('q'):
        break
    
    # RESET
    if key == ord('r'):
        blur_x, blur_y = 3, 3
        hpass_x, hpass_y = 3, 3
        level = 127
        frame = input_image
        
    # LEVEL
    if key == ord('x'):
        level += 1
        print(level)
    if key == ord('z'):
        level -= 1
        print(level)
        
    # HIGH-PASS
    if key == ord('w'):
        hpass_x += 1
        hpass_y += 1
        print(hpass_x,hpass_y)
    if key == ord('s'):
        hpass_x -= 1
        hpass_y -= 1
        print(hpass_x,hpass_y)
        
    # BLUR
    if key == ord('d'):
        blur_x += 1
        blur_y += 1
        print(blur_x, blur_y)
    if key == ord('a'):
        blur_x -= 1
        blur_y -= 1
        print(blur_x, blur_y)
        
    # RECORD
    if record:
        frames.append(frame)
if record:
    out = cv2.VideoWriter("out.mov",
                          cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                          23,
                          (frame.shape[1], frame.shape[0]))
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()
cv2.destroyAllWindows()
