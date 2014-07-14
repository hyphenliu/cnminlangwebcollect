# -*- coding: utf-8 -*-
'''
Created on 2013年11月14日

@author: Hyphen.Liu
'''

# 不同的user agents 伪装浏览器浏览网页
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', 
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', 
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0', 
               'IBM WebExplorer /v0.94', 
               'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', 
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 
               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', 
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25', 
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36', 
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
#headers没有在程序中出现，只做测试使用
headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13", 
                    #"User-Agent" = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13", 
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
                    "Accept-Language":"zh-cn,zh;q=0.5", 
                    #"Accept-Encoding":"gzip,deflate", 
                    "Accept-Charset":"GB2312,utf-8;q=0.7,*;q=0.7", 
                    "Keep-Alive":"115", 
                    "Connection":"keep-alive" 
                   }
excludeurl = ['.360.cn','.google.','.baidu.','.yahoo.',
              '.bing.','.so.','.alexa.','.taobao.']         #获取这些网站内容时不记录和打印其网站字符集
subDomain = ['com','gov','edu','org','net','ac','mil']      #提取域名需要考虑的情况，如，com.cn等
url360 = 'http://webid.360.cn/complaininfo.php?domain='     #从360查询备案号
beiAnInfoItem = [u'网站域名：',u'网站名称:', u'网站首页地址:',
                 u'主办单位名称:',u'主办单位性质:',u'审核时间:',
                 u'网站备案/许可证号:',u'信息来源:']                    #备案号等信息
beiAnNoInfo = u'未向工信部提交ICP备案'                        # 没有备案号的信息
alexaUrl = 'http://www.alexa.com/siteinfo/'                 #全球Alexa排名网站url地址
alexInfo = [u'全球综合排名第',u'位，中文排名第',u'位。']                    #Alexa排名特征
alexNoInfo = u'没有排名数据'
ipTaobao = 'http://ip.taobao.com/service/getIpInfo.php?ip=' # 从淘宝查找ip地址的位置
google_url = 'http://www.google.com.hk/search?hl=en&q='     #谷歌搜索引擎url地址
google_url_end = ''
baidu_url = 'http://www.baidu.com/s?&wd='                   #百度搜索引擎url地址
baidu_url_end = ''
so_url = 'http://www.so.com/s?q='                           #360搜索引擎url地址
so_url_end = ''
yahoo_url = 'http://www.yahoo.cn/s?q='                      #雅虎搜索引擎url地址
yahoo_url_end = ''
bing_url = 'http://cn.bing.com/search?q='                   #必应搜索引擎url地址
bing_url_end = ''
#获取不同搜索引擎返回结果的不同参数。即，标记返回结果页面的链接参数<h3>等，指示下一页参数next page 等
google_engine = ['google',google_url,google_url_end,'',
                 '&start=',['div','id','navcnt'],'Next','en'] #谷歌搜索引擎返回结果特征
baidu_engine = ['baidu',baidu_url,baidu_url_end,'',
                '&pn=',['p','id','page'],u'下一页','en']       #百度搜索引擎返回结果特征
so_engine = ['so',so_url,so_url_end,'',
             '&pn=',['div','id','page'],u'下一页','en']        #360搜索引擎返回结果特征
yahoo_engine = ['yahoo',yahoo_url,yahoo_url_end,'',
                '&page=',['div','class','page'],u'下一页','en']#雅虎搜索引擎返回结果特征
bing_engine = ['bing',bing_url,bing_url_end,'',
               '&first=',['div','class','sb_pag'],u'下一页','en']                  #必应搜索引擎返回结果特征
engines = [google_engine,baidu_engine,so_engine,yahoo_engine,bing_engine]       #搜索引擎列表，本处只做测试使用
httpHead = ['http://','https://','ftp://','ftps://','sftp://',
            'http:/','https:/','ftp:/','ftps:/','sftp:/']   #所有的http协议
removeDomain = ['apple.','kaoyan.','30edu.','baidu.','yahoo.','so.',
                'google.','qq.','sina.','163.','blogbus.','ifeng.',
                'diandian.','cnblogs.','sohu.','tianya.','lofter.',
                'csdn.','bokee.','cnfol.','eastmoney.','hexun.',
                'smzdm.','blogchian.','songshuhui.','williamlong.',
                'blogcn.','36kr.','ifangr.','docin.','wendang.',
                'nexoncn.','doc35.','4shared.','douban.','soso.',
                'doc88.','xiangdang.','scribd.','docstoc.','youku.',
                'tudou.','ku6.','56.','6.','v1.','xunlei.','youtube.',
                'letv.','pps.','pptv.','wasu.','baomihua.','iqiyi.',
                'kankan.','verycd.','weibo.','renren.','kaixin001.',
                '51.','pengyou.','chinaren.','wealink.','facebook.',
                'twitter.','myspace.','linkedin.','myspace.','1ting.',
                'yue365.','kuwo.','xiami.','duomi.','chinaz.','dns558.',
                'baike.','iciba.','360doc.','i-part.','abkai.','appgame.',
                'gxsd.','kdnet.','cwshk.','answers.','studa.','chaoxing.',
                'wzk.','diyifanwen.','wenmi114.','51ppt.','ybask.','115.',
                '3456.','zuowen.','zww.','hudong.','uu456','kaoyan001.',
                '5sing.','2000y.','book118.','565656.','360edu.','58.',
                'sogou.','12306.','12321.','miibeian.','bjtime','123cha.',
                'xiazaiba.','huochepiao.','9ku.','myeducs.','book118.',
                '30edu.','cersp.','chinadmd.','microsoft.','kuocha.',
                'blogspot.','blogger.','fl168.','w3.','yaolan.','kdd.',
                'haodic.','tez321.','kongfz.','cnki.','meile.','ewsos.',
                'jkmyi.','cqvip.','fwol.','xbdj.','mobuk.','jd.','amazon.',
                '766.','tvmao.','cnki.']              #常见的非少数民族语言网站域名，对搜索引擎返回结果进行过滤
removeUrl = ['zh.wikipedia.org','en.wikipedia.org']
fileTypes = ['.doc','.docx','.txt','.pdf','.xls','.xlsx','.ppt','.pptx','.zip','.rar']        #排除返回的结果里含有的常见文件
threadlist = []                                             #线程列表，存储已经运行的线程
ERRORCODE = [204,304,400,401,403,404,500,501,502,503,504,505]
CHARSET = ['big5','gbk','gb2312','windows-1255','euc-tw','hz-gb-2312','iso-2022-cn']
SEVERROR = ['Bad Request','Not Found','Forbidden','getaddrinfo failed',
            'Errno 10054','Errno 10060','Errno 10061']