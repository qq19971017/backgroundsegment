import cv2
import numpy as np

class video:
    def readVideo(self, path):
        my_video = cv2.VideoCapture(path)
        while(1):
            ret, frame = my_video.read()
            cv2.imshow("original", frame)
            k = cv2.waitKey(30)& 0xff
            if(k == 27):
                break
        my_video.release()
        cv2.destroyAllWindows()

    def readVideo2(self):
        camera = cv2.VideoCapture(1)
        while True:
            # 从摄像头读取图片
            sucess, img = camera.read()
            # 显示摄像头，背景是灰度。
            cv2.imshow("img", img)
            # 保持画面的持续。
            k = cv2.waitKey(1)
            if k == 27:
                # 通过esc键退出摄像
                cv2.destroyAllWindows()
                break
            elif k == ord("s"):
                # 通过s键保存图片，并退出。
                cv2.imwrite("image2.jpg", img)
        # 关闭摄像头
        camera.release()