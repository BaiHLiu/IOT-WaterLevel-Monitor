#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/2 3:35 PM
# @Author  : Catop
# @File    : cache.py
# @Software: PyCharm

import redis
import sys
from datetime import datetime

sys.path.append("..")
from httpAPI import dbconn as devDB
from webApp import dbconn as webDB

rds = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def redis_add_log(sensor_id, dev_id, ip, distance, temperature):
    sensor_info = webDB.get_sensor_info(sensor_id)
    logMap = {
        'dev_id': dev_id,
        'ip': ip,
        'distance': distance,
        'temperature': temperature,
        'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'max_line': webDB.get_dev_by_id(dev_id)[4][1:-2].split(', ')[0],
        'offset': sensor_info[3],
        'home_graph': sensor_info[6],
        'sensor_name': sensor_info[1],

    }

    return rds.hmset(sensor_id, logMap)


def redis_get_newest_record(dev_id):
    sensors_list = webDB.get_sensors(dev_id)
    ret_list = []

    for sens in sensors_list:
        rdsRet = rds.hgetall(sens[0])
        if rdsRet:
            sensor_record = {
                'dev_ip': rdsRet['ip'],
                'sensor_id': sens[0],
                'distance': int(rdsRet['distance']),
                'temperature': int(rdsRet['temperature']),
                'offset': int(rdsRet['offset']),
                'update_time': rdsRet['datetime'],
                'max_line': int(rdsRet['max_line']),
                'home_graph': int(rdsRet['home_graph']),
                'sensor_name': rdsRet['sensor_name']
            }
        ret_list.append(sensor_record)

    return ret_list


if __name__ == '__main__':
    print(redis_add_log(9, 13, '10.9.0.2', 3607, 304))
    print(redis_add_log(11, 13, '10.9.0.2', 3607, 304))
    print(redis_get_newest_record(13))
