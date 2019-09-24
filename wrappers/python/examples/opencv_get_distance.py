# coding: utf-8

import cv2
import numpy as np
from realsensecv import RealsenseCapture


# マウスイベント時に処理を行う
def mouse_event(event, x, y, flags, param):
    depth_frame = param
    distance = depth_frame.get_distance(x, y)
    # 左クリックで座標を返す
    if event == cv2.EVENT_LBUTTONUP:
        return print(distance)


cap = RealsenseCapture()
cap.WIDTH = 1280
cap.HEIGHT = 960
cap.FPS = 30
cap.start()


while True:
    ret, frames = cap.read(is_filtered=True)
    color_frame = frames[0]
    depth_frame = frames[1]
    # print(color_frame.shape, depth_frame.shape)
    # レンダリング
    images = np.hstack((color_frame, depth_frame))
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)

    # マウスイベント時に関数mouse_eventの処理を行う
    cv2.setMouseCallback('RealSense', mouse_event, cap.depth_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ストリーミング停止
cap.release()
cv2.destroyAllWindows()
