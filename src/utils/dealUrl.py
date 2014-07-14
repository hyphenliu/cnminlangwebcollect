# -*- coding:utf-8 -*-
'''
Created on 2013年11月15日

@author: Hyphen.Liu
'''
from globalvar import crawlerGlobalVar as cgv

class PreProcess():
    def preProcess(self,url):
        '''
        :预处理传入的url链接，有些链接在程序获取的时候出现异常，
        :如，在http://之前有其他的字符，故本程序先将这些信息去除掉。
        :与此同时，需要判断该链接是否合法。
        '''
        for http in cgv.httpHead:                           #处理返回的异常的url链接
            if url.find(http) > 0:
                url = url[url.index(http):]
                urlt = url[len(http):]
                break
            else:
                urlt = url
        if urlt.find('/') > 0:
            urlt = urlt[:urlt.index('/')]
        urlt = urlt.split('.')
        if len(url) < 2:
            return None
        return url
    
class RemoveUrl():
    '''
    :搜索引擎经常搜索到一些常用的非少数民族语言文字的网站页面，
    :但这些页面含有少数民族语言文字并且这些页面量很大，
    :故在识别页面语言之前将这些网站过滤掉。
    '''
    def removeUrl(self,url):
        '''
        :判断给定的url是否为非少语网站或是否为非文档（.doc,.pdf,.xls,.txt等）
        :param url: 给定的url
        '''
        if not url:
            return None
        url = url.strip()
        for filetype in cgv.fileTypes:                      #常见文档类型的url需要排除
            if url.endswith(filetype):
                return None
        for rurl in cgv.removeUrl:                          #常见非少语网站的url需要排除
            if rurl in url:
                return None
        gd = GetDomain()
        domain = gd.getDomain(url)
        for removedomain in cgv.removeDomain:               #常见非少语网站的域名需要排除
            if domain:
                if domain.startswith(removedomain):
                    return None
        return domain

class DealUrl():
    '''
    :将传入的url分步的剥离出域名、子域名、子目录、二级子目录
    '''
    def extract(self,url):
        urlp = ''                                           #url头部协议
        extractResult = []
        extractResult.append(1)                             # 添加域名出现的次数
        pp = PreProcess()
        url = pp.preProcess(url)
        if url:
            for http in cgv.httpHead:                       # 保存头部协议，然后去除
                if url.startswith(http):
                    urlp = http
                    url = url[len(http):]
                    break
            if url.endswith('/'):
                url = url[:-1]
            extractResult.insert(0, urlp+url)               # 添加原始的url
            if url.find('/') > 0:
                url = url.split('/')
                if len(url) > 3:                            # 添加url二级目录
                    extractResult.insert(0, urlp+'/'.join(url[:3])+'/')
                elif len(url) == 3:
                    if (urlp+'/'.join(url)) == extractResult[-2]:extractResult.insert(0, ' ')
                    else:extractResult.insert(0, urlp+'/'.join(url))
                else:
                    extractResult.insert(0, ' ')
                if (urlp+'/'.join(url[:2])) == extractResult[-2]:extractResult.insert(0, ' ')
                else:extractResult.insert(0, urlp+'/'.join(url[:2]))    # 添加url子目录
            else:                                           #为二级目录和子目录添加占空符
                extractResult.insert(0, ' ')
                extractResult.insert(0, ' ')
            if isinstance(url,list):
                url = '/'.join(url)
            if url.find('/') > 0:                           # 添加子域名
                url = url[:url.index('/')+1]
            if urlp+url == extractResult[-2]:               #去除重复项
                extractResult.insert(0, ' ')
            else:
                extractResult.insert(0, urlp+url)   
            gd = GetDomain()                                # 添加域名
            domain = gd.getDomain(urlp+url)
            extractResult.insert(0, domain)    
        return extractResult
    
    def dealUrl(self,urls):
        '''
        :计算获取到的url页面所在域名的出现频次，但不计算常见非少语网站的频次
        '''
        dict = {}
        du = RemoveUrl()
        urls = set(urls)                                    #对url列表去重
        for url in urls:                                    #去除常见非少语url
            domain = du.removeUrl(url)
            if domain:
                rst = self.extract(url)
                if dict.has_key(domain):                    #计算域名出项的频率，暂时没有使用到这个频率
                    rst[-1] = int(dict[domain][-1]) + 1
                dict[domain] = rst[1:]
        return dict

class GetDomain():
    '''
    :单独获取传入url的子域名和域名的程序
    '''
    def getSubDomain(self,url):
        '''
        :获取子域名
        '''
        pp = PreProcess()
        url = pp.preProcess(url)
        for http in cgv.httpHead:                           #剥离传输协议
            if url.startswith(http):
                url = url[len(http):]
                break
        if url.find('/') > 0:                               #分离子域名
            url = url.split('/')
            return url[0]
        return url
    
    def getDomain(self,url):
        '''
        :获取传入url的域名
        '''
        url = self.getSubDomain(url)
        url = url.split('.')
        if len(url) < 2:
            return None
        for dm in cgv.subDomain:
            if url[-2] == dm:
                domain = '.'.join(url[-3:])
                break
            else:
                domain = '.'.join(url[-2:])
        if ':' in domain:                                   #去除url的端口号信息
            domain = domain.split(":")[0]
        return domain
