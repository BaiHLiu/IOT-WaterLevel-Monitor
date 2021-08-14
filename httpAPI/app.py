#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 4:21 下午
# @Author  : Catop
# @File    : app.py
# @Software: 提供tcp-server回调接口，保存设备查询数据

from flask import Flask, request, jsonify
import dbconn
from flask_cors import *
from conf import Config


app = Flask(__name__)
CORS(app, supports_credentials=True)



@app.route('/', methods=['GET'])
def index():
    dev_name = request.args.get('dev_name')
    return f"dev_name = {dev_name}"


@app.route('/upload', methods=['GET'])
def upload_log():
    ret_dict = {}
    try:
        # 串口服务器信息
        ip = request.args.get('ip')
        port = request.args.get('port')
        dev_id = dbconn.get_dev_id(port)
        # 获取传感器id
        sensor_address = request.args.get('sensor_address')
        sensor_id = dbconn.get_sensor_id(dev_id, sensor_address)
        # 距离和温度处理值信息
        distance = request.args.get('distance')
        temperature = request.args.get('temperature')

        dbconn.add_log(dev_id, ip, sensor_id, distance, temperature)
        ret_dict['code'] = 0
        return jsonify(ret_dict)

    except:
        ret_dict['code'] = 1
        return jsonify(ret_dict)


@app.route('/get_query_params', methods=['GET'])
def get_query_params():
    dev_port = str(request.args.get('dev_port'))
    params = dbconn.get_query_info(dev_port)

    return jsonify(params)




if __name__ == '__main__':
    app.run(host=Config.http_api['bind_address'], port=Config.http_api['bind_port'])
