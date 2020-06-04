
import cv2
import numpy as np
import joblib

pts = []  # 用于存放点
pts_inner = [] # 用于存放标记内部roi的点
 # 用于判断画外框还是内框
flag = 0
img2= []

# 统一的：mouse callback function
def draw_roi(event, x, y, flags, param):


    global flag
    global img2

    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击，选择点
        if flag == 0:
            pts.append((x, y))
        else:
            pts_inner.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:  # 右键点击，取消最近一次选择的点
        if flag == 0:
            pts.pop()
        else:
            pts_inner.pop()
    if event == cv2.EVENT_MBUTTONDOWN:  # 中键绘制轮廓
        if flag == 0:
            mask = np.zeros(img.shape, np.uint8)
            points = np.array(pts, np.int32)
            points = points.reshape((-1, 1, 2))

            # 画多边形
            mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
            mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))  # 用于求 ROI
            mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))      # 用于 显示在桌面的图像
            show_image = cv2.addWeighted(src1=img2, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

            # cv2.imshow("mask", mask2)
            cv2.imshow("show_img", show_image)
            flag = 1
            # ROI = cv2.bitwise_and(mask2, img)
            # cv2.imshow("ROI", ROI)
            # cv2.waitKey(0)
        else:
            mask_inner = np.zeros(img.shape, np.uint8)
            points_inner = np.array(pts_inner, np.int32)
            points_inner = points_inner.reshape((-1, 1, 2))

            # 画多边形
            mask_inner = cv2.polylines(mask_inner, [points_inner], True, (255, 255, 255), 2)
            mask2_inner = cv2.fillPoly(mask_inner.copy(), [points_inner], (255, 255, 255))  # 用于求 ROI
            mask3_inner = cv2.fillPoly(mask_inner.copy(), [points_inner], (0, 0, 255))  # 用于 显示在桌面的图像
            show_image = cv2.addWeighted(src1=img2, alpha=0.8, src2=mask3_inner, beta=0.2, gamma=0)
            cv2.imshow("show_img", show_image)
            cv2.waitKey(0)
    if flag == 0:
        if len(pts) > 0:
            # 将pts中的最后一点画出来
            cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

        if len(pts) > 1:
            # 画线
            for i in range(len(pts) - 1):
                cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x ,y 为鼠标点击地方的坐标
                cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)
            if event == cv2.EVENT_MBUTTONDOWN:
                cv2.line(img=img2, pt1=pts[len(pts)-1], pt2=pts[0], color=(255, 0, 0), thickness=2)
    else:
        if len(pts_inner) > 0:
            # 将pts中的最后一点画出来
            cv2.circle(img2, pts_inner[-1], 3, (255, 0, 0), -1)
        if len(pts_inner) > 1:
            # 画线
            for i in range(len(pts_inner) - 1):
                cv2.circle(img2, pts_inner[i], 5, (255, 0, 0), -1)  # x ,y 为鼠标点击地方的坐标
                cv2.line(img=img2, pt1=pts_inner[i], pt2=pts_inner[i + 1], color=(255, 255, 0), thickness=2)
            if event == cv2.EVENT_MBUTTONDOWN:
                cv2.line(img=img2, pt1=pts_inner[len(pts_inner)-1], pt2=pts_inner[0], color=(255, 0, 0), thickness=2)
    cv2.imshow('image', img2)





# 创建图像与窗口并将窗口与回调函数绑定
img = cv2.imread("image.jpg")
img2 = img.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_roi)
print("[INFO] 单击左键：选择点，单击右键：删除上一次选择的点，单击中键：确定ROI区域")
print("[INFO] 按‘S’确定选择区域并保存")
print("[INFO] 按 ESC 退出")


while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    if key == ord("s"):
        saved_data1 = {"ROI1": pts}
        joblib.dump(value=saved_data1, filename="config1.pkl")
        saved_data2 = {"ROI2": pts_inner}
        joblib.dump(value=saved_data2, filename="config2.pkl")

        print("[INFO] ROI坐标已保存到本地.")
        break
cv2.destroyAllWindows()
