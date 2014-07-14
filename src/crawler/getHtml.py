# -*- coding:utf-8 -*-
'''
Created on 2013年11月14日

@author: Hyphen.Liu
'''
import urllib2,time,random,re,types,logging
import json,chardet

from bs4 import BeautifulSoup
import mechanize
import globalvar.crawlerGlobalVar as cgv
import globalvar.guiGlobalVar as ggv

class GetHtmlSource():
    '''
    :获取传入url的网页源码信息，保存获取到的网页的响应代码到crawlercgv的satatusCode.
    :若出现错误则保存错误到crawlercgv的errorStr中
    '''
    def randomSleep(self,int1=5,int2=20):
        '''
        :随机睡眠时间
        :param int1:范围起始值
        :param int2:范围终止值
        '''
        sleeptime = random.randint(int1, int2)
        time.sleep(sleeptime)
        
    def getElement(self,html):
        '''
        :提取网页源码中的元素
        :如，title，font-family，charset，meta name="generator"等
        :作为网页语言文字识别的辅助条件
        :param html:网页源码
        '''
        citers = re.finditer(r'charset\s*=\s*[\'\"]*((\w+[\-_]*)+\w+)[\'\",;>}]',html,re.I)
        if citers:
            for i in citers:                                #去除重复的charset值
                mcharset = i.group().lower()
                if not mcharset in self.htmlitems['charset-web'].split('\t'):
                    self.htmlitems['charset-web'] += mcharset+'\t'
        tmatch = re.search(r'<title>(.*)</title>',html,re.I)
        if tmatch:                                          #title内容需要正确解码，故首先读取网页编码
            mcode = 'utf8'
            if len(self.htmlitems['charset-web']) > 2:
                codematch = re.search(r'\s*[\'\"]*((\w+[\-_]*)+\w*)[\'\",;>}]',self.htmlitems['charset-web'].split('\t')[0])
                mcode = codematch.group(1).strip().lower()
            self.htmlitems['title'] = tmatch.group(1).decode(mcode,'ignore').strip()
        mpt = r'<\s*meta\s*name\W{0,5}generator\W{0,2}\s*?content=\W{0,2}\w*\s*?(portal-http://www.menksoft.com)\W{0,2}>'
        mmatch = re.search(mpt,html,re.I)
        if mmatch:
            self.htmlitems['generator'] = mmatch.group(1).strip()
        fiters = re.finditer(r'[\s{<;]font-family\s*:\s*[\'\"]*((\w+[ \-_]*)+\w*)[\'\",;>}]',html,re.I)
        if fiters:
            for i in fiters:                                #未考虑多字体同时写的情况，对多次出现的字体去重
                ff = i.group().lower()
                if not ff in self.htmlitems['font-family'].split('\t'):
                    self.htmlitems['font-family'] += ff+'\t'
        
    def charsetDect(self,url,html):
        '''
        :检测网页的字符集。网页源码含有的字符集和字体，以及第三方程序检测的字符集。但需要排除获取网站详细信息中常用的网页
        :charsetdet字典键值有:'font-family'字体集,'charset-web'网页给出的字符集,'encoding'检测出的字符集,'confidence'检测出的字符集可信度
        :param url:网页连接
        :param html:网页源码
        '''
        for xurl in cgv.excludeurl:                         #排除搜索引擎结果页面，获取网站信息页面的字符集判断
            if xurl in url:
                return html
        charsetdet = chardet.detect(html)                   #检测网页字符集
        charset = charsetdet['encoding']
        if charset:
            charset = charset.lower()
#             print '%s\tconfidence:%s\turl:%s'%(charset,charsetdet['confidence'],url)
            logging.info('%s\tconfidence:%s\turl:%s'%(charset,charsetdet['confidence'],url))
            if charset in cgv.CHARSET:                      #中文字符集使用范围最大的编码方式GB18030
                html = html.decode('gb18030','ignore')
#             else:html = html.decode('utf-8','ignore')
        return html
    
    def dealUrlError(self,url,e,retry):
        '''
        :处理获取网页时出现的错误
        :param url:网页连接
        :param e:网页返回错误
        :param retry:重试次数
        '''
        if hasattr(e,'reason'):
#             print 'Failed to reach a server. Reason:%s, url:%s, retry:%d'%(e.reason,url,retry)
            logging.error('Failed to reach a server. Reason: %s,url:%s,  retry: %d'%(e.reason,url,retry))
            for serror in cgv.SEVERROR:                     #列表中的错误直接跳过
                if serror in str(e.reason):
                    return False
            return True
        elif hasattr(e,'code'):
#             print 'The server could not fulfill the request. Error code: %s, retry: %d'%(e.code,retry)
            logging.error('The server could not fulfill the request. Error code: %s, retry: %d'%(e.code,retry))
            if e.code in cgv.ERRORCODE:                         #400之后的错误代码，对该url直接丢弃
                return False
            return True
        else:
