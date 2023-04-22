import cv2
import numpy as np  
import pyautogui 

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret is False:
        break
    row0, col0, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if (len(faces) == 0):
        cv2.imshow('frame', frame)
        key = cv2.waitKey(30)
        if key == 27:
            break
        continue

    for (fx, fy, fw, fh) in faces:
        # cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
        roi_gray = gray[fy:fy+fh, fx:fx+int(fw/2)]
        roi_color = frame[fy:fy+fh, fx:fx+fw]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        if (len(eyes) == 0):
            cv2.imshow('frame', frame)
            key = cv2.waitKey(30)
            if key == 27:
                break
            continue
            
        for (ex, ey, ew, eh) in eyes:
            ey=ey+int(eh/4)
            eh=int(eh/2)            
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 2)
            frame1 = frame[faces[0][1]:faces[0][1]+faces[0]
                           [3], faces[0][0]:faces[0][0]+faces[0][2]]

            eye_orig_image = frame1[eyes[0][1]+int(eyes[0][3]/4):(
                eyes[0][1]+int(3*eyes[0][3]/4)), eyes[0][0]:(eyes[0][0]+eyes[0][2])]
            if eye_orig_image.shape[0]==0: 
                cv2.imshow('frame', frame)
                key = cv2.waitKey(30)
                if key == 27:
                    break
                continue
            # cv2.imshow('iris', eye_orig_image)
    
            roi = eye_orig_image
            rows, cols, _ = roi.shape
            row1, col1, _ = frame1.shape
            # if(len(roi)==0): break
                
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
            # kernel=np.ones((5,5),np.uint8)
            # gray_roi=cv2.dilate(gray_roi,kernel,iterations=2) 
            # gray_roi=cv2.erode(gray_roi,kernel,iterations=2) 
            value = 10
            t_area =roi.shape[0] * roi.shape[1]

            
            
            # contour, _ = cv2.findContours(
            #         threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            while (value < 100):

                _, threshold = cv2.threshold(
                    gray_roi, value, 255, cv2.THRESH_BINARY_INV)
                
                contours, _ = cv2.findContours(
                threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # area=0
                contours = sorted(
                    contours, key=lambda x: cv2.contourArea(x), reverse=True)
                print(contours)
                if(len(contours)>0):area=cv2.contourArea(contours[0])
                else:
                    value=value+1
                    continue
                if(area==0):
                    value=value+1
                    continue
                if(t_area/area<15):
                    break
                value=value+1

                    
                    
                
                
                # _, threshold = cv2.threshold(
                #     gray_roi, value, 255, cv2.THRESH_BINARY_INV)
                # th, tw = threshold.shape
                # split1 = threshold[0:int(th/2), 0:tw]
                # split2 = threshold[int(th/2):th, 0:tw]
                # contour1, _ = cv2.findContours(
                #     split1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                # contour2, _ = cv2.findContours(
                #     split2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                # area1=0
                # area2=0
                # for cnt in contour1:
                #     area1 = area1+cv2.contourArea(cnt)
                # for cnt in contour2:
                #     area2 = area2+cv2.contourArea(cnt)
                
                
                # if (area1 + area2>0.6*area):
                #     value=40
                #     break
                # elif(area1>area2):
                #     break

                # value = value+1
            # value=45
            print(value)
            # threshold = cv2.adaptiveThreshold(
                    # gray_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY_INV,11,2)
            # _, threshold = cv2.threshold(
            #         gray_roi, value, 255, cv2.THRESH_BINARY_INV)
            
            # contours, _ = cv2.findContours(
            #     threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            
            # contours = sorted(
            #     contours, key=lambda x: cv2.contourArea(x), reverse=True)
            
            (x_axis,y_axis),radius = cv2.minEnclosingCircle(contours[0])

            center = (int(x_axis),int(y_axis))
            radius = int(radius)

            cv2.circle(roi,center,radius,(0,255,0),2)
            # cv2.imshow("gray roi", gray_roi)
            # cv2.imshow("Roi", roi)
            
            # area = cv2.contourArea(cnt)
            # if(area==0):continue
            b=t_area/area
            print (area,t_area,b)
            cv2.putText(frame,f'{b}', (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, [255,0,0], 2)
            cv2.imshow('Thresh',threshold)
            cv2.imshow('frame', frame)


    key = cv2.waitKey(30)
    if key == 27:
        break
cv2.destroyAllWindows()