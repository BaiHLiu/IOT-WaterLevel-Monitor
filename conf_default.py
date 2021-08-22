#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/16 3:04 下午
# @Author  : Catop
# @File    : pushconf_default.py
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

    msg_push = {
        "topic_ids": [''],
        "token": ''
    }

    user = {
        "admin": {
            "username": "admin",
            "password": "12345"
        },
        "viewer": {
            "username": "guest",
            "password": "12345"
        }
    }