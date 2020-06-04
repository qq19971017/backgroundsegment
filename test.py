import joblib
import cv2
import numpy as np

Roi = joblib.load("config.pkl")

pts = Roi.get('ROI')

img = cv2.imread("image.jpg")
mask = np.zeros(img.shape, np.uint8)
points = np.array(pts, np.int32)
points = points.reshape((-1, 1, 2))

# 画多边形
mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))  # 用于求 ROI
mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))      # 用于 显示在桌面的图像
show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

cv2.imshow("mask", mask2)
cv2.imshow("show_img", show_image)

ROI = cv2.bitwise_and(mask2, img)
cv2.imshow("ROI", ROI)
cv2.waitKey(0)