# -*- coding:utf-8 -*-
'''
Created on 2013年12月18日

@author: Hyphen.Liu
'''
import logging
import threading
import os

import globalvar.guiGlobalVar as ggv
from crawler.engineResultThread import EngineResultThread
from crawler.siteInfoMain import SiteInfoMain
from crawler.outerSearch import OuterSearch

class StartRun(threading.Thread):
    '''
    :程序主窗口点击开始运行时程序开始运行调度函数
    '''
    def __init__(self,window):
        '''
        :初始化参数
        :param window:程序主窗口
        '''
        threading.Thread.__init__(self)
        logging.info('start running...')
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
    
    def mainCollection(self):
        '''
        :网站收集程序主入口
        '''
        if not os.path.isfile(ggv.OUTTEMPF):
            if not os.path.isfile(ggv.ENGTEMPF):
                if not os.path.isfile(ggv.URLTEMPF):        #检查TEMPF文件是否存在，否则生存TEMPF文件
                    if ggv.pterminate:return None
                    EngineResultThread(ggv.URLTEMPF)
                if ggv.pterminate:return None
                SiteInfoMain('engine',ggv.URLTEMPF,ggv.ENGTEMPF)                #检测url的语言并获取相关网站的信息
            if ggv.pterminate:return None
            OuterSearch(ggv.OUTTEMPF,ggv.ENGTEMPF)
        if ggv.pterminate:return None
        SiteInfoMain('wide',ggv.OUTTEMPF)                   #检测url的语言并获取相关网站的信息
        if not ggv.pterminate:                              #程序运行完成，且非被手动终止。
            self.window.gauge.Hide()
            self.window.gauge.SetValue(0)
            self.window.OnStop()
    
    def stop(self):
        self.timeToQuit.set()
        
    def run(self):
        while True:
            if self.timeToQuit.isSet():
                break
            self.mainCollection()
    