#             print 'Get source unknown error: %s, retry: %d'%(e,retry)
            logging.error('Get source unknown error: %s, retry: %d'%(e,retry))
            return True
        
    def getHtmlSource(self,url,reply=False):
        '''
        :获取网页源代码。默认返回为空
        :param url:传入的链接地址
        :param reply:是否返回网页的字符集，字体信息和检测到的字符集及检测置信度
        '''
        self.html = ''                                      #默认返回值为空
        self.htmlitems = {'font-family':'',                 #网页元素
                          'charset-web':'',
                          'title':'',
                          'generator':'',}                  #默认返回结果为空
        if ggv.pterminate:                                  #手动停止程序
            if reply:
                return self.html,self.htmlitems
            return self.html                   
        retry = 3                                           #获取html内容最多尝试3次
        while retry:
            try:
                length = len(cgv.user_agents)
                index = random.randint(0,length-1)
                user_agent = cgv.user_agents[index]
                if not ggv.systemSetList[0] == '':          #设置了代理
                    opener = urllib2.build_opener(urllib2.ProxyHandler({'http':ggv.systemSetList[0]}),
                                                  urllib2.HTTPHandler(debuglevel=1))
                else:
                    opener = urllib2.build_opener(urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                request = urllib2.Request(url)
                request.add_header('Accept-Charset','GBK,utf-8;q=0.7,*;q=0.3')
#                 request.add_header('Accept-Encoding', 'gzip')
                request.add_header('Connection','keep-alive')
                request.add_header('User-agent', user_agent)
                response = urllib2.urlopen(request,timeout = 10)
                self.html = response.read()
#                 print self.html
                if ggv.pterminate:self.html
                if self.html:
                    if reply:self.getElement(self.html)     #提取网页其它元素辅助识别网页语言文字
                    self.html = self.charsetDect(url,self.html)                 #字符集检测，并正确编码
                response.close()
                if reply:
                    return self.html,self.htmlitems
                return self.html
            except urllib2.URLError,e:
                if ggv.pterminate: break                    #程序终止
                retry -= 1
                if not self.dealUrlError(e,url,retry):break
                if retry == 0:break
                self.randomSleep()
                continue
            except Exception,e:
                if ggv.pterminate: break                    #程序终止
#                 print 'get html source other error:%s. url:%s'%(e,url)
                logging.error('get html source other error: %s.url:%s'%(e,url))
                retry -= 1
                if retry == 0:break
                self.randomSleep()
                continue
        if reply:
            return self.html,self.htmlitems
        return self.html
    
class GetHtmlText():
    '''
    :提取返回页面的文本内容
    '''
    def delStyleScript(self,html):
        '''
        :删除网页源代码中的样式和脚本代码
        :param html:网页源码
        '''
        soup = BeautifulSoup(html)
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        return soup
    
    def getHtml(self,url,reply=False):
        '''
        :提取不含样式和脚本的网页源码
        :param url:网页连接
        :param reply:是否返回网页的字符集等信息
        '''
        ghs = GetHtmlSource()
        if reply:
            html,htmlitems = ghs.getHtmlSource(url, reply=True)
        else:
            html = ghs.getHtmlSource(url)
        if len(html) < 10:                                  #无法判断html是否为空
            if reply:
                return None,htmlitems
            return None
        soup = self.delStyleScript(html)
        if reply:
            return soup,htmlitems
        return soup

    def getText(self,soup):
        '''
        :通过BeautifulSoup提取网页的文本内容
        :param soup:经过BeautifulSoup处理过的网页源码
        '''
        content = soup.text
        content = ' '.join(content.split())
        return content
    
    def getHtmlText(self,url,reply=False):
        '''
        :获取网页文本内容的入口程序
        :param url:网页连接
        :param reply:是否返回网页字符集信息的标志
        '''
        if reply:
            html,htmlitems = self.getHtml(url, reply=True)
        else:
            html = self.getHtml(url)
        if html:
            if reply:
                logging.info('url:%s\tcharset:%s\tfont:%s\tgenerator:%s\ttitle:%s\t'
                             %(url,htmlitems['charset-web'],htmlitems['font-family'],htmlitems['generator'],htmlitems['title']))
                return self.getText(html),htmlitems
            return self.getText(html)
        else:
            if reply:return None,htmlitems
            return None

class GetIpAddress():
    '''
    :获取传入ip地址所属国家地区城市和服务提供商的信息。
    :获取的信息源为淘宝ip页面
    '''
    def getIpAddress(self,ip):
        time.sleep(0.1)                                     #淘宝规定的最大限制时间
        if ggv.pterminate:return None
        data = urllib2.urlopen(cgv.ipTaobao + ip)
        datadict = json.loads(data.read())
        for oneinfo in datadict:
            if "code" == oneinfo:
                if datadict[oneinfo] == 0:
                    return datadict["data"]["country"] + \
                        datadict["data"]["region"] + \
                        datadict["data"]["city"] + \
                        datadict["data"]["isp"] 
