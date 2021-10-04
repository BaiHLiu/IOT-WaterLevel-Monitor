#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 5:56 下午
# @Author  : Catop
# @File    : dbconn.py
# @Software: Flask后端数据库连接
import json
from datetime import datetime
import datetime as dt
import sqlite3

conn = sqlite3.connect("../db.sqlite", check_same_thread=False)


def add_dev(dev_name, dev_port, interval_time, distance_query_arg, temperature_query_arg, alarm_params):
    """添加新设备"""
    cur = conn.cursor()
    sql = "INSERT INTO dev_info(dev_name,dev_port,interval_time,distance_query_arg,temperature_query_arg,alarm_params) VALUES(?,?,?,?,?,?)"
    params = [dev_name, dev_port, interval_time, distance_query_arg, temperature_query_arg, alarm_params]

    cur.execute(sql, params)
    conn.commit()


def add_sensor(bind_dev_id, sensor_name, distance_offset, hex_address):
    """添加新传感器"""
    cur = conn.cursor()
    sql = "INSERT INTO sensor_info(bind_dev_id,sensor_name,distance_offset,hex_address) VALUES (?,?,?,?)"
    params = [bind_dev_id, sensor_name, distance_offset, hex_address]

    cur.execute(sql, params)
    conn.commit()


def get_all_dev_info():
    """查询所有设备信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM dev_info"
    cur.execute(sql)
    rets = cur.fetchall()

    return rets


def get_dev_by_id(dev_id):
    """查询指定id的设备信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM dev_info WHERE dev_id=?"
    params = [dev_id]
    cur.execute(sql, params)
    rets = cur.fetchone()

    return rets


def get_dev_id(dev_port):
    """查询指定端口设备的id"""
    cur = conn.cursor()
    sql = "SELECT dev_id FROM dev_info WHERE dev_port=?"
    params = [dev_port]
    cur.execute(sql, params)
    ret = cur.fetchone()

    return ret[0]


def get_dev_port(dev_id):
    """查询指定id的设备端口"""
    cur = conn.cursor()
    sql = "SELECT dev_port FROM dev_info WHERE dev_id=?"
    params = [dev_id]
    cur.execute(sql, params)
    ret = cur.fetchone()

    return ret[0]


def modify_dev(dev_id, dev_name, dev_port, alarm_params, interval_time):
    """配置串口服务器参数"""
    cur = conn.cursor()
    sql = "UPDATE dev_info SET dev_name=?,dev_port=?,alarm_params=?,interval_time=? WHERE dev_id=?"
    params = [dev_name, dev_port, alarm_params, interval_time]
    cur.execute(sql, params)
    conn.commit()


def get_period_record(sensor_id, start_time, end_time):
    """获取指定设备time_m内历史记录"""
    cur = conn.cursor()
    sql = "SELECT * FROM upload_log WHERE(datetime>=? AND datetime<=? AND sensor_id=?)"
    params = [start_time, end_time, sensor_id]
    cur.execute(sql, params)
    ret = cur.fetchall()

    return ret


def get_newest_record(dev_id, number=1):
    """获取指定设备指定条数历史记录"""
    # 指定条数已弃用，改为 get_recent_records(dev_id, number)
    sensors_list = get_sensors(dev_id)
    ret_list = []

    for sens in sensors_list:
        cur = conn.cursor()
        sql = "SELECT * FROM upload_log WHERE (dev_id=? AND sensor_id=?) ORDER BY datetime DESC LIMIT 1"
        params = [dev_id, sens[0]]
        cur.execute(sql, params)
        sql_ret = cur.fetchone()
        if (sql_ret):
            sensor_record = {
                'dev_ip': sql_ret[2],
                'sensor_id': sql_ret[3],
                'distance': sql_ret[4],
                'temperature': sql_ret[5],
                'offset': sens[3],
                'update_time': sql_ret[6]
            }

            ret_list.append(sensor_record)

    return ret_list


def get_recent_records(dev_id, number):
    """获取指定设备各个传感器最近number条记录"""
    cur = conn.cursor()
    sensor_number = len(get_sensors(dev_id))
    sql = "SELECT * FROM upload_log WHERE dev_id=? ORDER BY datetime DESC LIMIT ?"
    params = [dev_id, number * sensor_number]
    cur.execute(sql, params)

    sql_ret = cur.fetchall()
    ret_dict = {}
    for log in sql_ret:
        sensor_id = log[3]
        sensor_name = get_sensor_info(sensor_id)[1]
        if (sensor_name in ret_dict.keys()):
            ret_dict[sensor_name].append((
                get_water_level(sensor_id, log[4]), log[5], log[6]
            ))
        else:
            ret_dict[sensor_name] = []
            ret_dict[sensor_name].append((
                get_water_level(sensor_id, log[4]), log[5], log[6]
            ))

    return ret_dict


