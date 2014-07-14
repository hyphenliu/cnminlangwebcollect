# -*- coding:utf-8 -*-
'''
Created on 2013年11月14日

@author: Hyphen.Liu
'''
import types
import requests
import logging

from getHtml import GetHtmlText,GetHtmlSource
from utils.dealUrl import RemoveUrl
import globalvar.guiGlobalVar as ggv

class GetEngineResult():
    '''
    :选择搜索引擎，现有：谷歌、百度、360、雅虎和必应搜索引擎。
    :各搜索引擎搜索结果的返回界面源码特征信息为：搜索引擎名、
    :搜索引擎的链接、输入的关键字、返回结果超链接表示标识、
    :页面导航链接标识、下一页标识、选择的语言。默认语言为en。
    '''
    def __init__(self,engattr,keyWord,queue):
        '''
        :初始化相应搜索引擎的源码标识信息
        :param engattr:搜索引擎返回页面结果含有的超链接html标志，所在div，下一页等
        :param keyWord:搜索的关键字
        :param queue:
        '''
        self.engine = engattr[0]
        self.baseUrl = engattr[1]
        self.baseUrlEnd = engattr[2]                        #链接添加信息，为了不使用ncr功能
        self.keyWord = keyWord
        self.urlId = engattr[4]
        self.navId = engattr[5]
        self.nextId = engattr[6]
        self.lang = engattr[7]
        self.queue = queue                                  #结果收集队列
        self.window = ggv.window
        self.getResult()
        
    def getSinglePageResult(self,url):
        '''
        :获取单个页面的搜索结果链接，百度的链接需要单独处理，因为其返回结果加密重定向了。
        :本函数返回所有搜索结果的链接，以及判断是否有下一页的链接。
        :param url: 给定的url链接
        '''
        ru = RemoveUrl()
        gh = GetHtmlText()
        signal = 1
        flag = 0
        retry = 10                                          #程序可能不能一次完全加载反馈所有内容，故需要等待重新加载
        while signal:   
            if ggv.pterminate:break
            soup = gh.getHtml(url)
            if type(soup) == types.NoneType:
                retry -= 1
                if retry == 0:break
                continue
            navcnt = soup.find(self.navId[0],{self.navId[1]:self.navId[2]})
            if(type(navcnt) == types.NoneType):
                #print 'Not find the engine result resource div, span, h3 : NoneType retry:',retry
                logging.error('Not find the engine result resource div, span, h3 : NoneType retry: %d'%retry)
                retry -= 1
                if retry == 0:
                    flag = 0
                    break
                continue
            signal = 0                                      #已经获取到网页的内容，直接跳出while循环
            navends = navcnt.findAll('a')                   #找到所有超链接的html标志
            if not navends:break                            #返回为空停止运行
            navend = navends[-1]
            if navend.text.find(self.nextId) >= 0:flag = 1
            else:flag = 0
            h3s = soup.findAll('h3')                        #定位返回结果链接所属范围
            for h3 in h3s:
                if(type(h3) == types.NoneType):continue
                link = h3.find('a')                         #定位结果链接位置
                if(type(link) == types.NoneType):continue
                link = link['href']                         #提取链接
                if(self.engine == 'baidu'):                 #百度返回结果需要特殊处理
                    try:link = requests.get(link.strip())
                    except:continue
                    link = link.url
                if ru.removeUrl(link):                      #去除常见的非少数网站url
#                     print link
                    logging.info('Get Link: %s'%link)
                    self.window.scanlogUpdate(link)         #主界面同步显示
                    self.queue.put(link)
                    self.window.SetStatusText(u'获取到：%d个结果'%self.queue.qsize(),2) #在状态栏第二栏显示当前获取到的结果数量
        return flag
    
    def getNextPageUrls(self,url):
        '''
        :根据getSinglePageResult返回结果获取下一页的链接，
        :并返回本次所搜关键字的所有搜索结果链接。
        :param url: 给定的url
        '''
        if ggv.pterminate:return None
        urlf = url
        flag = 1
        urlSuf = ''
        ghs = GetHtmlSource()
        if self.engine == 'so' or self.engine == 'yahoo':page = 1
        else:page = 0
        while flag and not ggv.pterminate:                  #程序发出终止信号
            page += 1
            if page >= ggv.systemSetList[-1]:break          #每次获取的页面数由用户设定
            flag = self.getSinglePageResult(urlf)
            if flag ==0: break
            if self.engine == 'google' or self.engine == 'baidu':
                urlSuf = str(page*10)
            elif self.engine == 'so' or self.engine == 'yahoo':
                urlSuf = str(page)
            else:
                urlSuf = str(page) + '1'
            urlf = url + self.urlId + urlSuf
            ghs.randomSleep(3,10)                           # 睡眠3-10秒钟
   
    def getResult(self):
        '''
        :获取搜索引擎结果程序主函数
        '''
        url = self.baseUrl + self.keyWord + self.baseUrlEnd
        self.getNextPageUrls(url)
