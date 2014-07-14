# -*- coding:utf-8 -*-
'''
Created on 2014年1月11日

@author: Hyphen.Liu
'''
import wx,os,re,wx.grid,webbrowser

from utils.sqlite3DB import DBstorage
from utils.excel import ExcelWriter
import globalvar.guiGlobalVar as ggv

class CheckDB(wx.Frame):
    '''
    :查看或编辑数据库数据
    :根据参数选择查看或编辑数据库数据
    :其中某些数据不允许编辑
    '''
    def __init__(self,parent=ggv.window,title=u'数据库查看',edit=False):
        '''
        :初始化参数
        :param parent:主界面窗口
        :param title:窗口标题
        :param edit:编辑标志
        '''
        wx.Frame.__init__(self,
                          parent=ggv.window,
                          title=title,
                          size=(620,400),
                          style=wx.DEFAULT_FRAME_STYLE)
        self.edit = edit
        self.colwidth = [2,2,2,2,1,2,3,3,3,2,2,1,2,4,2]     #列表宽度
        self.singleflag = False
        self.lang = u'藏文'                                   #默认藏文
        self.editdata = ['',]
        
        self.CenterOnParent()
        self.CreateSizer()
        self.CreateStatusBar(2)                             #创建2个状态栏，一个显示语言，一个显示查询结果个数
        self.SetStatusText(u'查询藏文网站数据',0)
        self.PopupMenuFunc()
        
        self.SetMinSize((600,300))                          #为了便于显示数据，设置最小窗口
        #self.SetMaxSize((1300,650))    
        self.Show()                                         #显示窗口
        
    def createheader(self):
        '''
        :创建窗口上方的容器面板 ，即查询的信息选项
        '''
        self.langpanel = wx.Panel(self,-1)                  #查询语言下拉面板
        wx.StaticText(self.langpanel,-1,
                      u'查询语言:',
                      pos=(5,12),
                      size=(55,30))
        self.langlachoice = wx.Choice(self.langpanel,-1,
                                      choices = ggv.langs,
                                      pos=(65,10),
                                      size=(70,30))
        self.langlachoice.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.langlachoice)
        
        self.choicepanel = wx.Panel(self,-1)                #单表和总表选择面板
        self.radio1 = wx.RadioButton(self.choicepanel,-1,
                                     u'单表',pos=(5,8),
                                     size=(45,25),
                                     style = wx.RB_GROUP)
        self.radio2 = wx.RadioButton(self.choicepanel,-1,
                                     u'总表',
                                     pos=(55,8),
                                     size=(45,25))
        self.radio2.SetFocus()                              #默认查询总表
        for er in [self.radio1,self.radio2]:                #添加事件
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, er)
        
        self.datepanel = wx.Panel(self,-1)                  #日期输入面板
        wx.StaticText(self.datepanel,-1,
                      u'入库时间:',
                      pos=(5,12),
                      size=(55,30))
        self.startdate = wx.TextCtrl(self.datepanel,-1,
                                     '',
                                     pos=(60,10),
                                     size=(70,20))
        self.hyphenst = wx.StaticText(self.datepanel,-1,
                                      '-',
                                      pos=(135,12),
                                      size=(10,30))
        self.enddate = wx.TextCtrl(self.datepanel,-1,
                                   '',
                                   pos=(145,10),
                                   size=(70,20))
        
        self.buttonpanel = wx.Panel(self,-1)                #查询按钮面板
        self.checkbutton = wx.Button(self.buttonpanel,-1,
                                     u'查询',
                                     pos=(5,7),
                                     size=(50,25))
        self.savebutton = wx.Button(self.buttonpanel,-1,
                                    u'导出',
                                    pos=(60,7),
                                    size=(50,25))
        self.Bind(wx.EVT_BUTTON, self.OnCheck, self.checkbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSaveExport, self.savebutton)
        self.savebutton.Enable(False)
        #将所有的面板集成到父容器中
        self.headsizer.Add(self.langpanel,4,wx.EXPAND,0)
        self.headsizer.Add(self.choicepanel,3,wx.EXPAND,0)
        self.headsizer.Add(self.datepanel,6,wx.EXPAND,0)
        self.headsizer.Add(self.buttonpanel,3,wx.EXPAND,0)
        
    def creategrid(self):
        '''
        :创建显示表格
        :默认为0行，15列，数据添加时自动添加行数
        '''
        self.grid = wx.grid.Grid(self,-1,size=(1,1))
        self.grid.CreateGrid(0,15)                          #创建列数
        self.grid.EnableEditing(0)
