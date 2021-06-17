# -*- encoding: utf-8 -*-
'''
@DESCRIPTION : program entrance
@AUTHOR      : jylsec
@TIME        : 2021/06/17
'''


import sys
import os
import config

from gui.gui import GUI
from PyQt5.QtWidgets import QApplication

# 定义工作目录
config.WORK_DIR = os.getcwd()
# 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
app = QApplication(sys.argv)
ui = GUI()
ui.show()
#系统exit()方法确保应用程序干净的退出
#的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
sys.exit(app.exec_())