#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import sys
import json
import time
import datetime
import requests
from Clock_UI import Ui_clock
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget


class Clock(QWidget, Ui_clock):
    def __init__(self):
        super(Clock, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)    # 设置窗口显示在最上层

        self.timer = QTimer()       # 初始化一个定时器
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.OnShowTime)     # 将定时器超时信号与槽函数showTime()连接
        self.OnShowDate()       # 在窗口中显示日期
        self.show()

    def OnShowTime(self):
        time_now = time.strftime('%H:%M:%S')        # 获取当前时间
        self.hour.setText(time_now[:2])
        self.min.setText(time_now[3:5])
        self.sec.setText(time_now[6:8])

    def OnShowDate(self):
        week_day_dict = {1: '星期一', 2: '星期二', 3: '星期三', 4: '星期四', 5: '星期五', 6: '星期六', 0: '星期日'}
        today = datetime.date.today()       # 获取今天的日期
        week = week_day_dict[int(today.strftime('%w'))]
        year, month, day = today.year, today.month, today.day
        date = '{}-{}-{}'.format(year, month, day)
        lunar_date = self.LunarDate(date)
        date_text = '{}年{}月{}日，{}，{}'.format(year, month, day, week, lunar_date)
        self.date.setText(date_text)
        self.date.setFocus()

    @staticmethod
    def LunarDate(date):        # 调用聚合数据的农历api接口
        url = 'http://v.juhe.cn/calendar/day?date=' + date + \
              '&key=需要替换为自己的key'
        reps = requests.get(url=url)
        data = json.loads(reps.text)
        lunar_year = data['result']['data']['lunarYear']
        animals_year = data['result']['data']['animalsYear']
        lunar = data['result']['data']['lunar']
        lunar_date = '{}，{}年，{}'.format(lunar_year, animals_year, lunar)
        return lunar_date


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ex = Clock()
    sys.exit(app.exec_())
