#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 5:55 下午
# @Author  : Catop
# @File    : app.py
# @Software: flask后端主程序

from flask import Flask, request, jsonify
from flask_cors import *
import dbconn

app = Flask(__name__)
CORS(app, supports_credentials=True)

# json响应模板
resp_template = {'code': 0, 'msg': "", 'body': None}


@app.route('/get_devices_info')
def get_devices_info():
    """获取所有设备简要信息"""
    ret_dict = []
    devs = dbconn.get_all_dev_info()
    # print(devs)
    for dev in devs:
        dev_info = {
            'id': dev[0],
            'name': dev[1],
            'update_time': dev[3],
            'ip': None,
            'interval_time':dev[6],
            'data': []
        }
        # 获取最新上报信息
        dev_upload_msg = dbconn.get_newest_record(dev[0])
        if (dev_upload_msg):
            # 用传感器ip代替串口服务器ip
            dev_info['ip'] = dev_upload_msg[0]['dev_ip']
            # print(dev_upload_msg)
            for sens in dev_upload_msg:
                sen_info = {
                    'high_level': dbconn.get_water_level(sens['sensor_id'], sens['distance']),
                    'temperature': sens['temperature'],
                    'sensor_name' : dbconn.get_sensor_info(sens['sensor_id'])[1]

                }
                dev_info['data'].append(sen_info)

            ret_dict.append(dev_info)

        else:
            pass

    return jsonify(ret_dict)


@app.route('/get_history')
def get_history():
    """获取历史值"""
    dev_id = request.args.get('dev_id')
    number = request.args.get('number')

    his_list = dbconn.get_recent_records(dev_id, number)

    return jsonify(his_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
