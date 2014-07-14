# -*- coding:utf-8 -*-
'''
Created on 2014年1月3日

@author: Hyphen
'''
import threading

from getUrls import GetUrls
import globalvar.guiGlobalVar as ggv
import globalvar.crawlerGlobalVar as cgv

class GetThread(threading.Thread):
    '''
    :获取页面广度遍历连接线程函数
    '''
    def __init__(self,inqueue,outqueue,flag):
        '''
        :初始化参数
        :param inqueue:待广度遍历的网页链接队列
        :param outqueue:保存获取到的链接到队列
        :param flag:对应sublink,outlink,inlink即包含子域名的链接、不包含本域名的链接和包含本链接以“/”分割前部分的链接
        '''
        threading.Thread.__init__(self)
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.flag = flag
        self.window = ggv.window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
    
    def stop(self):
        self.timeToQuit.set()
        
    def run(self):
        while True:
            if self.timeToQuit.isSet():break
            if ggv.pterminate:break
            if self.inqueue.empty():break
            url = self.inqueue.get()
            GetUrls(url,self.outqueue,self.flag)
            if ggv.pterminate:break
            gpercent = float('%.3f'%(1.0*(ggv.gaugesize-self.inqueue.qsize())/ggv.gaugesize))*100   #完成进度百分比
            self.window.gauge.SetValue(gpercent)
            if self.flag == 'outlink':
                self.window.SetStatusText(u'3/4网站广度遍历中..%.1f%%'%gpercent,1)
            else:self.window.SetStatusText(u'3/4网站遍历中...%.1f%%'%gpercent,1)
            self.window.SetStatusText(u'3/4网站遍历中...',1)
            self.inqueue.task_done()
        
class GetUrlThread():
    '''
    :获取网页广度遍历链接
    '''
    def __init__(self,inqueue,outqueue,flag):
        '''
        :初始化参数
        :param inqueue:是要进行遍历的网址队列
        :param outqueue:输出队列
        :param flag:flag是遍历的条件，只接受三个参数：inlink，sublink，outlink
        '''
        self.thread_num = ggv.systemSetList[1]
        self.flag = flag
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.getUrlsThread()
        
    def getUrlsThread(self):
        '''
        :获取页面链接线程
        :param thread_num:线程的数量
        '''
        for i in range(self.thread_num):
            if ggv.pterminate:break
            gut = GetThread(self.inqueue,self.outqueue,self.flag)
#             gut.setDaemon(True)
            cgv.threadlist.append(gut)
            gut.start()
        self.inqueue.join()
