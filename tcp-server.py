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
import httpAPI.utils as utils

###########################################
# HTTP-API设置
HTTP_API_ENDPOINT = "http://127.0.0.1:5001"
###########################################


def get_client_info(tcp_client_1, tcp_client_address):
    """创建tcp-server，轮询获取设备信息"""
    while True:
        arg_idx = 0
        #获取客户机ip和端口
        client_ip = tcp_client_address[0]
        client_port = tcp_client_address[1]

        #请求http api，更新查询参数列表
        query_params = get_query_params(client_port)
        INTERVAL_TIME = query_params['interval_time']

        for sensor_info in query_params['sensors_list']:
            #循环各个传感器，拼接查询命令
            POLLING_ARGUMENTS = []
            for arg in query_params['args_list']:
                POLLING_ARGUMENTS.append(utils.crc16_modbus(sensor_info['hex_address'] + " " + arg))


            # 响应参数列表（hex字符串）
            resp_args = []

            for send_data_str in POLLING_ARGUMENTS:
                # 循环查询参数
                arg_idx += 1
                #发送数据
                send_data = bytes.fromhex(send_data_str)
                tcp_client_1.send(send_data)
                print(f"[+] Sent to {str(tcp_client_address)} : {send_data_str}")
                #接收数据
                time.sleep(1)     #数据测量需要一段时间，避免出现0距离
                recv_data = tcp_client_1.recv(4096)
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
                    "sensor_address":sensor_info['hex_address'],
                    "distance": int(resp_args[0][6:10], 16),
                    "temperature": int(resp_args[1][6:10], 16)
                }
                requests.get(url=HTTP_API_ENDPOINT + "/upload", params=params)
                print("[+] Upload to HTTP-API successfully")

        # 轮询延时
        time.sleep(INTERVAL_TIME)



def get_query_params(dev_port):
    params = {"dev_port" : dev_port}
    resp = requests.get(url=HTTP_API_ENDPOINT + "/get_query_params", params=params)

    return json.loads(resp.text)



if __name__ == '__main__':

    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    tcp_server.bind(("", 10123))
    tcp_server.listen(128)
    while True:
        tcp_client_1 , tcp_client_address = tcp_server.accept()
        print("[+] New client connected: "+str(tcp_client_address))
        thd = threading.Thread(target = get_client_info, args = (tcp_client_1,tcp_client_address))
        thd.start()
