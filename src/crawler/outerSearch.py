# -*- coding:utf-8 -*-
'''
Created on 2014年2月2日

@author: Hyphen.Liu
'''

import os,Queue,logging

import globalvar.guiGlobalVar as ggv
from utils.dealUrl import DealUrl
from getUrlThread import GetUrlThread

class OuterSearch():
    '''
    :对已经识别为某语言的网站进行遍历查找这些网站的友情链接是否为该语言文字
    '''
    ''''''
    def __init__(self,outfile,infile):
        '''
        :初始化参数
        :param outfile:待写入的文件名称
        :param inqueue:之前得到的结果
        '''
        self.outfile = outfile
        self.infile = infile
        self.outqueue = Queue.Queue()
        self.inqueue = Queue.Queue()
        self.window = ggv.window
        ggv.scanindex = 0
        ggv.rstindex = 0
        self.window.scanlog.SetValue(u'扫描信息：\r\n\r\n')
        self.window.rstlog.SetValue(u'搜索结果：\r\n\r\n')
        self.window.SetStatusText('',2)
        self.webknown = []
        self.outersearch()
        self.saveresult()
        
    def outersearch(self):
        '''
        :网站遍历准备工作
        '''
        if not os.path.isfile(self.infile):return None      #程序被强行终止不会生成infile文件，但会从中断代码后运行，在此检测是否为强制终止程序
        lines = open(self.infile,'r').readlines()
        for line in lines:
            if line:
                self.webknown.append(line)
                self.inqueue.put(line)
                self.window.scanlogUpdate(line)
#         self.window.gauge.SetValue(0)
#         self.window.gauge.Show()
        self.window.SetStatusText(u'3/4网站广度遍历中..请耐心等待',1)     #状态栏提示进行广度遍历
#         ggv.gaugesize = self.inqueue.qsize()                #设定进度条最大值
        GetUrlThread(self.inqueue,self.outqueue,'outlink')
        os.remove(self.infile)

    def saveresult(self):
        '''
        :对获取到的网站连接处理并将结果保存到文件
        '''
        if ggv.pterminate:return None
        self.window.gauge.Hide()
        self.window.SetStatusText(u'3/4暂存网站广度遍历结果！',1)
        du = DealUrl()
        ofile = open(self.outfile,'w+')
        urls = []
        while True:                                         #搜索引擎返回的结果，使之保存到列表中
            if self.outqueue.empty():break
            url = self.outqueue.get()
            if url not in self.webknown:                    #排除已经存在的网站
                logging.info('url:%s'%url)
                urls.append(url)
#             self.queue.task_done()
#         print 'urls:',urls
        urls = set(urls)
        if ggv.pterminate:return None
        urldict = du.dealUrl(urls)                          #分别返回链接的域名、子域名、子目录、二级目录、收集到的网页数量
        self.window.SetStatusText(u'共有%d个网站'%len(urls),2)
        for domain in urldict:
            urlitem = domain + '\t' + '\t'.join(urldict[domain][:-1]) + '\t' + str(urldict[domain][-1])
            ofile.write(urlitem + '\r\n')
        ofile.close()
        self.window.SetStatusText(u'3/4保存结果完毕！',1)