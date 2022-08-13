# from easygui import diropenbox,integerbox,boolbox # 简单对话框
# from random import randint # 随机数
# from os import listdir, system # 读取文件名
# from os.path import join,split # 合并路径
from PIL.Image import open as openImage # 读取图片
# from pystray import MenuItem,Icon,Menu # 托盘图标
# from ctypes import windll # 设置壁纸的api
# from apscheduler.schedulers.background import BackgroundScheduler # 定时任务
# from datetime import datetime # 提供now()函数以即时触发任务
# from configparser import ConfigParser # 读取参数
from pystray import MenuItem,Icon # 菜单和托盘图标
from easygui import boolbox
import json #解析json文件
from sys import path as syspath
from os.path import join

class PCAsistant:
    def __init__(self):
        self.icon = Icon('',openImage('./icon.ico'),'PC Asistant')
        self.addons = []
        self.loadAddons()
        self.setInitMenu()
        self.updateMenu()
        print('初始化完毕。')

    def loadAddons(self):
        with open('addons.json','r',encoding='utf-8') as file:
            addonsInAFolder = json.load(file)
        for addons in addonsInAFolder:
            parentFolder = addons['parent folder']
            modules = addons['modules']
            if not parentFolder or not modules:
                continue
            for addon in modules:
                folder = addon['folder']
                module = addon['module']
                enabled = addon['enabled']
                if not(folder and module and enabled):
                    continue
                syspath.append(join(parentFolder,folder)) # 每个子文件夹都添加，是为了避免路径出现空格
                exec('global mainClass; from %s import mainClass' % module)
                addon = mainClass()
                if addon:
                    if addon.needParent:
                        addon.PCAsistant = self
                    self.addons.append(addon)

    def setInitMenu(self):
        self.exitMenu = MenuItem('退出',self.stop)
        # self.restartMenu = MenuItem('重新启动',self.restart)
        # self.manageMenu = MenuItem('管理',Menu(self.restartMenu))

    def updateMenu(self):
        self.menu = [addon.menu for addon in self.addons]
        # self.menu.append(self.manageMenu)
        self.menu.append(self.exitMenu)
        self.icon.menu = self.menu

    def run(self):
        for addon in self.addons:
            addon.run()
        self.icon.run()

    def stop(self):
        msg = '确定退出吗？'
        if boolbox(msg,choices=('是','否'),default_choice='否',cancel_choice='否'):
            for addon in self.addons:
                addon.stop()
            self.icon.stop()
            print('已退出。')
            return True
        return False

if __name__ == '__main__':
    pcAsistant = PCAsistant()
    pcAsistant.run()
