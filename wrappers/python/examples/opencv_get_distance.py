# coding: utf-8

import pyrealsense2 as rs
import cv2
import numpy as np


# マウスイベント時に処理を行う
def mouse_event(event, x, y, flags, param):
    depth_frame = param
    distance = depth_frame.get_distance(x, y)
    # 左クリックで座標を返す
    if event == cv2.EVENT_LBUTTONUP:
        return print(distance)


# ストリーム(Depth/Color)の設定
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)


try:
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not depth_frame or not color_frame:
            continue
        # ndarrayに変換
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        # ヒートマップに変換
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.08), cv2.COLORMAP_JET)
        # レンダリング
        images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

        # マウスイベント時に関数mouse_eventの処理を行う
        cv2.setMouseCallback('RealSense', mouse_event, depth_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # ストリーミング停止
    pipeline.stop()
    cv2.destroyAllWindows()