def get_sensors(dev_id):
    """获取绑定指定设备的传感器信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM sensor_info WHERE bind_dev_id=?"
    params = [dev_id]
    cur.execute(sql, params)

    return cur.fetchall()


def get_water_level(sensor_id, distance):
    """获取指定传感器的真实值"""
    # 计算公式：真实值(level) = 偏差值(offset) - 距离值(distance)
    cur = conn.cursor()
    sql = "SELECT distance_offset FROM sensor_info WHERE sensor_id=? LIMIT 1"
    params = [sensor_id]

    cur.execute(sql, params)
    offset = cur.fetchone()[0]

    return offset - distance


def get_sensor_info(sensor_id):
    """获取传感器信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM sensor_info WHERE sensor_id=?"
    params = [sensor_id]
    cur.execute(sql, params)

    return cur.fetchone()


def modify_device_config(dev_id, dev_name, dev_port, alarm_params, interval_time, distance_query_arg,
                         temperature_query_arg):
    """修改设备信息"""
    cur = conn.cursor()
    sql = "UPDATE dev_info SET dev_name=?,dev_port=?,alarm_params=?,interval_time=?,distance_query_arg=?,temperature_query_arg=? " \
          "WHERE dev_id=? "
    params = [dev_name, dev_port, alarm_params, interval_time, distance_query_arg, temperature_query_arg, dev_id]
    cur.execute(sql, params)

    conn.commit()


def modify_sensor_config(sensor_id, sensor_name, distance_offset, hex_address, home_graph):
    """修改传感器信息"""
    cur = conn.cursor()
    sql = "UPDATE sensor_info SET sensor_name=?,distance_offset=?,hex_address=?,home_graph=? WHERE sensor_id=?"
    params = [sensor_name, distance_offset, hex_address, home_graph, sensor_id]

    cur.execute(sql, params)

    conn.commit()


def rm_sensor(sensor_id):
    """删除传感器"""
    cur = conn.cursor()
    sql = "DELETE FROM sensor_info WHERE sensor_id=?"
    params = [sensor_id]

    cur.execute(sql, params)

    conn.commit()


def rm_device(dev_id):
    """删除串口服务器"""
    cur = conn.cursor()
    sql = "DELETE FROM dev_info WHERE dev_id=?"
    params = [dev_id]

    cur.execute(sql, params)

    conn.commit()


def set_offset(sensor_id, offset):
    """快速设置偏移值"""
    cur = conn.cursor()
    sql = "UPDATE sensor_info SET distance_offset=? WHERE sensor_id=?"
    params = [offset, sensor_id]

    cur.execute(sql, params)

    conn.commit()

# TODO:get_sensor_distance改为redis调用
def get_sensor_distance(sensor_id):
    """获取指定设备最新测量值"""
    cur = conn.cursor()
    sql = "SELECT sensor_distance from upload_log WHERE sensor_id=? ORDER BY datetime DESC LIMIT 1"
    params = [sensor_id]

    cur.execute(sql, params)
    distance = cur.fetchone()[0]

    return distance


def set_ground_level(sensor_id, ground_level):
    """设置底板高度"""
    cur = conn.cursor()
    sql = "UPDATE sensor_info SET ground_level=? WHERE sensor_id=?"
    params = [ground_level, sensor_id]

    cur.execute(sql, params)

    conn.commit()


def set_alarm_param(dev_id, max_level, min_level, time_delta, level_delta):
    """设置报警参数"""
    cur = conn.cursor()
    sql = "UPDATE dev_info SET alarm_params=? WHERE dev_id=?"
    alarm_list = [
        max_level,
        min_level,
        time_delta,
        level_delta
    ]

    params = [json.dumps(alarm_list), dev_id]
    cur.execute(sql, params)
    conn.commit()


if __name__ == "__main__":
    # add_dev("测试地点",'6002')
    # print(get_all_dev_info()[0])
    # modify_dev(1, "新地点", '1234', 1023)
    # print(type(get_dev_port('1')))
    # now_time = datetime.now()
    # start_time = now_time - dt.timedelta(minutes=200)
    # print(get_recent_record(2, start_time, now_time))
    # print(get_newest_record(4))
    # print(get_sensors(4))

    # print(get_water_level(3,100))
    # print(get_newest_record(4, 10))
    # print(get_recent_records(4, 10))

    # add_dev("模拟站点", "3000", 5, "03 01 00 00 01", "03 01 02 00 01")
    # add_sensor(4,"模拟距离2",400,'02')

    # rm_sensor(8)
    # print(get_all_dev_info())
    # modify_device_config(4, "新名称5", 2002, '',5, "03 01 00 00 01", "03 01 02 00 01")

    # add_dev('hello', '', 10, '', '', '')
    # print(get_sensor_distance(3))
    # set_offset(3,100)
    # set_alarm_param(3,0,0,30,1000)
    # print(get_dev_by_id(3))
    print(get_all_dev_info())
