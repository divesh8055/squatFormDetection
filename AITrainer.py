import cv2
import numpy as np
import PoseModule as pm
 
# for video already captured
cap = cv2.VideoCapture("squat_1.mp4")

# for live video capturing through camera
# cap = cv2.VideoCapture()
# cap.open(1, cv2.CAP_DSHOW)
detector = pm.poseDetector()
count = 0 #count of the number of squats
dir = 0 #for sitting and standing positions
while True:
    #reading each frame
    success, img = cap.read()
    
    #Resizing the image to show it properly in the frame
    # img = cv2.resize(img, (720, 1280))
    
    #Slicing out the extra parts of the frame
    img = img[:,210:-200,:]
    
    #find the posing
    img = detector.findPose(img, False)
    
    #finding the position
    lmList = detector.findPosition(img, False)
    # print(lmList)
    
    if len(lmList) != 0:
        angle = detector.findAngle(img, 23, 25, 27)
        per = np.interp(angle, (80, 170), (0, 100))
        bar = np.interp(angle, (80, 170), (650, 100))
        # print(angle, per)
 
        color = (255, 0, 255)
        if per == 0:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 100:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        # print(count)
 
        # Drawing the Progress Bar
        cv2.rectangle(img, (800, 100), (825, 650), color, 3)
        cv2.rectangle(img, (800, int(bar)), (825, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (800, 75), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
 
        # Writing the Squat Count
        # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 10,
                    (255, 0, 0), 15)
 
    #displaying the frames
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyWindow("Image")
        break
    cv2.waitKey(1)