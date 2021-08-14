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
    tcp_client_1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        #将socket绑定到固定的端口，标识不同设备
        tcp_client_1.bind(('', int(local_port)))
        tcp_client_1.connect((host,port))
    except ConnectionRefusedError:
        print("[!] Can't connect to server, retry in 3s")
        time.sleep(3)
        init_connect(host, port, local_port)
    else:
        print("[+] Connected to server successfully.")
        return tcp_client_1


def work_msg(tcp_client):
    while True:
        if(tcp_client):
            recv_data = tcp_client.recv(1024)
            if(recv_data):
                recv_data_str = bytes.hex(recv_data)
                print("[+]Received command:"+recv_data_str)
                if recv_data_str=="01030100000185f6":
                    # 查询距离_01
                    send_data_str = "01 03 02 02 F2 38 A1"
                elif recv_data_str == "0103010200012436":
                    # 查询温度_01
                    send_data_str = "01 03 02 01 2C B8 09"
                elif recv_data_str == "02030100000185C5":
                    # 查询距离_02
                    send_data_str = "01 03 02 0B 3C BF 65"
                elif recv_data_str == "0203010200012405":
                    # 查询温度_02
                    send_data_str = "01 03 02 01 18 B9 DE"

                time.sleep(1)
                send_data = bytes.fromhex(send_data_str)
                tcp_client.send(send_data)
                print("[+]Sent command:"+send_data_str)

#tcp_client_1.close()

if __name__ == "__main__":
    local_port = 2003
    tcp_client = init_connect('127.0.0.1',10123,local_port)
    work_msg(tcp_client)

        