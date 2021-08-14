#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 10:32 下午
# @Author  : Catop
# @File    : conf.py
# @Software: PyCharm

class Config:
    tcp_server = {
        "bind_address": "",
        "bind_port": 10123,
        "max_connections": 128,
        "http_api_endpoint": "http://127.0.0.1:5001"
    }

    http_api = {
        "bind_address": "0.0.0.0",
        "bind_port": 5001
    }

    web_app = {
        "bind_address": "0.0.0.0",
        "bind_port": 5002
    }
