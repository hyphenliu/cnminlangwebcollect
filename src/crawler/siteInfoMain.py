# -*- coding:utf-8 -*-
'''
Created on 2014年2月2日

@author: Hyphen.Liu
'''

import Queue
import os

import globalvar.guiGlobalVar as ggv
import globalvar.crawlerGlobalVar as cgv
from crawler.siteInfoThread import SiteInfoThread

class SiteInfoMain():
    '''
    :对所有的网页连接识别该网页的语言
    :对已经识别为相应语言的网站获取该网站建站详细信息
    '''
    def __init__(self,flag,infile,outfile=None):
        '''
        :初始化参数
        :param flag:区别是进行搜索引擎结果的网站信息获取还是广度遍历的网站信息获取。标志取值：engine,wide
        :param infile:需要从文本中读入待识别网页的超链接
        :param outfile:结果写入的文档
        '''
        self.flag = flag
        self.infile = infile
        self.outfile = outfile
        self.window = ggv.window
        self.threadnum = ggv.systemSetList[1]
        self.inqueue = Queue.Queue()
        self.outqueue = Queue.Queue()                       #保存收集到的网站结果，供网站广度扫描使用，在收集网站广度扫描得到的网站时只做计数器
        if self.flag == 'engine':m = '2/4'                  #第二步
        else: m = '4/4'                                     #第四步
        self.window.SetStatusText(u'%s网页语言识别中..0.0%%'%m,1)   #设置状态栏显示
        self.window.SetStatusText(u'收集网站数：0',2)
        self.window.gauge.Show()                            #设置进度条为显示状态
        self.siteinfos()
        if self.outfile:self.saveresults()                  #程序第二阶段需要保存结果
        
    def siteinfos(self):
        '''
        :检测网页语言并获取识别出的语言的网页所属网站的详细信息
        :param infile: 给定预处理后的url文档，该文档含有很多域名的url及其分段剥离后的url段
        '''
        if not os.path.isfile(self.infile):return None      #获取搜索引擎程序被强行终止不会生成infile文件，在此检测是否为强制终止程序
        ggv.scanindex = 0                                   #重置序号
        lines = open(self.infile,'r').readlines()           #读取保存好的txt文件内容
        for line in lines:
            if line:
                self.inqueue.put(line)                      #带检测url队列生成
        ggv.gaugesize = self.inqueue.qsize()                #进度条的分母值
        for i in range(self.threadnum):
            if ggv.pterminate:break                         #程序被强制终止
            gsit = SiteInfoThread(self.inqueue,self.outqueue,self.flag)             #语言识别和网站信息获取主要类
            cgv.threadlist.append(gsit)
#             gsit.setDaemon(True)
            gsit.start()                                    #启动线程
        self.inqueue.join()                                 #等待输入队列为空再执行其他操作
        if os.path.isfile(self.infile):os.remove(self.infile)
        self.window.gauge.Hide()
        
    def saveresults(self):
        '''
        :保存结果到文件
        '''
        if ggv.pterminate:return None
        ofile = open(self.outfile,'w+')
        while True:
            if self.outqueue.empty():break
            lk = self.outqueue.get()
            if lk:
                ofile.write(lk+'\r\n')
        ofile.close()