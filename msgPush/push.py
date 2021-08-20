#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/17 9:09 上午
# @Author  : Catop
# @File    : push.py
# @Software: 消息推送模块
from wxpusher import WxPusher
from conf import Config

def send_message(content):
    # try:
    ret = WxPusher.send_message(content,
          content_type=3,
          topic_ids=Config.msg_push['topic_ids'],
          token=Config.msg_push['token'])
    if(ret['code'] == 1000):
        return 0
    else:
        return -1
    # except:
        return -1


if __name__ == "__main__":
    print(send_message("# Hello!\n#hello"))