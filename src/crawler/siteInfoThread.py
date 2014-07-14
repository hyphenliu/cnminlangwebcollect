# -*- coding:utf-8 -*-
'''
Created on 2014年1月2日

@author: Hyphen.Liu
'''
import threading,re,logging

import globalvar.guiGlobalVar as ggv
from utils.langDect import LangDect
from getSiteInfo import GetSiteInfo
from getHtml import GetHtmlText
from utils.sqlite3DB import DBstorage

class SiteInfoThread(threading.Thread):
    '''
    :添加多线程支持
    :功能：识别网页语言和获取网站详细信息
    '''
    def __init__(self,inqueue,outqueue,flag):
        threading.Thread.__init__(self)
        self.window = ggv.window
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        if flag == 'engine':self.m = '2/4'                  #第二步
        else: self.m = '4/4'                                #第四步
        self.window.gauge.SetValue(0)
        
    def stop(self):
        self.timeToQuit.set()

    def sitld(self,url):
        '''
        :识别判断给定的url的语言是否为给定的语言
        :param url: 给定的url
        '''
        if ggv.pterminate:return None
        self.mksure = False
        ld = LangDect()
        html = GetHtmlText()
        text,htmlitems = html.getHtmlText(url,reply=True)
        if ggv.lang_use == 'mn' and text:                            #蒙古文网站复杂需要特殊处理
            msignal = [u'蒙文',u'蒙古语',u'蒙古学会',u'蒙古文']
            if len(htmlitems['generator']) > 5:             #数字5没有特殊的意义
                self.mksure = True
            elif not self.mksure:
                for ms in msignal:
                    if htmlitems['title'].find(ms) >= 0:
                        self.mksure = True
                if re.search(r'蒙古族.*(中|大|小)学'.decode('utf8'),htmlitems['title'],re.I):
                    self.mksure = True
            elif not self.mksure:
                for mf in ggv.fontfamily['mn'].split(','):
                    if htmlitems['font-family'].find(mf) >= 0:
                        self.mksure = True
            if self.mksure:
                self.window.scanlogUpdate(u'语   言：%s\r\n可信度：1.000000000\r\n链   接：%s\r\n'%(ggv.lang_use,url))   #主界面同步显示扫描结果
                return [{ggv.lang_use:'1.0'},htmlitems['charset-web']]
        if text:
            ldRst = ld.langDect(ggv.lang_use, text)         #此处只需要返回的语言及其可信度，不需要接受编码方式
            if ldRst:
#                 print '语言：%s\t可信度：%s\t链接：%s\t'%(ldRst[0].keys()[0],ldRst[0].values()[0],url)
                logging.info('语言：%s\t可信度：%s\t链接：%s\t'%(ldRst[0].keys()[0],ldRst[0].values()[0],url))
                self.window.scanlogUpdate(u'语   言：%s\r\n可信度：%s\r\n链   接：%s\r\n'\
                                          %(ldRst[0].keys()[0],ldRst[0].values()[0],url))           #主界面同步显示扫描结果
                if ggv.lang_use in ldRst[0] and ldRst[0][ggv.lang_use] > ggv.systemSetList[3]*0.01: #用户设定的阈值乘以0.01
                    return ldRst
            return None
        return None

    def sitgsi(self,domain,separates):
        '''
        :对给定的已经预处理的url（域名，子域名，目录和子目录等）判断是否为给定的语言
        :param domain: 给定的域名
        :param separates: 子域名、目录和子目录组成的列表
        '''
        si = []
        gsi = GetSiteInfo()
        #对域名进行判断，判断域名、子目录是否为本语言
        for urlS in separates[:-1]:                         #最后一个为数字，第一个是域名
            if ggv.pterminate:return si                     #程序被强制终止
            if not urlS or urlS == ' ':continue             #判断是否为空，有的网址分段之后可能为空
            if not urlS.startswith('http'):urlS = 'http://' + urlS
            urlS = urlS.strip()
            rst = self.sitld(urlS)
            if ggv.pterminate:return si
            if rst:
                si = gsi.getSiteInfo(urlS)                  #获取网站属性信息
                if si:
                    si[0] = domain                          #防止从网上获取到的域名错误，故在此替换正确的域名
                    si.extend([str(rst[1]),str(rst[0][ggv.lang_use]),urlS])
                return si
        return si
        
    def run(self):
        while True:
            if self.timeToQuit.isSet():break
            if self.inqueue.empty():break
            line = self.inqueue.get()
            line = line.split('\t')
            si = self.sitgsi(line[0], line[1:])
            if ggv.pterminate:break
            gpercent = float('%.3f'%(1.0*(ggv.gaugesize-self.inqueue.qsize())/ggv.gaugesize))*100               #完成进度百分比
            self.window.gauge.SetValue(gpercent)
            self.window.SetStatusText(u'%s网页语言识别中..%.1f%%'%(self.m,gpercent),1)
            if si:
                dbs = DBstorage()           
                dbs.insert_data(ggv.lang_use, si)           #存入数据库
                self.window.rstlogUpadate(u'语   言：%s\r\n可信度：%s\r\n链   接：%s\r\n'%(ggv.lang_use,si[-2],si[-1]))   #成功识别语言，在主界面显示
                self.outqueue.put(si[-1])
                self.window.SetStatusText(u'收集网站数：%d'%self.outqueue.qsize(),2)
            self.inqueue.task_done()
