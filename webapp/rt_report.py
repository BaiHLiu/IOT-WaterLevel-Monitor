#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/20 3:58 下午
# @Author  : Catop
# @File    : rt_report.py
# @Software: 生成实时数据报表

import xlwt
from datetime import datetime


def generate_rt_report(rt_info):
    now_time = datetime.now().strftime("%Y-%m-%d")
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Sheet1')

    # 公共
    # 边框线
    borders = xlwt.Borders()

    borders.left = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.right = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.top = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.bottom = xlwt.Borders.THIN  # 添加边框-虚线边框

    # 标题
    font_title = xlwt.Font()
    font_title.name = 'name Times New Roman'
    font_title.height = 25 * 11
    font_title.bold = True
    style_title = xlwt.XFStyle()
    style_title.font = font_title

    worksheet.write_merge(0, 0, 0, 6, f'昌邑市潍河防潮蓄水闸服务所每日报表 {now_time}', style_title)

    # 表头
    font_text = xlwt.Font()
    font_text.name = 'name Times New Roman'
    font_text.height = 20 * 11
    style_text = xlwt.XFStyle()
    style_text.font = font_text
    style_text.borders = borders

    worksheet.write(1, 0, '站点名称', style_text)
    worksheet.write(1, 1, '采集位置', style_text)
    worksheet.write(1, 2, '水位(米)', style_text)
    worksheet.write(1, 3, '深度(米)', style_text)
    worksheet.write(1, 4, '上传时间', style_text)
    worksheet.write(1, 5, '超警', style_text)

    # 数据
    idx = 1
    for dev in rt_info:
        idx += 1
        for sensor in dev['data']:
            worksheet.write(idx, 0, dev['name'], style_text)
            worksheet.write(idx, 1, sensor['sensor_name'], style_text)
            worksheet.write(idx, 2, "%.2f"%(int(sensor['high_level'])/1000), style_text)
            worksheet.write(idx, 3, "%.2f"%(int(sensor['water_depth'])/1000), style_text)
            worksheet.write(idx, 4, dev['update_time'].split(' ')[1], style_text)
            if dev['if_alarm']:
                worksheet.write(idx, 5, "是", style_text)
            else:
                worksheet.write(idx, 5, '否', style_text)
            if(len(dev['data']) > 1):
                idx += 1

    # 保存
    file_name = f'../data/real-time-table/每日报表-{now_time}.xls'
    workbook.save(file_name)
    return file_name


if __name__ == "__main__":
    rt_info = [
        {'data': [{'high_level': 7120, 'sensor_id': 4, 'sensor_name': '闸前', 'temperature': 280, 'water_depth': 3620}],
         'id': 3, 'if_alarm': True, 'interval_time': 10, 'ip': '127.0.0.1', 'name': '城东',
         'update_time': '2021-08-20 16:05:07'},
        {'data': [{'high_level': -7196, 'sensor_id': 7, 'sensor_name': '闸前', 'temperature': 290, 'water_depth': -9996}],
         'id': 12, 'if_alarm': False, 'interval_time': 10, 'ip': '27.205.138.14', 'name': '城北',
         'update_time': '2021-08-19 19:41:34'}, {'data': [
            {'high_level': -1789, 'sensor_id': 9, 'sensor_name': '闸后', 'temperature': 280, 'water_depth': -789},
            {'high_level': -3083, 'sensor_id': 11, 'sensor_name': '闸前', 'temperature': 280, 'water_depth': -2083}],
                                                 'id': 13, 'if_alarm': False, 'interval_time': 10, 'ip': '60.233.1.79',
                                                 'name': '辛安庄', 'update_time': '2021-08-19 19:41:08'}]
    generate_rt_report(rt_info)
