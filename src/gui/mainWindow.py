# -*- coding:utf-8 -*-
'''
Created on Oct 2, 2013

@author: Hyphen

:文件名: mainWindow.py

:功能: 主界面的代码，但不包括其它的弹出窗口代码，如，关于本软件，系统设置等。

:基于: python2.7.3, wxpython2.8.12.1
'''

import os,time,gc,wx

import globalvar.guiGlobalVar as ggv
import globalvar.crawlerGlobalVar as cgv
from initialVar import InitialVar
from about import About
from syssetting import SysSetting
from startrun import StartRun
from utils.logger import Logger
from checkDB import CheckDB

MENU_LANG = wx.NewId()
MENU_ENG = wx.NewId()
MENU_SYS_SET = wx.NewId()
TOOLBAR_SYS_SET = wx.NewId()
WELCOMESTR = u'\r\n\t\t欢迎使用少数民族网站收集软件!\r\n\r\n\r\n'

class MainWindow(wx.Frame):
    def __init__(self, parent=None, title=u'少数民族文字网站收集软件'):
        '''
        :初始化界面：大小、启动画面背景颜色等
        :设置界面的布局等属性
        :param parent: none
        :param title: 界面标题
        '''
        wx.Frame.__init__(self, parent, 
                          title=title, 
                          size=(600, 450),
                          style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER |wx.MAXIMIZE_BOX))
        # 在主程序运行前显示欢迎图片
        bmp = wx.Image('../images/welcome.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        wx.SplashScreen(bmp, 
                        wx.SPLASH_CENTER_ON_PARENT | wx.SPLASH_TIMEOUT,
                        2500, 
                        None, 
                        -1)
        wx.Yield()
        time.sleep(2)
        # 系统变量：语言、搜索引擎、保存文档类型
        ggv.window  = self                                  #生成主框架
        self.CenterOnScreen()                               # 窗口显示在屏幕的正中间位置
        # 为主窗口标题添加图片
        self.icon = wx.Icon('../images/icon2.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.SetBackgroundColour('white')
        # 构建页面的主函数
        self._SetStatusBar()                                # 设置窗口大小和位置
        self._CreateMenubar()
        self._CreateToolBar()
        self._CreateSizer()                                 #创建容器及布局
        #显示系统默认值
        self.sysinfoUpdate()
        
        self.Show()                                         #窗口显示
        
    '''*********主要函数**********'''
    # 设置窗口的大小和位置
    def _SetStatusBar(self):
        '''
        :状态栏的设置，属性、大小、比例等。共分为3个状态栏，负责不同的状态提示
        :在第二状态栏设置添加进度条
        '''
        self.CreateStatusBar(3)                             # 添加3个状态栏。第一个为软件提示状态，第二个为程序运行状态，第三个为程序输出结果状态
        self.SetStatusText(u'欢迎使用少数民族语言文字网站收集软件')
        self.SetStatusWidths([-5,-5,-3])                                        #设置状态栏的比例
        self.gauge = wx.Gauge(self.StatusBar,-1,100,pos=(375,4),size=(80,16))   #第二个状态栏设置进度条，在识别网页语言是使用
        self.gauge.SetBezelFace(3)                          #进度条的显示风格
        self.gauge.SetShadowWidth(3)                        #进度条的宽度
        self.gauge.Hide()                                   #默认隐藏
        
    def _CreateMenubar(self):
        '''
        :创建菜单栏并添加子菜单和菜单项
        '''
        menubar = wx.MenuBar()                              #创建菜单栏
        for eachMenuData in self.menuData():                #添加子菜单及菜单项
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menubar.Append(self.createMenu(menuItems),menuLabel)
        self.SetMenuBar(menubar)                            #将菜单加入主界面显示
        
    def _CreateToolBar(self):
        '''
        :创建工具栏并添加工具图标
        '''
        toolbar = self.CreateToolBar()                      #创建工具栏
        for each in self.toolbarData():                     #添加工具
            self.createTool(toolbar,*each)
        toolbar.Realize()                                   #显示工具栏
        
    def _CreateSizer(self):
        '''
        :创建面板主容器，存放界面左侧属性面板和右侧显示面板
        '''
        leftSizer = wx.BoxSizer(wx.VERTICAL)                #使用Boxsizer作为容器存放左侧属性设置信息
        notebook = wx.Notebook(self,-1)                     #使用Notebook作为实时信息显示容器
        self.createLeftPanel(leftSizer)
        self.createNotebook(notebook)
        sizer = wx.BoxSizer(wx.HORIZONTAL)                  #左右侧容器水平放置到父容器中
        sizer.Add(leftSizer,2,wx.EXPAND,1)
        sizer.Add(notebook,5,wx.ALL | wx.EXPAND,1)
        self.SetSizer(sizer)                                #把父容器添加到主界面
    
    '''**********子函数 **********'''
    '''**********菜单子函数 **********'''
    def menuData(self):
        '''
        :菜单的各项信息以及相应的触发事件
        :self.On*的函数为点击菜单项出发的事件
        '''
        return ((u"文件",
                    (u'查看数据库', u'查询数据库', self.OnDBCheck),   #第二项为在第一状态栏显示的信息
                    ('','',''),                             #没有数据则后面的程序为之添加分隔符
                    (u'导入库', u'从外面文件导入数据库', self.OnImport),
                    (u'导出库', u'从数据库中导出数据', self.OnExport),
                    ('','',''),
                    (u'退出', u'退出程序', self.OnExit)),
                (u"编辑",
                    (u'语言选择',u'选择需要搜集的语言'),                 #长度为2代表该项还具有子菜单或子菜单项
                    ('','',''),
                    (u'搜索引擎选择',u'选择搜索引擎'),
                    ('','',''),
                    (u'系统设置', u'设置系统的代理服务器，延时，线程数，阈值等', self.OnSysSet),
                    ('','',''),
                    (u'修改数据库', u'修改数据库数据', self.OnDataEdit),
                    ('','',''),
                    (u'首选项',u'添加或设置系统功能',self.OnPreferenceSet)),
                (u"统计",
                    (u'最新入库', u'查看最新入库数据', self.OnNewIn),
                    (u'最新词语', u'查看最新词语', self.OnNewWord),
                    ('','',''),
                    (u'入库直方图 ', u'查看入库数据的直方图', self.OnTaproot),
                    ('','',''),
                    (u'词频走势', u'查看词语词频走势', self.OnTrend)),
                (u"关于",
                    (u'本软件', u'关于本软件的作者和版本', self.OnAbout),
                    ('','',''),
                    (u'更新软件', u'更新软件到最新版本', self.OnUpdate),
                    ('','',''),
                    (u'帮助', u'本软件帮助程序', self.OnHelp)))

    def createSubMenu(self,flag):
        '''
        :创建子菜单项
        :param flag:区分搜索引擎和语言选择子菜单项的创建
        '''
        handler = self.OnLangEngineSelect                   #搜索引擎选择和语言选择事件处理函数
        if flag == 1:
            lists = ggv.langs
        else:
            lists = ggv.engines
        subLabel = wx.Menu()
        for lbl in lists:                                   #添加菜单项
            menuItem = subLabel.Append(-1,'%s'%lbl,u'选择%s'%lbl,wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, handler, menuItem)
        return subLabel
    
    def createMenu(self,menuData):
        '''
        :创建菜单
        :param menuData:需要创建的菜单信息
        '''
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:                          #长度为2需要另行处理，因为其还有子项
                eachLabel,eachStatus = eachItem
                if eachLabel == u'语言选择':                #区分语言选择菜单还是搜索引擎选择菜单
                    submenu = self.createSubMenu(1)
                    menu.AppendMenu(MENU_LANG,eachLabel,submenu)
                else:
                    submenu = self.createSubMenu(2)
                    menu.AppendMenu(MENU_ENG,eachLabel,submenu)
            else:                                           #单独作为菜单项处理
                eachLabel, eachStatus, eachHandler = eachItem
                if not eachLabel:                           #空项处添加分割符
                    menu.AppendSeparator()
                    continue
                if eachLabel == u'系统设置':
                    menuItem = menu.Append(MENU_SYS_SET,eachLabel,eachStatus)
                else:
                    menuItem = menu.Append(-1, eachLabel, eachStatus)
                self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    '''**********工具栏子函数**********'''

    def toolbarData(self):
        '''
        :工具栏数据项
        '''
        return ((u'导入库','../images/import.png',u'从外面文件导入数据库',self.OnImport),
                (u'导出库','../images/export.png',u'从数据库导出数据',self.OnExport),
                ('','','',''),                              #数据为空则添加分隔符
                (u'最新入库','../images/newIn.png',u'最新入库的网站网址',self.OnNewIn),
                (u'最新单词','../images/newWord.png',u'最新发现词语',self.OnNewWord),
                ('','','',''),
                (u'直方图','../images/taproot.png',u'搜集结果中网站数量直方图',self.OnTaproot),
                (u'词频走势','../images/trend.png',u'最近搜集到的最常出现词语走势',self.OnTrend),
                ('','','',''),
                (u'修改数据库','../images/edit.png',u'修改数据库数据',self.OnDataEdit),
                (u'系统设置','../images/setting.png',u'设置系统的代理服务器，延时，线程数，阈值等',self.OnSysSet),
                ('','','',''),
                (u'帮助','../images/help.png',u'需要帮助请点击',self.OnHelp),
                ('','','',''),
                (u'退出','../images/exit.png',u'退出程序',self.OnExit))
    
    def createTool(self,toolbar,label,imagename,status,handler):
        '''
        :创建工具项
        :param toolbar:父容器，即创建到工具栏
        :param label:工具标签
        :param imagename:图标的名字
        :param status:鼠标移动到图标时第一状态栏显示的信息
        :param handler:事件处理函数
        '''
        if not label:                                       #label为空，添加分隔符
            toolbar.AddSeparator()
            return
        bmp = wx.Image(imagename,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        if label == u'系统设置':                            #程序运行时系统不可设置，故此处需要单独处理。锁定ID
            tool = toolbar.AddSimpleTool(TOOLBAR_SYS_SET,bmp,label,status)
        else:
            tool = toolbar.AddSimpleTool(-1,bmp,label,status)
        self.Bind(wx.EVT_MENU, handler, tool)
    '''********** 主体子函数 **********'''
    '''**********左边栏**********'''
    def createLeftPanel(self,ls):
        '''
        :创建左侧属性信息设置面板的各项信息和属性
        :param ls:父容器，即主界面左侧容器
        '''
        #系统设置BoxSizer
        sysSizers = wx.StaticBox(self,-1,'')                #系统设置静态box分组，使之能显示组名
        sp = wx.Panel(self,-1)                              #每组分配一个面板存放其它小器件
        wx.StaticText(sp,-1,
                      u'系统设置:',
                      pos=(10,5),
                      size=(60,25))
        self.sysButton = wx.Button(sp,-1,
                                   u'设  置',
                                   pos=(75,5),
                                   size=(70,25))
        wx.StaticText(sp,-1,
                      u'语言选择：',
                      pos=(10,35),
                      size=(60,25))
        self.langChoice = wx.Choice(sp,-1,
                                    choices = ggv.langs,
                                    pos=(75,35),
                                    size=(70,20))
        wx.StaticText(sp,-1,
                      u'搜索引擎：',
                      pos=(10,65),
                      size=(60,25))
        self.engChoice = wx.Choice(sp,-1,
                                   choices = ggv.engines,
                                   pos=(75,65),
                                   size=(70,20))
        sysSizer = wx.StaticBoxSizer(sysSizers,wx.VERTICAL) #添加静态box到容器boxsiser里
        sysSizer.Add(sp,1,wx.EXPAND,0)                      #设置容器的属性，可伸缩、边界为0
        #设置初始值
        self.langChoice.SetSelection(0)                     #设置默认选择值为语言列表的第一个语言
        self.engChoice.SetSelection(0)                      #设置默认选择搜索引擎列表第一个搜索引擎
        #绑定事件
        self.Bind(wx.EVT_BUTTON,self.OnSysSet,self.sysButton)                   #为系统设置按钮事件添加响应函数
        self.Bind(wx.EVT_CHOICE,self.OnLangSelect,self.langChoice)              #为语言选择下拉菜单事件添加响应函数
        self.Bind(wx.EVT_CHOICE,self.OnEngineSelect,self.engChoice)             #为搜索引擎选择下拉菜单事件添加响应函数

        #关键字BoxSizer
        kwSizers = wx.StaticBox(self,-1,'')                 #关键字设置静态分组
        kwp = wx.Panel(self,-1)
        self.radio1 = wx.RadioButton(kwp,-1,
                                     u'系统默认',
                                     pos=(10,5),
                                     size=(70,25),
                                     style = wx.RB_GROUP)
        self.radio2 = wx.RadioButton(kwp,-1,
                                     u'手工输入',
                                     pos=(80,5),
                                     size=(70,25))
        wx.StaticText(kwp,-1,
                      u'关键字：',
                      pos=(10,35),
                      size=(50,25))
        self.keywordh = wx.TextCtrl(kwp,-1,
                                    pos=(65,35),
                                    size=(80,20))
        wx.StaticText(kwp,-1,
                      u'编   码：',
                      pos=(10,65),
                      size=(50,25))
        self.codeChoice = wx.Choice(kwp,-1,
                                    choices = ggv.codes,
                                    pos=(65,65),
                                    size=(80,20))
        kwSizer = wx.StaticBoxSizer(kwSizers,wx.VERTICAL)
        kwSizer.Add(kwp,1,wx.EXPAND,0)                      #设置可伸缩等属性
        #设置初始值
        self.radio1.SetValue(1)                             #默认选择第一个按钮
        self.keywordh.Enable(False)                         #默认非手工输入
        self.codeChoice.SetSelection(0)                     #默认选择“unicode”编码方式
        self.codeChoice.Enable(False)
        for er in [self.radio1,self.radio2]:                #依次添加事件
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, er)
        
        #程序控制BoxSizer
        ctrlSizers = wx.StaticBox(self,-1,'')               #程序控制静态组
        cp = wx.Panel(self,-1)
        wx.StaticText(cp,-1,
                      u'程序运行：',
                      pos=(10,5),
                      size=(60,20))
        self.startB = wx.Button(cp,-1,
                                u'开  始',
                                pos=(75,2),
                                size=(70,22))
        wx.StaticText(cp,-1,
                      u'数 据  库：',
                      pos=(10,35),
                      size=(60,20))
        self.dbCheck = wx.Button(cp,-1,
                                 u'查  看',
                                 pos=(75,32),
                                 size=(70,22))
        ctrlSizer = wx.StaticBoxSizer(ctrlSizers,wx.VERTICAL)
        ctrlSizer.Add(cp)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.startB) #程序“开始”“运行”事件
        self.Bind(wx.EVT_BUTTON, self.OnDBCheck, self.dbCheck)                  #程序数据库查看按钮事件
        
        #Logo BoxSizer
        logoSizers = wx.StaticBox(self,-1,'')               #python logo静态组，只添加一张logo图片
        lp = wx.Panel(self,-1)
        logo = wx.Image('../images/logo.png')
        logo.Rescale(150,50)
        img = wx.BitmapFromImage(logo)
        logo = wx.StaticBitmap(lp,-1,
                               img,
                               wx.DefaultPosition,
                               style=wx.BITMAP_TYPE_PNG)
        logoSizer = wx.StaticBoxSizer(logoSizers,wx.VERTICAL)
        logoSizer.Add(lp,1,wx.EXPAND,0)
        
        #添加到左边栏BoxSizer
        ls.Add(sysSizer,3,wx.EXPAND,0)                      #添加系统设置组到左侧面板
        ls.Add(kwSizer,3,wx.EXPAND,0)                       #添加关键字设置组到左侧面板
        ls.Add(ctrlSizer,2,wx.EXPAND,0)                     #添加程序控制组到左侧面板
        ls.Add(logoSizer,2,wx.EXPAND,0)                     #添加python logo组到左侧面板
    '''**********右边**********'''
    def createSysinfoPanel(self):
        '''
        :创建系统设置信息显示面板及其属性
        '''
        self.sysinfo = wx.TextCtrl(self.siPanel,-1,'',
                                   pos=(5,5),
                                   size=(405,300),
                                   style=wx.TE_RICH|wx.TE_MULTILINE)
        self.sysinfo.SetEditable(False)
        self.sysinfo.SetLabel(WELCOMESTR)
        self.sysinfo.SetBackgroundColour('#DEFFAC')
        
    def createScanPanel(self):
        '''
        :创建程序运行扫描信息显示面板及其属性
        '''
        self.scanlog = wx.TextCtrl(self.scPanel,-1,'',
                                   pos=(5,5),
                                   size=(405,300),
                                   style=wx.TE_RICH|wx.TE_MULTILINE|wx.TE_DONTWRAP)
        self.scanlog.SetEditable(False)
        self.scanlog.SetLabel(u'扫描信息：\r\n\r\n')
        self.scanlog.SetBackgroundColour('#CCFF80')
        
    def createResultPanel(self):
        '''
        :创建程序运行结果信息显示面板及其属性
        '''
        self.rstlog = wx.TextCtrl(self.rstPanel,-1,'',
                                  pos=(5,5),
                                  size=(405,300),
                                  style=wx.TE_RICH|wx.TE_MULTILINE|wx.TE_DONTWRAP)
        self.rstlog.SetEditable(False)
        self.rstlog.SetLabel(u'搜索结果：\r\n\r\n')
        self.rstlog.SetBackgroundColour('#B7FF4A')
        
    def createNotebook(self,nb):
        '''
        :创建notebook容器子项
        :param nb:notebook容器
        '''
        self.siPanel = wx.Panel(nb,-1)                      #系统信息显示面板
        self.scPanel = wx.Panel(nb,-1)                      #扫描信息显示面板
        self.rstPanel = wx.Panel(nb,-1)                     #结果信息显示面板
