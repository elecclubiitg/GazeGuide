import cv2
import numpy as np
import pyautogui as p

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
            ey = ey+int(eh/4)
            eh = int(eh/2)
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 2)
            frame1 = frame[faces[0][1]:faces[0][1]+faces[0]
                           [3], faces[0][0]:faces[0][0]+faces[0][2]]

            eye_orig_image = frame1[eyes[0][1]+int(eyes[0][3]/4):(
                eyes[0][1]+int(3*eyes[0][3]/4)), eyes[0][0]:(eyes[0][0]+eyes[0][2])]
            if eye_orig_image.shape[0] == 0:
                cv2.imshow('frame', frame)
                key = cv2.waitKey(30)
                if key == 27:
                    break
                continue
            # cv2.imshow('iris', eye_orig_image)

            roi = eye_orig_image
            rows, cols, _ = roi.shape
            row1, col1, _ = frame1.shape

            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
            # kernel=np.ones((5,5),np.uint8)
            # gray_roi=cv2.dilate(gray_roi,kernel,iterations=2)
            # gray_roi=cv2.erode(gray_roi,kernel,iterations=2)
            value = 10
            t_area = roi.shape[0] * roi.shape[1]

            while (value < 100):

                _, threshold = cv2.threshold(
                    gray_roi, value, 255, cv2.THRESH_BINARY_INV)

                contours, _ = cv2.findContours(
                    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(
                    contours, key=lambda x: cv2.contourArea(x), reverse=True)
                # print(contours)

                # area=0
                if (len(contours) > 0):
                    area = cv2.contourArea(contours[0])
                else:
                    value = value+1
                    continue
                if (area == 0):
                    value = value+1
                    continue
                if (t_area/area < 20):
                    break
                value = value+1

            print(value)

            for cnt in contours:
                (x, y, w, h) = cv2.boundingRect(cnt)
                # cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
                cv2.line(frame, (fx+ex+x + int(w/2), 0),
                         (fx+ex+x + int(w/2), row0), (0, 255, 0), 2)
                cv2.line(frame, (0, fy+ey+y + int(h/2)),
                         (col0, fy+ey+y + int(h/2)), (0, 255, 0), 2)
                if (x+int(w/2) < int(ew/2)):
                    p.moveRel(10, 0, duration=0.01)
                if (x+int(w/2) > int(2*ew/3)):
                    p.moveRel(-10, 0, duration=0.01)
                break
            
            (x_axis, y_axis), radius = cv2.minEnclosingCircle(contours[0])

            center = (int(x_axis), int(y_axis))
            radius = int(radius)

            cv2.circle(roi, center, radius, (0, 255, 0), 2)
            # cv2.imshow("gray roi", gray_roi)
            # cv2.imshow("Roi", roi)

            # area = cv2.contourArea(cnt)
            # if(area==0):continue
            b = t_area/area
            print(area, t_area, b)
            cv2.putText(frame, f'{b}', (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 0, 0], 2)
            cv2.imshow('Thresh', threshold)
            cv2.imshow('frame', frame)

    key = cv2.waitKey(30)
    if key == 27:
        break

cv2.destroyAllWindows()
