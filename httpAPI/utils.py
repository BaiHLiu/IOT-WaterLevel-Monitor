#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 9:27 上午
# @Author  : Catop
# @File    : utils.py
# @Software: PyCharm

from binascii import unhexlify
from crcmod import mkCrcFun

# common func for crc16
def get_crc_value(s, crc16):
    data = s.replace(' ', '')
    crc_out = hex(crc16(unhexlify(data))).upper()
    str_list = list(crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = ''.join(str_list[2:])
    return crc_data[:2] + ' ' + crc_data[2:]


# CRC16/MODBUS
def crc16_modbus(s):
    crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    last_str = get_crc_value(s, crc16)

    ret = s+" "+last_str.split(' ')[1]+" "+last_str.split(' ')[0]
    return ret



if __name__ == "__main__":
    print(crc16_modbus("01 03 02 02 F2"))