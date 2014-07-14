# -*- coding:utf-8 -*-
'''
Created on 2013年11月7日

@author: Hyphen.Liu

本程序不处理所给链接是否有效，本程序目前只接受已经识别了网页语言的url链接。
'''
import base64
import socket
import time
import types
import logging

from getHtml import GetIpAddress, GetHtmlText
from utils.dealUrl import GetDomain
import globalvar.crawlerGlobalVar as cgv
import globalvar.guiGlobalVar as ggv

coding = 'utf8'

class GetItems():
    '''
    :具体读取网页相关信息的函数
    '''
    def getItems(self,text,infoItems,noInfos):
        '''
        :如果网页有相应的信息元则提取相应的信息元否则不提取
        :起初为其它网页设计但目前只为360服务
        :param text:传入的文本文档
        :param infoItems:传入的需要提取的信息元列表
        :param noInfos:文本文档没有信息元的标志
        '''
        if ggv.pterminate:return None
        list = []
        noInfos = noInfos.decode(coding)
        if not text:
            return False
        for i in range(len(infoItems)):
            infoItems[i] = infoItems[i].decode(coding)
        if text.find(noInfos) > 0 or text.find(u'工业和信息化部') < 10:
            list += ['-']*(len(infoItems)-1)
            return list
        for item in infoItems:
            #item = item.decode('utf8')
            nextIndex = infoItems.index(item) + 1
            if nextIndex > len(infoItems) - 1:
                break
            index1 = text.index(item) + len(item)
            index2 = index1 + text[index1:].index(infoItems[nextIndex])
            if index1 == index2:
                list.append('-')
            else:
                list.append(text[index1:index2].strip())
            text = text[index2:]
        return list

class Get360Beian():
    def getBeian(self,url):
        '''
        :从360服务器读取所要网站的建站的详细信息
        :如，网站名称、网站主页、网站所有者、网站所有单位、所有单位性质、备案信息、检验时间等信息。
        :param url:需要获取相关信息的网站链接
        '''
        if ggv.pterminate:return None
        gd = GetDomain()
        domain = gd.getDomain(url)                          #提取链接中的域名，因为360根据域名获取网站建站信息
        gi = GetItems()
        base64Code = base64.b64encode(domain)               #编码为base64，因为360获取网站建站信息的超链接域名是base64编码的
        beianUrl = cgv.url360 + base64Code
        htmlText = GetHtmlText()                            #获取网页文本
        text = htmlText.getHtmlText(beianUrl)
        return gi.getItems(text, cgv.beiAnInfoItem, cgv.beiAnNoInfo)
        
class GetAlexa():
    '''
    :从alexa.com上获取网站的全球排名、中文排名
    '''
    def getAlexa(self,url):
        '''
        :从Alexa网站上获取全球排名中文排名信息
        :param url:待获取排名信息的超链接
        '''
        if ggv.pterminate:return None
        ranks = []
        numR = 0
        gd = GetDomain()
        domain = gd.getDomain(url)                          #提取超链接的域名
        url = cgv.alexaUrl + domain
        time.sleep(10)                                      #休眠10秒
        htmlText = GetHtmlText()
        soup = htmlText.getHtml(url)                        #获取网页源码，不能直接根据网页文本进行判断，因为有的信息不存在
        if soup:
            rankrow = soup.findAll('div',{'class':'rank-row'})
            for rk in rankrow:
                rkl = rk.find('div')
                if type(rkl) == types.NoneType:
                    continue
                numR += 1
                rank = rkl.find('a').text                   #如果有排名，排名处会出现超链接
                ranks.append(rank)
            if numR < 2:
                ranks.append('-')
        else:                                               #没有相关标志则表示不存在
            ranks.append('-')
            ranks.append('-')
        return ranks
    
class GetIpAndAddress():
    '''
    :获取网站域名的ip地址和所在服务器地址
    :根据获取到的ip地址得到该ip地址所在的位置信息。
    :如，所在区域、国家、城市、服务提供商名称
    '''
    def getIpAndAddress(self,url):
        '''
        :获取相应url的ip地址
        :param url:待获取ip地址的超链接
        '''
        if ggv.pterminate:return None
        list = []
        gd = GetDomain()
        domain = gd.getDomain(url)
        try:
            ip = socket.gethostbyname(domain) 
        except Exception,e:
            if ggv.pterminate:return None
#             print 'Get Ip address error: %s, url:%s'%(e,url)
            logging.error('Get Ip address error: %s,url:%s '%(e,url))
            try:
                ip = socket.gethostbyname('www.'+domain)
            except Exception,e:
                if ggv.pterminate:return None
#                 print 'Get Ip address error2:%s,url:%s '%(url,e)
                logging.error('Get Ip address error2: %s,url:%s '%(url,e))
                list.extend(['-','-'])
                return list
        list.append(ip)
        gia = GetIpAddress()
        address = gia.getIpAddress(ip)
        list.append(address)
        return list

class GetSiteInfo():
    '''
    :获取某个网站的具体信息。
    :如：域名、网站名称、备案号、网站所有者、网站所有单位、
    :所有单位的性质、服务器地址、服务器所在位置、网站全球排名、
    :中文排名、日均访问量、日均pv量、检验时间等信息。
    '''
    def getSiteInfo(self,url):
        if ggv.pterminate:return None
        info = []                                           #保存网站所有建站信息的列表
        url = url.strip()
        g3b = Get360Beian()
        if g3b.getBeian(url):
            info.extend(g3b.getBeian(url))
        giaa = GetIpAndAddress()
        if giaa.getIpAndAddress(url):
            info.extend(giaa.getIpAndAddress(url))
        ga = GetAlexa()
        gainfo = ga.getAlexa(url)
        if gainfo:
            info.extend(gainfo)
        if len(info) > 10:                                  #数字10没有具体的意义，可以修改，但不要超过返回item的总个数
            return info
        return None
