#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 4:21 下午
# @Author  : Catop
# @File    : dbconn.py
# @Software: PyCharm

from datetime import datetime
import sqlite3

conn = sqlite3.connect("../db.sqlite", check_same_thread=False)

def add_log(dev_id, dev_ip, sensor_id, sensor_distence, sensor_temperature):
    """用于tcp-server主动上报"""
    # 写入upload_log
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = conn.cursor()
    sql = "INSERT INTO upload_log(dev_id,dev_ip,sensor_id,sensor_distance,sensor_temperature,datetime) VALUES(?,?,?,?,?,?)"
    params = [dev_id, dev_ip, sensor_id, sensor_distence, sensor_temperature, now_time]
    cur.execute(sql, params)

    # 更新dev_info中统计信息
    sql = "UPDATE dev_info SET last_upload_datetime=?,upload_count=upload_count+1 WHERE dev_id=?"
    params = [now_time, dev_id]
    cur.execute(sql, params)

    conn.commit()

def get_query_info(dev_port):
    """返回指定设备的传感器信息和查询参数"""
    ret_dict = {}

    cur = conn.cursor()
    sql = "SELECT distance_query_arg,temperature_query_arg,interval_time FROM dev_info WHERE dev_id=?"
    params = [get_dev_id(dev_port)]
    cur.execute(sql, params)
    sql_ret = cur.fetchone()

    #查询参数列表
    ret_dict['args_list'] = [sql_ret[0], sql_ret[1]]

    #设置轮询时间
    ret_dict['interval_time'] = sql_ret[2]

    #拼接传感器地址码
    sql = "SELECT distance_offset, hex_address FROM sensor_info WHERE bind_dev_id=?"
    cur.execute(sql, params)
    sql_ret = cur.fetchall()
    ret_dict['sensors_list'] = []
    for sens in sql_ret:
        sensor_info = {
            "distance_offset" : sens[0],
            "hex_address" : sens[1]
        }

        ret_dict['sensors_list'].append(sensor_info)

    return ret_dict


def get_dev_id(dev_port):
    """查询指定端口设备的id"""
    cur = conn.cursor()
    sql = "SELECT dev_id FROM dev_info WHERE dev_port=?"
    params = [dev_port]
    cur.execute(sql, params)
    ret = cur.fetchone()

    return ret[0]

def get_sensor_id(bind_dev_id, sensor_address):
    """查询传感器id"""
    cur = conn.cursor()
    sql = "SELECT sensor_id FROM sensor_info WHERE (bind_dev_id=? AND hex_address=?) LIMIT 1"
    params = [bind_dev_id, sensor_address]
    cur.execute(sql, params)
    sensor_id = cur.fetchone()[0]

    return  sensor_id

if __name__ == "__main__":
    #add_log('127.0.0.1','6002',1211,37.2)
    #print(get_query_info('2000'))
    #print(get_dev_id('2000'))
    print(get_sensor_id(3, '01'))