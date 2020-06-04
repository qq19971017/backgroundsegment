import cv2
import numpy as np
import joblib

cap = cv2.VideoCapture("VideoRecord.avi")
fgbg = cv2.createBackgroundSubtractorMOG2()
Roi = joblib.load("config.pkl")
pts = Roi.get('ROI')
points = np.array(pts, np.int32)
points = points.reshape((-1, 1, 2))


# 指定视频编解码方式为MJPG
codec = cv2.VideoWriter_fourcc(*'MJPG')
fps = 25.0  # 指定写入帧率为25
# frameSize = (640, 480)  # 指定窗口大小
frameSize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# # 创建 VideoWriter对象
output_video1 = cv2.VideoWriter('roi.avi', codec, fps, frameSize)
output_video2 = cv2.VideoWriter('backsub.avi', codec, fps, frameSize)
output_video3 = cv2.VideoWriter('test.avi', codec, fps, frameSize)

while (cap.isOpened):
    ret, frame  =cap.read()
    if ret:
        fgmask = fgbg.apply(frame)
        mask = np.zeros(frame.shape, np.uint8)
        mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
        mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))  # 用于求 ROI
        mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))  # 用于 显示在桌面的图像
        show_image = cv2.addWeighted(src1=frame, alpha=0.8, src2=mask3, beta=0.2, gamma=0)
        ROI = cv2.bitwise_and(mask2, frame)
        fgmask_roi = fgbg.apply(ROI)
        # (im2, contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # looping for contours
        # for c in contours:
        #     if cv2.contourArea(c) < 500:
        #         continue
        #
        #     # get bounding box from countour
        #     (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv2.polylines(frame, [points], True, (255, 0, 0), 2)  # 对roi区域进行标定

        #  进行物体识别，主要是获取轮廓，然后获取最终目标的最小外接矩形
        contours, hierarchy = cv2.findContours(fgmask_roi, cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓
        for contour in contours:
            if cv2.contourArea(contour) < 60:
                continue
            (x, y , w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)

        cv2.imshow('BackgroundSubtractorMOG2', fgmask)
        cv2.imshow('rgb', frame)
        cv2.imshow('roi', ROI)
        cv2.imshow('mog_roi',fgmask_roi)
        fgmask_roi = cv2.cvtColor(fgmask_roi, cv2.COLOR_GRAY2RGB)
        output_video1.write(ROI)
        output_video2.write(fgmask_roi)
        output_video3.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