#         self.grid.EnableGridLines(0)
        self.grid.EnableDragGridSize(0)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        for i,item in enumerate(ggv.siteInfoDB):            #创建表头
            self.grid.SetColLabelValue(i,item)
            self.grid.SetColMinimalWidth(i,self.colwidth[i])
        self.grid.SetColLabelSize(25)
        self.grid.SetRowLabelSize(40)
        attr = wx.grid.GridCellAttr()                       #设置某些列不可编辑
        attr.SetReadOnly()
        #第1列、13列、14列、15列不可编辑
        self.grid.SetColAttr(0,attr)
        self.grid.SetColAttr(12,attr)
        self.grid.SetColAttr(13,attr)
        self.grid.SetColAttr(14,attr)
        
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnChange)
        
    def CreateSizer(self):
        '''
        :创建boxsizer容器来包含所有的组件
        '''
        self.headsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.createheader()                                 #创建窗口上方控件
        
        self.creategrid()                                   #创建表体
        
        self.outsizer = wx.BoxSizer(wx.VERTICAL)            #最大的容器
        self.outsizer.Add(self.headsizer,0,wx.EXPAND,1)
        self.outsizer.Add(self.grid,5,wx.EXPAND,0)
        
        self.SetSizer(self.outsizer)                        #将最大的容器添加到窗口
        
    def PopupMenuFunc(self):
        '''
        :为数据库编辑赋予右键弹出菜单功能
        '''
        self.popupmenu = wx.Menu()                          #添加右键弹出菜单功能
        if self.edit:
            self.SetTitle(u'数据库编辑')
            self.savebutton.SetLabel(u'保存')
            self.grid.EnableEditing(1)
