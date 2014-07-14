# -*- coding:utf-8 -*-
'''
Created on 2013年10月17日

@author: Hyphen
'''
LOGPATH = '../../log/'
URLTEMPF = ''
ENGTEMPF = ''
OUTTEMPF = ''
systemsetname = [u'收集网站语言：',u'搜索引擎选择：',u'关  键 字：',
                 u'编      码：',u'代      理：',u'线  程 数：',u'延 时(秒)：',
                 u'阈      值：',u'返回页面：']
siteInfo = [u'序号',u'域名',u'网站名称',u'首页地址',u'单位名称',
            u'单位性质',u'审核时间',u'备案号',u'服务器地址',
            u'服务器位置',u'全球排名',u'中文排名',u'编码',
            u'可信度',u'链接']                                   #需要收集网站的信息，共15项
siteInfoDB = [u'域名',u'网站名称',u'首页地址',u'单位名称',u'单位性质',
              u'审核时间',u'备案号',u'服务器地址',u'服务器位置',
              u'全球排名',u'中文排名',u'编码',u'可信度',u'链接',
              u'入库时间'] 
langs = [u'藏文', u'维吾尔文', u'蒙古文', u'哈萨克文', u'柯尔克孜文',
         u'朝鲜文', u'彝文', u'壮文', u'傣文']                       #目前能够收集的语言种类，共9种
langIds = ['bo', 'ug', 'mn', 'kk', 'ky', 'ko', 'ii', 'za', 'tl','all']  #语言的简写
engines = [u'谷歌', u'百度', u'360', u'雅虎', u'必应',u'所有']           #程序可以拽取的搜索引擎返回结果
engineIds = ['google','baidu','so','yahoo','bing','all']                #搜索引擎简写
codes = ['UNICODE','GBK','ASCII']                                       #关键字编码方式
wildcard = 'Excel files (*.xlsx)|*.xlsx|Excel files (*.xls)|*.xls'      #保存为excel表格的后缀形式
keywordslist = {'bo':[u'ཁབ',u'ལག',u'ལེན',u'罢邦︽',u'繻繴︽',],
                'ug':['ئوكيان','ئۇيغۇر','ئەڭ',],
                'mn':[u'',u'',u' ',u''],
                'kk':['ءبىز','ءبىر',],
                'ky':['كۉنۉ','سۉرۅتتۅر',],
                'ko':[u'사람들',u'일',],
                'ii':[u'ꉪꊇ',u'ꊿꊇ',],
                'za':['Cungguek',],
                'tl':[u'ᦷᦓᧃ',u'ᦺᦂᧈ',]}
fontfamily = {'mn':'symn,tsymn,sy20,saiyin,menksof,huritai,mgt-mhwt,mongolian',
              'bo':'bzd,tibetbt,himalaya'}
pterminate = False                                          #程序终止信号
pterminatestr = 'forcestop'                                 #作为返回值
window = []                                                 #主界面
scanindex = 0                                               #扫描结果计数
rstindex = 0                                                #识别出的网站计数
autostop = False                                            #程序自动运行结束标识
lang_use = ''                                               #搜索语言
engine_use = ['',]                                          #搜索引擎
keyword_use = ['',]                                         #关键字
gbs = ['bo','ug','kk','ky','ko','mn']                       #只能使用谷歌、360和必应搜索的语言

#需要从主界面获取到的信息填充变量，不同的语言需要选择不同的搜索引擎
#如，蒙古文不能在百度里搜索得到，如若要搜索蒙古文则搜索引擎列表不可
#出现百度引擎。根据主界面获取的结果，可能会出现搜索所有的语言的情况
#所以待检测的语言和待输入的关键字都是变量。所有的变量在主界面按下开
#始按钮时确定
langsDetect = []
engineGet = []
keywordsIn = [[]]                                           #二维列表

systemSetList = ['',10,30,40,30]                            #系统设置项：代理、线程个数、延时、阈值、最大引擎结果抓取页数
personSetList = [u'藏文',u'谷歌','དང་','UNINCODE']              #程序运行设置（语言、引擎、关键字、编码）
handInput = False                                           #默认非手工输入
gaugesize = 0
#菜单选项"关于"内容
aboutText = '''
<html>
<body bgcolor="#B7FF4A">
<center><table bgcolor="#FFE66F" width="100%" cellspacing="0"
cellpadding="0" border="0">
<tr>
    <td align="center"><h4><b>少数民族语言文字网站收集软件</b></h4></td>
    
</tr>
</table>
</center>
<p><b>少数民族语言文字网站收集软件</b>是一
个自动发现、识别少数民族语言文字网站
的软件。使用python编程语言编写，具有
自动发现和分析最新出现词语的功能。
</p>

<p><b>作者</b> 刘海峰  <b>邮箱</b> liuhaifeng_2011@126.com</p>
<center><p>Copyright &copy; 2013.</p></center>
</body>
</html>
'''
