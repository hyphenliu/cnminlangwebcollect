# -*- coding:utf-8 -*-
'''
Created on 2013年12月31日

@author: Hyphen
'''
import re
import logging

from getHtml import GetHtmlText
from utils.dealUrl import GetDomain, PreProcess

class GetUrls():
    '''
    :获取内部链接或外部链接或含有给定url的链接
    :flag参数：inlink，outlink，sublink
    '''
    def __init__(self,url,outqueue,flag):
        self.url = url
        self.outqueue = outqueue
        self.flag = flag
        self.flags = ['inlink','sublink','outlink']
        self.links = []
        self.extractUrls()
    
    def getUrls(self):
        '''
        :获取给定页面的所有超链接
        '''
        gh = GetHtmlText()
        pp = PreProcess()
        soup = gh.getHtml(self.url)
        if not soup:
            return None
        links = soup.findAll('a', href = True)              #超链接html标志
        urls = []
        if self.url.strip().endswith('/'):                  #拼接链接时防止出现两个斜杆相邻
            self.url=self.url.strip()[:-1]
        for link in links:
            link = link.get('href')
            pattern0 = re.compile(r'^\./')                  #本网站的链接不带http等协议开头的，直接以'./'开头
            pattern1 = re.compile(r'^(/\w+)')               #以'/'开头不带协议的本站链接
            pattern2 = re.compile(r'^(htt\w+)')             #带http协议的链接
            if pattern0.match(link):                        #此类链接需要拼接，拼接时去除'.'符号
                link = self.url + link[1:]
                link = pp.preProcess(link)
                if link:
                    urls.append(link)
            elif pattern1.match(link):                      #此类链接直接拼接即可
                link = self.url + link
                link = pp.preProcess(link)
                if link:
                    urls.append(link)
            elif pattern2.match(link):                      #此类链接需要特殊处理，链接没有问题之后就直接添加
                link = pp.preProcess(link)
                if link:
                    urls.append(link)
        return set(urls)
    
    def getInnerUrls(self):
        '''
        :获取本页面所有含有本域名的链接
        '''
        for l in self.links:
            if self.dm in l:
                self.outqueue.put(l)
    
    def getSubInnerUrls(self):
        '''
        :获取本页面含有本url前缀的链接
        '''
        for l in self.links:
            if not l in self.url and self.url in l:
                self.outqueue.put(l)
    
    def getOuterUrls(self):
        '''
        :获取本页面所有非本域名的链接
        '''
        for l in self.links:
            if not self.dm in l:
                self.outqueue.put(l)
    
    def extractUrls(self):
        '''
        :提取网页所有超链接
        '''
        gd = GetDomain()
        self.dm = gd.getDomain(self.url)
        if not self.dm:                                     #传入的链接本身就存在问题
#             print 'Illegal url'
            logging.warn('Illegal url: %s'%self.url)
            return
        if self.flag not in self.flags:                     #参数不合法
#             print 'Illegal parameter'
            logging.warn('Illegal parameter: %s'%self.choiceId)
            return
        else:
            self.links = self.getUrls()                     #获取超链接
            if self.links:
                if self.flag == 'inlink':self.getInnerUrls()
                elif self.flag == 'outlink':self.getOuterUrls()
                else:self.getSubInnerUrls()
