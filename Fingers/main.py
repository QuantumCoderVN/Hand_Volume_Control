import cv2
import numpy as np
import os
import time
import hand as htm


# Initialize variables
pTime = 0

# Set webcam resolution
cap = cv2.VideoCapture(0)
FolderPath = "Fingers" # Folder containing images
lst = os.listdir(FolderPath)
lst_2 = [] # List containing arrays of image values
# print(lst)

# Append images to lst_2 from FolderPath directory 
for i in lst:
    image = cv2.imread(f"{FolderPath}/{i}")
    # print(f"{FolderPath}/{i}")
    lst_2.append(image)


detector = htm.handDetector(detectionCon=0.75) # Set detection confidence to 75%

fingerid = [4, 8, 12, 16, 20] # Fingers to detect (Thumb, Index, Middle, Ring, Pinky)
while True:
    res, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False) # Detect position and draw lines on the frame



    # Write code to detect fingers
    if len(lmList) != 0: # If there are landmarks detected in the frame 
        
        finger = [] # List to store fingers
        # Write for the thumb (The idea is point 4 on the left or right of point 2)
        if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]: # If the x-coordinate of the thumb is less than the x-coordinate of the thumb - 1
            finger.append(1) # Append 1 to the finger list
        else:
            finger.append(0)



        for id in range (1, 5): # Loop
            if lmList[fingerid[id]][2] < lmList[fingerid[id] - 2][2]: # If the y-coordinate of the finger is less than the y-coordinate of the finger - 2
                finger.append(1) # Append 1 to the finger list
            else:
                finger.append(0)
        numberoffinger = finger.count(1) # Count the number of fingers
       

        h, w, c = lst_2[numberoffinger-1].shape
        frame[0:h, 0:w] = lst_2[numberoffinger-1] # Display the first image in the list

        # Write code to display the number of fingers
        cv2.rectangle = (frame, (0, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(finger.count(1)), (25, 300), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        




    # Write FPS
    cTime = time.time() # Current time
    fps = 1 / (cTime - pTime) # Calculate FPS
    pTime = cTime # Set previous time
    cv2.putText(frame, f'FPS: {int(fps)}', (200, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3) # Write FPS on frame


    cv2.imshow('Show video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # Press q to quit
        break

cap.release() # Release the webcam
cv2.destroyAllWindows() # Close the window
