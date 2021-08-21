#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/20 11:16 下午
# @Author  : Catop
# @File    : rtsp.py
# @Software: PyCharm


import cv2
from datetime import datetime
from camConf import Config


def get_img_from_camera_net(folder_path):
    camList = Config.camList
    for cam in camList.keys():
        try:
            name = cam
            url = camList[name]

            cap = cv2.VideoCapture(url)  # 获取网络摄像机
            ret, frame = cap.read()
            # cv2.imshow("capture", frame)
            file_name = f'{name}.jpg'
            cv2.imwrite(folder_path + file_name, frame, [cv2.IMWRITE_JPEG_QUALITY,80])  # 存储为图像
            cap.release()
            cv2.destroyAllWindows()
            print(f'[+]Successfully:{name} in {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        except:
            print(f'[!]Failed:{name} in {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')



# 测试
if __name__ == '__main__':
    folder_path = '/home/ClassBot/changZheng/compressed/wateriot/img'
    get_img_from_camera_net(folder_path)