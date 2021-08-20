#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 4:21 下午
# @Author  : Catop
# @File    : dbconn.py
# @Software: PyCharm

from datetime import datetime
from datetime import timedelta
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


def get_alarm_params(dev_id):
    """获取报警参数"""
    cur = conn.cursor()
    sql = "SELECT alarm_params FROM dev_info WHERE dev_id=?"
    params = [dev_id]

    cur.execute(sql, params)
    sql_ret = cur.fetchone()
    if(len(sql[0]) == 0):
        return '[0,0,0,0]'

    return sql_ret[0]

def get_sensors(dev_id):
    """获取绑定指定设备的传感器信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM sensor_info WHERE bind_dev_id=?"
    params = [dev_id]
    cur.execute(sql, params)

    return cur.fetchall()


def get_min_before_record(dev_id, time_period):
    """获取n分钟前指定设备各个传感器的记录"""
    sensors_id = get_sensors(dev_id)
    ret = []
    for sen in sensors_id:
        cur = conn.cursor()
        upload_time = (datetime.now() - timedelta(minutes=time_period)).strftime('%Y-%m-%d %H:%M')
        sql = "SELECT sensor_distance FROM upload_log WHERE sensor_id=? AND datetime LIKE ? LIMIT 1"
        params = [sen[0], upload_time+"%"]
        cur.execute(sql, params)

        record = cur.fetchone()
        if(record):
            # 找到符合条件的记录
            ret.append((sen[1],get_water_level(sen[0],record[0])))
        else:
            # 没找到符合条件记录，返回在此之前最近的一条
            cur = conn.cursor()
            upload_time = (datetime.now() - timedelta(minutes=time_period)).strftime('%Y-%m-%d %H:%M')
            sql = "SELECT sensor_distance FROM upload_log WHERE sensor_id=? AND datetime < ? ORDER BY datetime LIMIT 1"
            params = [sen[0], upload_time + ":00"]
            cur.execute(sql, params)
            record = cur.fetchone()

            ret.append((sen[1], get_water_level(sen[0], record[0])))


    return ret


def get_water_level(sensor_id, distance):
    """获取指定传感器的真实值"""
    # 计算公式：真实值(level) = 偏差值(offset) - 距离值(distance)
    cur = conn.cursor()
    sql = "SELECT distance_offset FROM sensor_info WHERE sensor_id=? LIMIT 1"
    params = [sensor_id]

    cur.execute(sql, params)
    offset = cur.fetchone()[0]

    return offset - distance


def set_alarm_log(sensor_id, dev_id, type, water_level):
    """写入告警记录"""
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = conn.cursor()
    sql = "INSERT INTO alarm_log(sensor_id,dev_id,type,water_level,datetime) VALUES(?,?,?,?,?)"
    params = [sensor_id, dev_id, type, water_level, now_time]

    cur.execute(sql, params)
    conn.commit()


def get_alarm_log(dev_id):
    """获取指定设备最新报警记录"""
    cur = conn.cursor()
    sql = "SELECT * FROM alarm_log WHERE dev_id=? ORDER BY datetime DESC LIMIT 1"
    cur.execute(sql, [dev_id])

    sql_ret = cur.fetchone()
    return  sql_ret


def get_sensor_info(sensor_id):
    """获取传感器信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM sensor_info WHERE sensor_id=?"
    params = [sensor_id]
    cur.execute(sql, params)

    return cur.fetchone()

def get_dev_info(dev_id):
    """获取设备信息"""
    cur = conn.cursor()
    sql = "SELECT * FROM dev_info WHERE dev_id=?"
    params = [dev_id]
    cur.execute(sql, params)

    return cur.fetchone()

def check_exist(port):
    """检查对应端口设备是否存在"""
    cur = conn.cursor()
    sql = "SELECT dev_id FROM dev_info WHERE dev_port=?"
    params = [port]
    cur.execute(sql, params)

    sql_ret = cur.fetchall()
    if(len(sql_ret) > 0):
        return  True
    else:
        return  False


if __name__ == "__main__":
    #add_log('127.0.0.1','6002',1211,37.2)
    #print(get_query_info('2000'))
    #print(get_dev_id('2000'))
    # print(get_sensor_id(3, '01'))
    # print(get_alarm_params(3))
    # print(get_min_before_record(4,30))
    # set_alarm_log(5,4,1,800)
    # print(get_alarm_log(4))
    # print(get_water_level(5,754))
    # print(check_exist(2001))

    print(get_dev_info(3))