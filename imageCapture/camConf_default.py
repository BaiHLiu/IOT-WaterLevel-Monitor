#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/21 8:19 上午
# @Author  : Catop
# @File    : camConf_default.py
# @Software: PyCharm

class Config:
    camList = {
        '城东-闸前':'rtsp://admin:passwd@192.168.123.180:9999/cam/realmonitor?channel=1&subtype=1',
        '城北-闸前':'rtsp://admin:passwd@192.168.123.180:9999/cam/realmonitor?channel=2&subtype=1'
    }