#         self.nwPanel = wx.Panel(nb,-1)                      #发现新单词显示面板
        #创建相应面板
        self.createSysinfoPanel()
        self.createScanPanel()
        self.createResultPanel()
        #添加相应面板到父容器notebook中
        nb.AddPage(self.siPanel,u'系统信息')
        nb.AddPage(self.scPanel,u'扫描信息')
        nb.AddPage(self.rstPanel,u'扫描结果')
#         nb.AddPage(self.nwPanel,u'最新词汇')
    
    def sysinfoUpdate(self):
        '''
        :更新系统设置信息的显示
        '''
        infolist = []
        infolist.extend(ggv.personSetList)
        infolist.extend(ggv.systemSetList)
        if not ggv.handInput:
            infolist[2] = u'系统值'
            infolist[3] = u'系统值'
        self.sysinfo.SetValue(WELCOMESTR)                   #重置欢迎语句
        for i,inf in enumerate(infolist):
            if i == 7:inf = 0.01 * inf                      #阈值乘以0.01
            if inf == '':inf = u'无'
            self.sysinfo.AppendText('\t%s\t\t\t%s\r\n'%(ggv.systemsetname[i],inf))
    
    def scanlogUpdate(self,logstring):
        '''
        :扫描信息同步更新
        :param logstring:需要更新的信息
        '''
        ggv.scanindex += 1
        self.scanlog.AppendText(u'序号%04d: \r\n%s\r\n'%(ggv.scanindex,logstring))
        
    def rstlogUpadate(self,rstlogstring):
        '''
        :更细扫描结果的信息
        :param rstlogstring:扫描结果信息
        '''
        ggv.rstindex += 1
        self.rstlog.AppendText(u'序号%04d: \r\n%s\r\n'%(ggv.rstindex,rstlogstring))
    