#             self.radio1.Enable(False)                         #仅允许编辑总表，为了数据的一致性维持，分表不允许编辑
            delitem = self.popupmenu.Append(-1,u'删除本数据项')
            self.Bind(wx.EVT_MENU, self.OnDeleteData, delitem)
        openitem = self.popupmenu.Append(-1,u'在浏览器打开链接')
        self.Bind(wx.EVT_MENU, self.OnOpenLink, openitem)
        self.Bind(wx.EVT_CONTEXT_MENU, self.ShowPopupMenu)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,self.ShowPopupMenu)
        
    def OnChoice(self,event):
        '''
        :语言选择下拉框事件响应
        :param event:事件值
        '''
        self.lang = self.langlachoice.GetLabel()
        self.SetStatusText(u'查询%s网站数据'%self.lang,0)
        
    def OnRadio(self,event):
        '''
        :程序选择单选按钮事件响应
        :param event:事件值
        '''
        text = event.GetEventObject().GetLabel()
        if text == u'单表':
            self.enddate.Hide()
            self.hyphenst.Hide()
            self.singleflag = True
        else:
            self.enddate.Show()
            self.hyphenst.Show()
            self.singleflag = False
        
    def OnCheck(self,event):
        '''
        :查询按钮动作事件响应
        :param event:事件值
        '''
        ''''''
        self.SetStatusText('',1)                            #清空状态栏信息
        self.savebutton.Enable(False)                       #重新获取数据，save按钮不可用
        if self.grid.GetNumberRows() > 0:                   #再次查询时清空还原
            self.grid.ClearGrid()
            self.grid.DeleteRows(0,self.grid.GetNumberRows())
        dbs = DBstorage()
        self.langid = ggv.langIds[ggv.langs.index(self.langlachoice.GetLabel())]    #查询是语种数据库
        self.datestart = self.startdate.GetValue()          #获取输入的日期
        if not self.ShowMessage(self.datestart): return None                        #判断日期是否为空
        if self.singleflag:                                 #查询单个数据表格
            langtable = self.langid+self.datestart          #构建待查询数据表名称
            self.dataitems = dbs.fetchall_data_single(langtable)#查询数据库
        else:
            self.dateend = self.enddate.GetValue()
            if not self.ShowMessage(self.dateend):return None                       #判断日期是否为空
            if self.dateend < self.datestart:self.dateend,self.datestart = (self.datestart,self.dateend)    #若截止日期小于开始日期则调换
            self.datestart = self.datestart[:4] + '-' + self.datestart[4:6] + '-' + self.datestart[6:]
            self.dateend = self.dateend[:4] + '-' + self.dateend[4:6] + '-' + self.dateend[6:]
            if not self.ShowMessage(self.dateend):return None
            self.dataitems = dbs.fetchall_data_total(self.langid, (self.datestart,self.dateend))
        if not self.dataitems:
            wx.MessageBox(u'这个时间段没有%s数据入库，\n请尝试查询其他时间段数据。'%self.lang,
                          u'找不到相关数据',
                          wx.OK|wx.ICON_INFORMATION)
            self.SetStatusText(u'查询到0个结果',1)
            return None
        self.grid.AppendRows(len(self.dataitems))
        self.SetStatusText(u'查询到%s个结果'%len(self.dataitems),1)
        for i,row in enumerate(self.dataitems):
            for j,col in enumerate(row[1:]):
                self.grid.SetCellValue(i,j,str(col).encode('utf8'))
        self.savebutton.Enable(True)
    
    def ShowMessage(self,datastr=None):
        '''
        :日期输入错误信息提示窗口
        :param datastr:传入的日期字符串
        '''
        regstr = re.compile(r'^2\d{3}((0([1-9]{1}))|(1[0|1|2]))(([0-2]([0-9]{1}))|(3[0|1]))$')              #判断日期是否合法
        if not datastr or datastr == ' ':
            wx.MessageBox(u'请输入查询的日期',
                          u'日期为空',
                          wx.OK|wx.ICON_WARNING)
            return False
        else:
            if not regstr.match(self.startdate.GetValue()): #日期不合法
                wx.MessageBox(u'请输入8位有效日期\n不要包含其他字符',
                              u'日期格式错误！',
                              wx.OK|wx.ICON_ERROR)
                return False
        return True
    
    def OnSaveExport(self,event):
        '''
        :保存和导出按钮事件响应
        :param event:事件值
        '''
        if self.savebutton.GetLabel() == u'导出':
            dlg = wx.FileDialog(self,u'保存为...',\
                                os.getcwd(),\
                                style = wx.SAVE|wx.OVERWRITE_PROMPT,\
                                wildcard = ggv.wildcard)
            dlg.CenterOnParent()
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                ExcelWriter(filename,self.lang,self.dataitems)
            dlg.Destroy()
        else:
            if self.singleflag:
                self.langid = self.langid + self.datestart
            dlg = wx.MessageDialog(self,
                                   u'确定修改数据库？所有修\n改的数据都将写会数据库',
                                   u'数据修改确认',
                                   wx.YES_NO|wx.ICON_QUESTION)
            dlg.CenterOnParent()
            if dlg.ShowModal() == wx.ID_YES:
                dbs = DBstorage()
                dbs.update_data_many(self.langid, self.editdata)
            else:
                return None
            
    def OnChange(self,event):
        '''
        :响应修改值事件
        :将修改的值和所在的位置对应的域名保存到列表以备后续写回库中
        :param event:事件值
        '''
        r = event.GetRow()
        c = event.GetCol()
        v = self.grid.GetTable().GetValue(r,c)
        domain = self.grid.GetTable().GetValue(r,0)
        self.editdata.append(((v,domain),c))
        
    def ShowPopupMenu(self,event):
        '''
        :捕捉鼠标位置并显示弹出菜单
        :param event:
        '''
        self.delrow = event.GetRow()
        pos = event.GetPosition()
        self.grid.PopupMenu(self.popupmenu, pos)
        
    def OnDeleteData(self,event):
        '''
        :删除正行数据事件响应
        :param event:事件值
        '''
        dlg = wx.MessageDialog(self,
                               u'确定删除本数据项？\n此操作将无法撤回',
                               u'数据项删除确认',
                               wx.YES_NO|wx.ICON_QUESTION)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_YES:
            domain = self.grid.GetTable().GetValue(self.delrow,0)
            if self.singleflag:
                self.langid = self.langid + self.datestart
            dbs = DBstorage()
            dbs.delete_data(self.langid, domain)
        else:
            return None
        
    def OnOpenLink(self,event):
        '''
        :在浏览器中打开链接
        :param event:事件值
        '''
        link = self.grid.GetTable().GetValue(self.delrow,13)
        webbrowser.open_new_tab(link)
