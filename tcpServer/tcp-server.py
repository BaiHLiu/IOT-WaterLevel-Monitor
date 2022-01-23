#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 3:50 下午
# @Author  : Catop
# @File    : tcp-server.py
# @Software: 用于连接串口服务器，并轮询获取数据，上报httpAPI
import json
import time
import threading
import socket
import requests

import sys



sys.path.append("..")
import httpAPI.utils as utils
from conf import Config
import redisCache.cache

HTTP_API_ENDPOINT = Config.tcp_server['http_api_endpoint']


def get_client_info(tcp_client_1, tcp_client_address):
    """创建tcp-server，轮询获取设备信息"""
    while True:
        arg_idx = 0
        # 获取客户机ip和端口
        client_ip = tcp_client_address[0]
        client_port = tcp_client_address[1]
        virtual_port_flag = 0


        # 请求http api，更新查询参数列表
        query_params = get_query_params(client_port)
        if len(query_params['sensors_list']) > 0:
            # 第1种上报类型：串口服务器带固定本地端口，用固定的端口接收指令
            pass
        else:
            # 第2种上报类型：串口服务器无固定本地端口，由它在建立连接时发送注册包，注册包内容为端口号的16进制
            # 注册包hex字符串格式举例：3e a0，两位十六进制数为虚拟串口号，需在塔石透传模块中设置"自定义注册包-连接到服务器时发送"
            virtual_port_flag = 1
            try:
                recv_data = tcp_client_1.recv(1024)
                if recv_data:
                    # 接收注册包
                    recv_data_str = bytes.hex(recv_data)
                    client_port = int(recv_data_str, 16)
                    print(f"[+]Virtual port connected:{client_port}")
                    query_params = get_query_params(client_port)
                    time.sleep(1)
            except:
                print("[!] Register message is broken")
                return
        # TODOd:增加redis缓存ip最后上报时间，update_time_192.168.1.18:"2021-10-05 19:00:00"
        redisCache.cache.set_upload_time(client_ip)


        INTERVAL_TIME = query_params['interval_time']
        for sensor_info in query_params['sensors_list']:
            # 循环各个传感器，拼接查询命令
            POLLING_ARGUMENTS = []
            for arg in query_params['args_list']:
                POLLING_ARGUMENTS.append(utils.crc16_modbus(sensor_info['hex_address'] + " " + arg))

            # 响应参数列表（hex字符串）
            resp_args = []

            for send_data_str in POLLING_ARGUMENTS:
                # 循环查询参数
                arg_idx += 1
                # 发送数据
                send_data = bytes.fromhex(send_data_str)
                tcp_client_1.send(send_data)
                print(f"[+] Sent to {str(tcp_client_address)} : {send_data_str}")
                # 接收数据
                time.sleep(1)  # 数据测量需要一段时间，避免出现0距离

                tcp_client_1.settimeout(5)
                try:
                    # 超时引发接收数据异常，断开连接销毁线程
                    recv_data = tcp_client_1.recv(1024)
                except:
                    tcp_client_1.close()
                    print("[!] Timed out, disconnected.")

                if recv_data:
                    recv_data_str = bytes.hex(recv_data)
                    resp_args.append(recv_data_str)
                    print(f"[+] {str(tcp_client_address)} Received message:" + recv_data_str)
                else:
                    print(f"[+] Client disconnected: {str(tcp_client_address)}")
                    tcp_client_1.close()
                    break
            # 上报http-api，目前这里参数只有距离和温度
            if (len(resp_args) == 2):
                params = {
                    "ip": client_ip,
                    "port": str(client_port),
                    "sensor_address": sensor_info['hex_address'],
                    "distance": int(resp_args[0][6:10], 16),
                    "temperature": int(resp_args[1][6:10], 16)
                }

                # 处理温度溢出问题
                if resp_args[1][6] == 'f':
                    params['temperature'] -= 65535

                requests.get(url=HTTP_API_ENDPOINT + "/upload", params=params)
                print("[+] Upload to HTTP-API successfully")
        # 轮询延时
        time.sleep(INTERVAL_TIME)
        if virtual_port_flag == 1:
            # 如果是虚拟端口设备，轮询一次后断开连接
            tcp_client_1.close()
            print(f"[+] Virtual port device disconnected, virtual port:{client_port}")


def get_query_params(dev_port):
    params = {"dev_port": dev_port}
    resp = requests.get(url=HTTP_API_ENDPOINT + "/get_query_params", params=params)

    return json.loads(resp.text)


if __name__ == '__main__':

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server.bind((Config.tcp_server['bind_address'], Config.tcp_server['bind_port']))
    tcp_server.listen(Config.tcp_server['max_connections'])
    while True:
        tcp_client_1, tcp_client_address = tcp_server.accept()
        print("[+] New client connected: " + str(tcp_client_address))
        thd = threading.Thread(target=get_client_info, args=(tcp_client_1, tcp_client_address))
        thd.start()
