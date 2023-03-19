import cv2
import numpy as np

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
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 2)

            frame1 = frame[faces[0][1]:faces[0][1]+faces[0]
                           [3], faces[0][0]:faces[0][0]+faces[0][2]]

            eye_orig_image = frame1[eyes[0][1]:(
                eyes[0][1]+eyes[0][3]), eyes[0][0]:(eyes[0][0]+eyes[0][2])]

            cv2.imshow('iris', eye_orig_image)

            roi = eye_orig_image
            rows, cols, _ = roi.shape
            row1, col1, _ = frame1.shape
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

            value = 0

            _, threshold = cv2.threshold(
                    gray_roi, 100, 255, cv2.THRESH_BINARY_INV)
            contour, _ = cv2.findContours(
                    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area=0
            for cnt in contour:
                    area = area+cv2.contourArea(cnt)

            while (value < 100):

                _, threshold = cv2.threshold(
                    gray_roi, value, 255, cv2.THRESH_BINARY_INV)
                th, tw = threshold.shape
                split1 = threshold[0:int(th/2), 0:tw]
                split2 = threshold[int(th/2):th, 0:tw]
                contour1, _ = cv2.findContours(
                    split1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                contour2, _ = cv2.findContours(
                    split2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                area1=0
                area2=0
                for cnt in contour1:
                    area1 = area1+cv2.contourArea(cnt)
                for cnt in contour2:
                    area2 = area2+cv2.contourArea(cnt)
                
                
                if (area1 + area2>0.6*area):
                    value=40
                    break
                elif(area1>0.8*area2):
                    break

                value = value+1
            print(value)
            # value=40
            # _, threshold = cv2.threshold(
            #         gray_roi, value, 255, cv2.THRESH_BINARY_INV)

            contours, _ = cv2.findContours(
                threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(
                contours, key=lambda x: cv2.contourArea(x), reverse=True)
            for cnt in contours:
                (x, y, w, h) = cv2.boundingRect(cnt)
                # cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # cv2.line(roi, (x + int(w/2), 0),
                #          (x + int(w/2), rows), (0, 255, 0), 2)
                # cv2.line(roi, (0, y + int(h/2)),
                #          (cols, y + int(h/2)), (0, 255, 0), 2)
                cv2.line(frame, (fx+ex+x + int(w/2), 0),
                         (fx+ex+x + int(w/2), row0), (0, 255, 0), 2)
                cv2.line(frame, (0, fy+ey+y + int(h/2)),
                         (col0, fy+ey+y + int(h/2)), (0, 255, 0), 2)
                break
            # cv2.imshow("Threshold", threshold)
            # cv2.imshow("gray roi", gray_roi)
            # cv2.imshow("Roi", roi)
            cv2.imshow('frame', frame)

    key = cv2.waitKey(30)
    if key == 27:
        break
cv2.destroyAllWindows()
