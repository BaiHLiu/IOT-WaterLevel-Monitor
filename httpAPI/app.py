#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 4:21 下午
# @Author  : Catop
# @File    : app.py
# @Software: 提供tcp-server回调接口，保存设备查询数据
import json
import importlib

from flask import Flask, request, jsonify
import dbconn
from flask_cors import *
import sys
import datetime
sys.path.append("..")
from conf import Config
from msgPush import push
import redisCache.cache

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
        importlib.reload(dbconn)
        ip = request.args.get('ip')
        port = request.args.get('port')
        dev_id = dbconn.get_dev_id(port)
        # 获取传感器id
        sensor_address = request.args.get('sensor_address')
        sensor_id = dbconn.get_sensor_id(dev_id, sensor_address)
        # 距离和温度处理值信息
        distance = request.args.get('distance')
        temperature = request.args.get('temperature')

        # redis缓存
        redisCache.cache.redis_add_log(sensor_id, dev_id, ip, distance, temperature)
        # mysql持久化
        dbconn.add_log(dev_id, ip, sensor_id, distance, temperature)

        # 获取设备和传感器名称
        dev_name = dbconn.get_dev_info(dev_id)[1]
        sensor_name = dbconn.get_sensor_info(sensor_id)[1]

        # 报警推送
        push_alarm(dev_id, sensor_id, distance, dev_name, sensor_name)

        ret_dict['code'] = 0
        return jsonify(ret_dict)
    except:
        ret_dict['code'] = 1
        return jsonify(ret_dict)


@app.route('/get_query_params', methods=['GET'])
def get_query_params():

    importlib.reload(dbconn)
    dev_port = str(request.args.get('dev_port'))
    if (dbconn.check_exist(dev_port)):
        params = dbconn.get_query_info(dev_port)
    else:
        params = {'sensors_list': []}

    return jsonify(params)


def push_alarm(dev_id, sensor_id, distance, dev_name, sensor_name):
    """报警推送"""
    msg_str = f"## 水位监控告警\n+ 监测点:{dev_name}\n+ 传感器:{sensor_name}\n"
    ALARM_INTERVAL_LINE = 180       # 高低水位超限报警间隔
    ALARM_INTERVAL_CHANGE = 60      # 变化水位超限报警间隔

    importlib.reload(dbconn)
    alarm_params = json.loads(dbconn.get_alarm_params(dev_id))
    water_level = int(dbconn.get_water_level(sensor_id, int(distance)))
    low_line = int(alarm_params[1])
    high_line = int(alarm_params[0])
    time_line = int(alarm_params[2])
    delta_line = int(alarm_params[3])

    if (not (high_line == 0)) and (not (low_line == 0)):
        # 超过高低警戒水位
        if (water_level < low_line or water_level > high_line):
            alarm_log = dbconn.get_alarm_log(dev_id)
            if (not alarm_log):
                # 没报警过
                push.send_message(
                    msg_str + f"+ 告警类型：高低水位超限\n+ 水位值：{water_level} 毫米\n+ 预警值:{low_line}/{high_line} 毫米")
                dbconn.set_alarm_log(sensor_id, dev_id, 1, water_level)
            else:
                # 报警过
                time_delta = int(((datetime.datetime.now() - datetime.datetime.strptime(alarm_log[5],
                                                                                        '%Y-%m-%d %H:%M:%S')).seconds) / 60)
                # 同种类型报警（高低警戒线）
                if (time_delta > ALARM_INTERVAL_LINE):
                    # 符合时间间隔
                    push.send_message(
                        msg_str + f"+ 告警类型：高低水位超限\n+ 水位值：{water_level} 毫米\n+ 预警值:{low_line}/{high_line} 毫米")
                    dbconn.set_alarm_log(sensor_id, dev_id, 1, water_level)

    if (not (time_line == 0)) and (not (delta_line == 0)):
        # 水位变化告警
        before_level = dbconn.get_min_before_record(dev_id, time_line)
        for sen in before_level:
            if (sen[0] == sensor_name) and (abs(sen[1] - water_level) > delta_line):
                alarm_log = dbconn.get_alarm_log(dev_id)
                if (not alarm_log):
                    push.send_message(
                        msg_str + f"+ 告警类型：水位变化速率超限\n+ 时间范围：{time_line} 分钟\n+ 变化值：{str(sen[1] - water_level)} mm\n+ 预警值:{time_line} 分钟内 变化 {delta_line} mm")
                    dbconn.set_alarm_log(sensor_id, dev_id, 2, water_level)
                else:
                    time_delta = int(((datetime.datetime.now() - datetime.datetime.strptime(alarm_log[5],
                                                                                            '%Y-%m-%d %H:%M:%S')).seconds) / 60)
                    if (time_delta > ALARM_INTERVAL_CHANGE):
                        push.send_message(
                            msg_str + f"+ 告警类型：水位变化速率超限\n+ 时间范围：{time_line} 分钟\n+ 变化值：{str(sen[1] - water_level)} mm\n+ 预警值:{time_line} 分钟内 变化 {delta_line} mm")
                        dbconn.set_alarm_log(sensor_id, dev_id, 2, water_level)





if __name__ == '__main__':
    app.run(host=Config.http_api['bind_address'], port=Config.http_api['bind_port'])