######################事件响应程序##################
    '''**********事件响应函数**********'''
    def OnImport(self, event):
        '''
        :导入文件事件响应
        :param event:事件值
        '''
        self.dirname = ''
        dlg = wx.FileDialog(self, 
                            u'选择需要导入的Excel文件', 
                            self.dirname, 
                            "", 
                            wildcard = ggv.wildcard, 
                            style = wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:                     #判断是否确认导入
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
    
    def OnExport(self, event):
        '''
        :文件导出事件响应
        :param event:事件值
        '''
        dlg = wx.FileDialog(self,'Save data as...',
                            os.getcwd(),
                            style = wx.SAVE|wx.OVERWRITE_PROMPT,
                            wildcard = ggv.wildcard)
        if dlg.ShowModal() == wx.ID_OK:                     #确认导出
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:           #确保文件名有后缀
                filename = filename + '.xls'
            self.filename = filename
        dlg.Destroy()
        
    def OnExit(self, event):
        '''
        :程序退出事件响应
        :功能：释放内存
        :param event:事件值
        '''
        self.StopThreads()
        gc.collect()                                        #释放内存
        self.Destroy()
    
    def OnLangEngineSelect(self,event):
        '''
        :语言选择和搜索引擎选择事件响应
        :param event:
        '''
        menubar = self.GetMenuBar()                         #获取到菜单栏
        item = menubar.FindItemById(event.GetId())          #通过ID得到菜单项的值
        if item:
            itemlabel = item.GetLabel()                     #获取菜单项的标签值
            if itemlabel in ggv.langs:
                ggv.personSetList[0] = itemlabel
                self.langChoice.SetSelection(ggv.langs.index(itemlabel))        #同步更新主界面左侧栏的语言选择值
                if itemlabel == u'所有语言':                #如果选择全部语言则禁止手工输入关键字
                    self.OnEnableFalse2()
                else:
                    self.OnEnableTrue2()
            else:
                ggv.personSetList[1] = itemlabel
                self.engChoice.SetSelection(ggv.engines.index(itemlabel))       #同步更新主界面左侧栏的引擎选择值
        self.sysinfoUpdate()                                #同时更新系统设置信息面板显示值

    def OnLangSelect(self,event):
        '''
        :语言选择下拉框事件响应
        :param event:事件值
        '''
        lang = event.GetEventObject().GetLabel()
        ggv.personSetList[0] = lang
        if lang == u'所有语言':
            self.OnEnableFalse2()
        else:
            self.OnEnableTrue2()
        self.sysinfoUpdate()                                #同时更新系统设置信息面板显示值
        
    def OnEngineSelect(self,event):
        '''
        :搜索引擎选择下拉框事件响应
        :param event:事件值
        '''
        ggv.personSetList[1] = event.GetEventObject().GetLabel()
        self.sysinfoUpdate()                                #同时更新系统设置信息面板显示值
    
    def OnRadio(self,event):
        '''
        :单选组radio按钮事件响应，即关键字的手工输入或选择系统值
        :param event:
        '''
        text = event.GetEventObject().GetLabel()
        if text == u'手工输入':
            ggv.handInput = True                            #设置手工输入
            self.keywordh.Enable(True)
            self.codeChoice.Enable(True)
        else:
            ggv.handInput = False                           #设置非手工输入
            self.keywordh.Enable(False)
            self.codeChoice.Enable(False)
        
    def OnEnableTrue2(self):
        '''
        :程序停止后所有的可选选项重启恢复程序运行之前的状态
        '''
        self.radio1.Enable(True)
        self.radio2.Enable(True)
        if self.radio2.GetValue():                          #判断关键字的输入方式
            self.keywordh.Enable(True)
            self.codeChoice.Enable(True)
        
    def OnEnableTrue(self):
        '''
        :程序停止后所有的可选选项重启恢复程序运行之前的状态
        '''
        menubar = self.GetMenuBar()
        menubar.Enable(MENU_LANG,True)                      #允许菜单栏语言的选择
        menubar.Enable(MENU_ENG,True)                       #允许菜单栏搜索引擎的选择
        menubar.Enable(MENU_SYS_SET,True)                   #允许菜单栏系统设置
        toolbar = self.GetToolBar()                     
        toolbar.EnableTool(TOOLBAR_SYS_SET,True)            #允许工具栏系统设置图标
        self.startB.SetLabel(u'开  始')                       #开始按钮标签值改变
        self.langChoice.Enable(True)                        #允许语言选择下拉菜单的使用
        self.sysButton.Enable(True)                         #允许系统设置按钮的使用
        self.engChoice.Enable((True))                       #允许搜索引擎选择下拉菜单的使用
        self.OnEnableTrue2()                                #其它允许选项
    
    def OnEnableFalse2(self):
        '''
        :程序处于运行状态很多的功能需要禁止
        :如，关键字的设置
        '''
        self.radio1.Enable(False)
        self.radio2.Enable(False)
        if self.radio2.GetValue():
            self.keywordh.Enable(False)
            self.codeChoice.Enable(False)
    
    def OnEnableFalse(self):
        '''
        :程序处于运行状态很多的功能需要禁止
        :如，菜单栏的语言选择、搜索引擎选择和系统设置菜单不可用
        :以及，工具栏的系统设置图标不可点击、语言选择和搜索引擎选择下拉框不可用
        '''
        menubar = self.GetMenuBar()
        menubar.Enable(MENU_LANG,False)
        menubar.Enable(MENU_ENG,False)
        menubar.Enable(MENU_SYS_SET,False)
        toolbar = self.GetToolBar()
        toolbar.EnableTool(TOOLBAR_SYS_SET,False)
        self.startB.SetLabel(u'结  束')
        self.langChoice.Enable(False)
        self.sysButton.Enable(False)
        self.engChoice.Enable((False))
        self.OnEnableFalse2()                               #关键字不可选择或输入
        
    def InitStart(self):
        '''
        :初始化界面显示信息，各种与显示相关的信息重置或清空
        '''
        Logger()  
        click = 0
        ggv.pterminate = False
        ggv.scanindex = 0                                   #扫描信息索引重置
        ggv.rstindex = 0                                    #收集结果信息索引重置
        self.SetStatusText('',1)                            #第二状态栏信息清空
        self.SetStatusText('',2)                            #第三状态栏信息清空
        self.gauge.SetValue(0)                              #进度条清零
        self.scanlog.SetValue(u'扫描信息：\r\n\r\n')             #扫描信息重置
        self.rstlog.SetValue(u'搜索结果：\r\n\r\n')              #搜索结果信息重置
        tempfiles = [ggv.URLTEMPF,ggv.ENGTEMPF,ggv.OUTTEMPF]
        tempfile = [i for i in tempfiles if os.path.exists(i)]
        if len(tempfile) > 0:
            md = wx.MessageDialog(self,
                                  u'检测到上次程序未完全运行完成，\r是否继续运行上次程序？',
                                  u'继上次运行提示',
                                  wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
            md.CenterOnParent()
            click = md.ShowModal()
        if click == wx.ID_NO:                               #不继续之前的程序，重新开始
            for j in range(len(tempfiles)):
                if os.path.isfile(tempfiles[j]):
                    os.remove(tempfiles[j])
        if click == wx.ID_CANCEL:                           #不开始程序
            return False
        return True
       
    def OnStart(self,event):
        '''
        :程序开始运行或手动结束函数
        :主要功能：初始化与语言设置等相关的变量
        :param event:
        '''
        if self.startB.GetLabel() == u'开  始':               #程序开始
            if ggv.handInput:                               #如果是手工输入则提取手工输入信息
                if not self.keywordh.GetValue():
                    wx.MessageBox(u'请添输入关键字',
                                  '手工输入',
                                  wx.OK|wx.ICON_ERROR)
                    return
                else:
                    ggv.personSetList[2] = self.keywordh.GetValue()
                    ggv.personSetList[3] = self.codeChoice.GetLabel()
            self.sysinfoUpdate()
            InitialVar()                                    #初始化，并检测上次运行的结果
            if not self.InitStart():                        #选择Cancel按钮，程序不运行
                return
            self.OnEnableFalse()                            #禁止程序属性设置
            sr = StartRun(self)                             #开始运行程序
            cgv.threadlist.append(sr)                       #使用线程引导主程序运行，若不使用线程将导致界面无法响应其它的事件，如拖动窗口等
            sr.start()                                      #程序运行
        else:                                               #程序停止
            md = wx.MessageDialog(self,
                                  u'确定要停止程序吗？',
                                  u'终止提示',
                                  wx.YES_NO|wx.ICON_QUESTION)
            md.CenterOnParent()
            if md.ShowModal() == wx.ID_YES:                 #确定终止程序运行
                ggv.pterminate = True                       #发送终止信号
                self.OnEnableTrue()                         #允许程序属性设置
                self.StopThreads()                          #停止所有的线程
                self.SetStatusText(u'程序被停止',1)          #状态栏显示程序被停止信息
                self.SetStatusText('',2)                    #第三状态栏信息清空
                self.gauge.Hide()
                    
    def OnStop(self): 
        '''
        :程序运行完毕
        :功能：清理数据，在状态栏显示相关信息，弹出任务完成对话框
        '''
        '''供其它程序调用，如，主程序已经运行完毕，即调用'''
        ggv.pterminate = False
        self.StopThreads()
        ms = ggv.personSetList[0]+u'网站收集任务完成'
        wx.MessageBox(ms,
                      u'任务完成',
                      wx.OK|wx.ICON_INFORMATION)
        self.SetStatusText(u'程序运行完成',1)
        self.gauge.Hide()
        self.OnEnableTrue()
        
    def StopThreads(self):
        '''
        :清空线程队列并对每个线程发送终止信号
        '''
        while cgv.threadlist:
            thread = cgv.threadlist[0]
            thread.stop()
            cgv.threadlist.remove(thread)
        
    def OnDBCheck(self,event):
        '''
        :仅仅查看数据库不具备编辑数据库的功能
        :param event:按钮事件
        '''
        CheckDB(edit=False)
    
    def OnSysSet(self, event):
        '''
        :系统设置窗口
        :功能：设置代理、阈值等属性信息
        :param event:按钮事件
        '''
        ss = SysSetting(self)
        ss.ShowModal()                                      #主界面显示
        ss.Destroy()
    
    def OnDataEdit(self, event):
        '''
        :查看和编辑数据库
        :param event:按钮事件
        '''
        CheckDB(edit=True)
    
    def OnPreferenceSet(self,event):
        pass
    
    def OnNewIn(self,event):
        pass
    
    def OnNewWord(self,event):
        pass
    
    def OnTaproot(self,event):
        pass
    
    def OnTrend(self,event):
        pass
    
    def OnAbout(self, event):
        '''
        :显示软件的功能等信息
        :param event:事件值
        '''
        dlg = About(self)
        dlg.ShowModal()                                     #显示“关于”窗口
        dlg.Destroy()
        
    def OnUpdate(self,event):
        pass
    
    def OnHelp(self,event):
        pass

class Main():
    '''
    :主界面程序入口
    '''
    app = wx.App(False)                                     #创建wx app
    frm = MainWindow()
    frm.Show()
    app.MainLoop()
    
if __name__ == '__main__':
    Main()