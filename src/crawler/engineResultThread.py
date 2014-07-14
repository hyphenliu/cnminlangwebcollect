# -*- coding:utf-8 -*-
'''
Created on 2014年1月2日

@author: Hyphen.Liu
'''
import threading,Queue

import globalvar.guiGlobalVar as ggv
import globalvar.crawlerGlobalVar as cgv
from getEngineResult import GetEngineResult
from utils.dealUrl import DealUrl

class GetResultThread(threading.Thread):
    '''
    :获取搜索引擎返回结果的多线程函数
    '''
    def __init__(self,equeue,keyword,oqueue):
        '''
        :初始化参数
        :param equeue:本次搜索使用的搜索引擎个数组成的队列
        :param keyword:搜索用的单独关键字
        :param oqueue:返回的搜索结果超链接
        '''
        threading.Thread.__init__(self)
        self.equeue = equeue
        self.keyword = keyword
        self.oqueue = oqueue
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        
    def stop(self):
        self.timeToQuit.set()
        
    def run(self):
        while True:
            if self.timeToQuit.isSet():break
            if self.equeue.empty():break
            engineattr = self.equeue.get()
            gr = GetEngineResult(engineattr,self.keyword,self.oqueue)
            gr.getResult()
            self.equeue.task_done()

class EngineResultThread():
    '''
    :启动搜索引擎搜索程序
    :搜索关键字和搜索引擎选择来自主界面设定值但没有返回结果
    :最终结果保存在globalvar.utilGlobalVar.URLTEMP文件里，供程序后期调用。
    '''
    def __init__(self,tmpfile):
        '''
        :初始化参数
        :param tmpfile:需要保存的文件名
        '''
        self.keywords = ggv.keyword_use
        self.engines = ggv.engine_use
        self.TEMPFILE = tmpfile
        self.window = ggv.window
        self.inqueue = Queue.Queue()
        self.equeue = Queue.Queue()
        self.getEngineResult()
        self.saveResult()
        
    def getEngineResult(self):
        '''
        :获取搜索引擎返回结果
        '''
        if ggv.pterminate:return None
        self.window.SetStatusText(u'1/4预处理中，请耐心等待...',1)    #状态栏显示当前进入预处理阶段
        for eng in self.engines:
            self.equeue.put(eng)
        for keyword in self.keywords:
            if ggv.pterminate:break
#             print u'关键字：',keyword
            for i in range(len(self.engines)):              #根据选择搜索引擎个数分配线程个数
                if ggv.pterminate:break
                grt = GetResultThread(self.equeue,keyword,self.inqueue)
                cgv.threadlist.append(grt)
                grt.setDaemon(True)
                grt.start()
        self.equeue.join()                                  #等待搜索引擎队列为空
        
    def saveResult(self):
        '''
        :保存搜索返回结果的后处理结果
        :功能：处理返回的链接依次剥离域名、子域名、二级目录，将处理结果保存到文档
        '''
        if ggv.pterminate:return None
        self.window.SetStatusText(u'1/4暂存搜索引擎结果！',1)
        du = DealUrl()
        ofile = open(self.TEMPFILE,'w+')
        urls = []
        while True:                                         #搜索引擎返回的结果，使之保存到列表中
            if self.inqueue.empty():break
            urls.append(self.inqueue.get())
#             self.queue.task_done()
        urls = set(urls)
        urldict = du.dealUrl(urls)                          #分别返回链接的域名、子域名、子目录、二级目录、收集到的网页数量
        self.window.SetStatusText(u'共有%d个网站'%len(urls),2)
        for domain in urldict:
            urlitem = domain + '\t' + '\t'.join(urldict[domain][:-1]) + '\t' + str(urldict[domain][-1])
            ofile.write(urlitem + '\r\n')
        ofile.close()
        self.window.SetStatusText(u'1/4保存结果完毕！',1)
        