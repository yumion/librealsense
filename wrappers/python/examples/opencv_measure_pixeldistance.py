# coding: utf-8

import cv2
import numpy as np
from realsensecv import RealsenseCapture

distance = None
left_click = [None, None]
right_click = [None, None]


# マウスイベント時に処理を行う
def mouse_event(event, x, y, flags, param):
    global distance, left_click, right_click
    depth_frame = param
    distance = depth_frame.get_distance(x, y)
    # 左クリックで座標を返す
    if event == cv2.EVENT_LBUTTONUP:
        left_click = [x, y]
    elif event == cv2.EVENT_MBUTTONUP:
        right_click = [x, y]
    if left_click[0] is not None and right_click[0] is not None:
        print(f'distance: {distance} \nwidth: {(0.0016 * distance * 100 + 0.0006) * abs(left_click[0] - right_click[0])}')
        left_click = [None, None]
        right_click = [None, None]


cap = RealsenseCapture()
# cap.WIDTH = 1280
# cap.HEIGHT = 720
# cap.FPS = 30
cap.start()


while True:
    ret, frames = cap.read(is_filtered=False)
    color_frame = frames[0]
    depth_frame = frames[1]
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
