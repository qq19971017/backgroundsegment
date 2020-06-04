import cv2

cap1 = cv2.VideoCapture(2)


while (cap1.isOpened):
    ret, frame1 = cap1.read()

    cv2.imshow("webcam1",frame1)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap1.release()
cv2.destroyAllWindows()

