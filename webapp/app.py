#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 5:55 下午
# @Author  : Catop
# @File    : app.py
# @Software: flask后端主程序

from flask import Flask, request, jsonify
from flask_cors import *
import dbconn
import sys 
sys.path.append("..") 
from conf import Config

app = Flask(__name__)
CORS(app, supports_credentials=True)


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
            'interval_time': dev[6],
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
                    'sensor_name': dbconn.get_sensor_info(sens['sensor_id'])[1]

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


def get_device():
    """添加新设备"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    dev_name = request.args.get('dev_name')
    dev_port = request.args.get('dev_port')
    interval_time = request.args.get('interval_time')
    alarm_params = request.args.get('alarm_params')
    distance_query_arg = request.args.get('distance_query_arg')
    temperature_query_arg = request.args.get('temperature_query_arg')

    try:
        dbconn.add_dev(dev_name, dev_port, interval_time, distance_query_arg, temperature_query_arg, alarm_params)
    except:
        ret_dict['code'] = -1
        ret_dict['msg'] = "设备添加失败"

    return jsonify(ret_dict)


@app.route('/get_devices_config')
def get_devices_config():
    """获取设备配置信息"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}
    try:
        ret_dict['body'] = dbconn.get_all_dev_info()
    except:
        ret_dict['code'] = -1
        ret_dict['msg'] = "获取设备配置信息失败"

    return jsonify(ret_dict)


@app.route('/get_sensors_config')
def get_sensors_config():
    """获取指定设备传感器信息"""
    dev_id = request.args.get('dev_id')
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    ret_dict['body'] = dbconn.get_sensors(dev_id)

    return jsonify(ret_dict)


@app.route('/modify_device_config')
def modify_device_config():
    """修改指定设备配置信息"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    dev_id = request.args.get('dev_id')
    dev_name = request.args.get('dev_name')
    dev_port = request.args.get('dev_port')
    alarm_params = request.args.get('alarm_params')
    interval_time = request.args.get('interval_time')
    distance_query_arg = request.args.get('distance_query_arg')
    temperature_query_arg = request.args.get('temperature_query_arg')

    try:
        dbconn.modify_device_config(dev_id, dev_name, dev_port, alarm_params, interval_time, distance_query_arg, temperature_query_arg)
    except:
        ret_dict['code'] = -1
        ret_dict['msg'] = "修改配置信息失败"



    return jsonify(ret_dict)


@app.route('/modify_sensor_config')
def modify_sensor_config():
    """修改传感器配置"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    sensor_id = request.args.get('sensor_id')
    sensor_name = request.args.get('sensor_name')
    distance_offset = request.args.get('distance_offset')
    hex_address = request.args.get('hex_address')
    home_graph = request.args.get('home_graph')

    try:
        dbconn.modify_sensor_config(sensor_id, sensor_name, distance_offset, hex_address, home_graph)
    except:
        ret_dict['code'] = -1

    return jsonify(ret_dict)


@app.route('/add_sensor')
def add_sensor():
    """新增传感器"""
    # 用户添加传感器时只需要输入名称，其他配置使用"修改配置"接口
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    sensor_name = request.args.get('sensor_name')
    bind_dev_id = request.args.get('bind_dev_id')

    try:
        dbconn.add_sensor(bind_dev_id, sensor_name, 0, "")
    except:
        ret_dict['code'] = -1

    return jsonify(ret_dict)


@app.route('/rm_sensor')
def rm_sensor():
    """删除传感器"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    sensor_id = request.args.get('sensor_id')
    try:
        dbconn.rm_sensor(sensor_id)
    except:
        ret_dict['code'] = -1

    return jsonify(ret_dict)


@app.route('/add_device')
def add_device():
    """新增串口服务器"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}
    # 用户添加串口服务器时只需要输入名称，其他配置使用"修改配置"接口
    dev_name = request.args.get('dev_name')

    try:
        dbconn.add_dev(dev_name,'',10,'','','')
    except:
        ret_dict['code'] = -1

    return jsonify(ret_dict)


@app.route('/rm_device')
def rm_device():
    """删除串口服务器"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}
    dev_id = request.args.get('dev_id')

    try:
        dbconn.rm_device(dev_id)
    except:
        ret_dict['code'] = -1

    return jsonify(ret_dict)


@app.route('/set_offset')
def set_offset():
    """设置偏移值"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}

    sensor_id = request.args.get('sensor_id')
    offset = request.args.get('offset')

    try:
        dbconn.set_offset(sensor_id, offset)
    except:
        ret_dict['code'] = -1

    return jsonify(ret_dict)


@app.route('/get_distance')
def get_distance():
    """获取测量值"""
    ret_dict = {'code': 0, 'msg': "", 'body': None}
    sensor_id = request.args.get('sensor_id')

    try:
        ret_dict['body'] = dbconn.get_sensor_distance(sensor_id)

    except:
        ret_dict['code'] = -1

    return  jsonify(ret_dict)


if __name__ == '__main__':
    app.run(host=Config.web_app['bind_address'], port=Config.web_app['bind_port'])

