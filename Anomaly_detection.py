import cv2
import numpy as np
import joblib

# 最开始计算轮廓会出现异常现象，会出现count =1 的错误
def count_conts(frame, contours, area ):
    count = 0
    for contour in contours:
        if cv2.contourArea(contour) < area:
            continue
        count += 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return count

""" 获取轮廓面积大于预定值的轮廓，用于追踪目标"""
def get_contours(contours,area):
    conts = []
    for contour in contours:
        if cv2.contourArea(contour) < area:
            continue
        conts.append(contour)
    return conts

# def get_area_center(points):
#
#     return (x,y)

"""
    计算区域中心，左中右进行排序
"""
def get_center(pts):
    x = 0
    y = 0


    for i in range(len(pts)):
        x += pts[i][0]
        y += pts[i][1]
    x /= len(pts)
    y /= len(pts)
    x_left = (pts[0][0]+pts[1][0])/2
    y_left = (pts[0][1]+pts[1][1])/2
    x_right = (pts[2][0] + pts[3][0]) / 2
    y_right = (pts[2][1] + pts[3][1]) / 2

    return (int(x),int(y)),(int(x_left),int(y_left)),(int(x_right),int(y_right))

"""
    异常分类：
        单目标异常：
            异常一：穿过区域,代码表示，3s内穿过中心点
            异常二：在异常区停留3s，代码表示3s内未穿过中心点
        todo：多目标异常
"""
if __name__ == '__main__':
    cap = cv2.VideoCapture(1)

    """
        获取手工标记的roi区域
    """
    fgbg = cv2.createBackgroundSubtractorMOG2()
    Roi = joblib.load("config1.pkl")
    pts = Roi.get('ROI1')
    points = np.array(pts, np.int32)
    points = points.reshape((-1, 1, 2))

    """
        获取手工标记的异常区域
    """
    Roi_error = joblib.load("config2.pkl")
    pts_error = Roi_error.get('ROI2')
    points_error = np.array(pts_error, np.int32)
    points_error = points_error.reshape((-1, 1, 2))

    """
        获取异常区域中
    """
    center_point,left_point,right_point = get_center(pts_error)

    print(center_point, left_point, right_point)

    """
        time_count: 解决第一次获取轮廓会获取最外层轮廓的异常现象
    """
    time_count = 0

    """ 
        用于判断异常类型
    """
    frequnence = cv2.getTickFrequency()
    start_time = 0
    flag = 0  # 用于计时，需要保证前后两人进入监控区的时间误差为1s
    error_time_first = 0  # 用于第一次异常判断，判断属于一个物体异常还是两个物体异常
    flag_error_first = 0
    flag_error_second = 0 #用于第二次异常判断
    error_type = 0 # 用于判断异常类型

    while (cap.isOpened):
        success, frame = cap.read()
        if success:
            """ 标记roi区域，为避免影响roi区域以外的区域不进行训练"""
            mask = np.zeros(frame.shape, np.uint8)
            # mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
            mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))  # 用于求 ROI
            mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))  # 用于 显示在桌面的图像
            # show_image = cv2.addWeighted(src1=frame, alpha=0.8, src2=mask3, beta=0.2, gamma=0)
            ROI = cv2.bitwise_and(mask2, frame)  #  获取roi区域掩模
            # cv2.imshow("roi",ROI)
            fgmask_roi = fgbg.apply(ROI)  #  背景减除算法应用
            ret, fgmask_roi = cv2.threshold(fgmask_roi, 254, 255, cv2.THRESH_BINARY) #  获取无阴影的图片
            # kernel = np.ones((3,1),np.uint8)
            # fgmask_roi = cv2.erode(fgmask_roi,kernel) #  腐蚀算法
            frame = cv2.polylines(frame, [points], True, (255, 0, 0), 2)  # 标定监控区域
            frame = cv2.polylines(frame, [points_error], True, (0, 255, 0), 2)
            frame = cv2.circle(frame, center_point, 3, (0, 0, 255), -1)
            frame = cv2.circle(frame, left_point, 3, (0, 0, 255), -1)
            frame = cv2.circle(frame, right_point, 3, (0, 0, 255), -1)

            contours, _ = cv2.findContours(fgmask_roi, cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            """
                直接跳过第一帧的画面从第二帧开始算起
            """
            if time_count == 0:
                time_count += 1
                continue
            count = count_conts(frame,contours,7000)




            """ 当检测区域中出现第一个异常开始计时判断异常"""
            if count == 1 and flag == 0 :
                start_time = cv2.getTickCount()
                error_time_first = start_time
                flag = 1
                # print(start_time)

            """ 保证err_time_first在start_time计时之后开始计时"""
            if flag == 1:
                error_time_first = cv2.getTickCount()
                if (error_time_first-start_time)/frequnence > 0.7 and flag_error_first == 0:
                    if count == 1:
                        print("属于第一大类异常")
                        flag_error_first = 1
                    else:
                        print("属于第二大类异常")
                        flag_error_first = 2
                    flag =2

            """若异常为第一大异常"""
            if flag_error_first == 1:
                # print("判断第一大类异常")
                conts = get_contours(contours,7000)
                # print(conts[0])
                if conts:   # 如果轮廓不为空

                    dist = cv2.pointPolygonTest(conts[0],center_point,False)
                    # print(dist)
                    if dist == 1.0 and flag_error_second == 0:
                        start_time = cv2.getTickCount()
                        # print("error1 starttime= ", start_time)
                        error_time_first = start_time
                        flag_error_second = 1
                    if flag_error_second == 1:

                        dist1 = cv2.pointPolygonTest(conts[0], left_point, False)
                        error_time_first = cv2.getTickCount()
                        if dist1 == 1.0 and dist == -1:
                            print("发生异常1")
                            error_type = 1
                            flag_error_first = 3

                        elif (error_time_first-start_time)/frequnence > 1:

                            dist2 = cv2.pointPolygonTest(conts[0],right_point,False)
                            # if dist == -1:
                            #     print("发生异常1")
                            #     error_type =1
                            #
                            # else:
                            #     error_type = 2
                            #     print("发生异常2")

                            if dist2 == 1:
                                print("发生异常3")
                                error_type = 3
                                flag_error_first = 3
                            elif (error_time_first-start_time)/frequnence > 3:
                                print("发生异常2")
                                error_type = 2
                                flag_error_first = 3

            elif flag_error_first==2:
                """若异常为第二大类异常"""
                # print("判断第一大类异常")
                conts = get_contours(contours, 7000)
                # print(conts[0])
                if conts:
                    dist = cv2.pointPolygonTest(conts[0], center_point, False)

                    if dist == 1 and flag_error_second==0:
                        start_time = cv2.getTickCount()
                        error_time_first = start_time
                        flag_error_second = 1
                    if flag_error_second == 1:
                        error_time_first = cv2.getTickCount()
                        if (error_time_first-start_time)/frequnence > 2:
                            if len(conts)>1:
                                print("发生异常4")
                                error_type =4

                            else:
                                error_type = 5
                                print("发生异常5")
                            flag_error_first = 3
                    # print("判断第二大类异常")


            if error_type == 1:
                frame = cv2.putText(frame, 'Error Happening, Error Type: 1', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                    (0, 0, 255), 2)
            elif error_type ==2:
                frame = cv2.putText(frame, 'Error Happening, Error Type: 2', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                    (0, 0, 255), 2)
            elif error_type == 3:
                frame = cv2.putText(frame, 'Error Happening, Error Type: 3', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                    (0, 0, 255), 2)
            elif error_type == 4:
                frame = cv2.putText(frame, 'Error Happening, Error Type: 4', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                    (0, 0, 255), 2)
            elif error_type == 5:
                frame = cv2.putText(frame, 'Error Happening, Error Type: 5', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                    (0, 0, 255), 2)

            cv2.namedWindow("src",cv2.WINDOW_NORMAL)
            cv2.resizeWindow("src",800,600)
            cv2.imshow("src", frame)
            cv2.namedWindow("mask", cv2.WINDOW_KEEPRATIO)
            cv2.resizeWindow("mask", 800, 600)
            cv2.imshow("mask", fgmask_roi)
            key = cv2.waitKey(1) & 0xFF
            '''重置'''
            if key == ord('r'):
                print("重置实验")
                start_time = 0
                flag = 0  # 用于计时，需要保证前后两人进入监控区的时间误差为1s
                error_time_first = 0  # 用于第一次异常判断，判断属于一个物体异常还是两个物体异常
                flag_error_first = 0
                flag_error_second = 0  # 用于第二次异常判断
                error_type = 0  # 用于判断异常类型

            if key == ord('q'):
                break
        else:
            break
cap.release()
cv2.destroyAllWindows()


