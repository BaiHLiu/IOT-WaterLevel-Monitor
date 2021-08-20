'''
Description: 
Author: Catop
Date: 2021-08-11 14:40:13
LastEditTime: 2021-08-11 15:46:03
'''
import sys
import time
import socket


def init_connect(host, port, local_port):
    tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 将socket绑定到固定的端口，标识不同设备
        tcp_client_1.bind(('', int(local_port)))
        tcp_client_1.connect((host, port))
    except ConnectionRefusedError:
        print("[!] Can't connect to server, retry in 3s")
        time.sleep(3)
        init_connect(host, port, local_port)
    else:
        print("[+] Connected to server successfully.")
        return tcp_client_1


def work_msg(tcp_client):
    while True:
        if (tcp_client):
            recv_data = tcp_client.recv(1024)
            if (recv_data):
                recv_data_str = bytes.hex(recv_data)
                print("[+]Received command:" + recv_data_str)
                if recv_data_str == "01030100000185f6":
                    # 查询距离_01
                    send_data_str = "01 03 02 0B B8 38 A1"
                elif recv_data_str == "0103010200012436":
                    # 查询温度_01
                    send_data_str = "01 03 02 01 2C B8 09"
                elif recv_data_str == "02030100000185c5":
                    # 查询距离_02
                    send_data_str = "02 03 02 0B 3C FB 65"
                elif recv_data_str == "0203010200012405":
                    # 查询温度_02
                    send_data_str = "02 03 02 01 18 FD DE"
                elif recv_data_str == "0303010000018414":
                    # 查询距离_03
                    send_data_str = "03 03 02 0B 4C C7 41"
                elif recv_data_str == "03030102000125d4":
                    # 查询温度_03
                    send_data_str = "03 03 02 01 20 C1 CC"
                elif recv_data_str == "FF0302000001906c":
                    # 查询设备地址
                    send_data_str = "FF 03 02 00 01 50 50"

                time.sleep(1)
                send_data = bytes.fromhex(send_data_str)
                tcp_client.send(send_data)
                print("[+]Sent command:" + send_data_str)


# tcp_client_1.close()

if __name__ == "__main__":
    local_port = 11000
    tcp_client = init_connect('127.0.0.1', 10123, local_port)
    work_msg(tcp_client)
