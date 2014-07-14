# -*- coding:utf-8 -*-
'''
Created on 2013年12月31日

@author: Hyphen.Liu
'''

import wx
import re
from globalvar import guiGlobalVar as ggv

class SysSetting(wx.Dialog):
    '''
    :系统属性设置窗口
    :功能：设置代理、线程个数、延时、阈值等信息
    '''
    def __init__(self,parent=ggv.window):
        '''
        :初始化参数
        :param parent:主界面主窗口
        '''
        wx.Dialog.__init__(self,parent=ggv.window,
                           id=-1,
                           title=u'系统设置',
                           size=(300,350))
        self.window = ggv.window
        #self.CenterOnParent()
        self.svalues = ggv.systemSetList                    #程序默认初始值
        self.CenterOnParent()
        self.createSizer()                                  #创建sizer容器
    
    def createSizer(self):
        '''
        :创建部件容器
        '''
        slist = [u'代理设置(端口):',u'最大线程个数:',u'最大延时(秒):',
                 u'阈值设定（x0.01）:',u'引擎结果页面个数:']
        
        ssSizer = wx.StaticBox(self,-1,'')
        sp = wx.Panel(self,-1)
        sty = 5
        for st in slist:                                    #布局标签
            wx.StaticText(sp,-1,st,(5,sty),(110,25),wx.ALIGN_RIGHT)
            sty += 55
        self.proxy_txt = wx.TextCtrl(sp,-1,pos=(125,5),size=(140,25))           #代理输入框
        #布局输入框和滑块
        self.thread_sl = wx.Slider(sp,-1,10,0,100,
                                   pos=(125,35),
                                   size=(140,-1),
                                   style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)   #线程数量
        self.timeout_sl = wx.Slider(sp,-1,30,0,100,
                                    pos=(125,90),
                                    size=(140,-1),
                                    style=wx.SL_AUTOTICKS|wx.SL_LABELS)         #延时设置
        self.threshold_sl = wx.Slider(sp,-1,40,0,100,
                                      pos=(125,145),
                                      size=(140,-1),
                                      style=wx.SL_AUTOTICKS|wx.SL_LABELS)       #阈值设置
        self.page_sl = wx.Slider(sp,-1,30,0,200,
                                 pos=(125,200),
                                 size=(140,-1),
                                 style=wx.SL_AUTOTICKS|wx.SL_LABELS)            #爬取搜索引擎结果页面数
        self.set_ok_bt = wx.Button(sp,-1,u'编辑',
                                   pos=(70,265),
                                   size=(70,30))            #确认和编辑按钮
        self.set_cancel_bt = wx.Button(sp,-1,u'取消',
                                       pos=(160,265),
                                       size=(70,30))        #取消按钮
        self.sliders = [self.proxy_txt,self.thread_sl,self.timeout_sl,self.threshold_sl,self.page_sl]
        #为滑块赋值
        for i,s in enumerate(self.sliders):
            if i == 0:s.SetValue(self.svalues[i])
            else:
                s.SetValue(int(self.svalues[i]))            #默认值设定
                s.SetTickFreq(5,1)                          #刻度值
            s.Enable(False)
        #为按钮绑定响应事件
        self.Bind(wx.EVT_BUTTON, self.OnEditOk, self.set_ok_bt)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.set_cancel_bt)
        #添加boxsizer
        sSizer = wx.StaticBoxSizer(ssSizer,wx.VERTICAL)
        sSizer.Add(sp,1,wx.EXPAND,0)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sSizer,1,wx.EXPAND,2)
        self.SetSizer(sizer)
        self.Layout()
    
    def checkip(self):
        '''
        :检测代理的ip和端口号是否合法
        '''
        #ipv4地址合法性检测
        reg = r'^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}$'
        pattern1 = re.compile(reg)
        pattern2 = re.compile(r'^\d{1,5}$')                 #端口号范围
        ipaddress = self.proxy_txt.GetValue()
        if ipaddress:                                       #检测ip地址的合法性
            if ipaddress.find(':') > 0:
                ipaddress = ipaddress.split(':')
                if not pattern1.search(ipaddress[0]):       #ip地址不合法
                    wx.MessageBox(u'请检查IP地址是否正确',
                                  u'代理设置',
                                  wx.OK|wx.ICON_ERROR)
                    return False
                if not pattern2.search(ipaddress[1]):       #端口号不合法
                    wx.MessageBox(u'请检查端口设置是否正确',
                                  u'代理设置',
                                  wx.OK|wx.ICON_ERROR)
                    return False
            else:
                if pattern1.search(ipaddress):              #未检测到端口号
                    wx.MessageBox(u'请添加端口号',
                                  u'代理设置',
                                  wx.OK|wx.ICON_ERROR)
                    return False
                wx.MessageBox(u'请检查IP地址是否正确',
                              u'代理设置',
                              wx.OK|wx.ICON_ERROR)
                return False
        return True
    
    def OnEditOk(self,event):
        '''
        :编辑确认功能
        :param event:
        '''
        if self.set_ok_bt.GetLabel() == u'编辑':
            for s in self.sliders:
                s.Enable(True)
            self.set_ok_bt.SetLabel(u'确定')
        else:
            if self.checkip():                              #在确认之前需要检测代理服务器的合法性
                for i,s in enumerate(self.sliders):
                    ggv.systemSetList[i] = s.GetValue()
                    s.Enable(False)
                #self.set_ok_bt.SetLabel(u'编辑')
                self.window.sysinfoUpdate()                 #更新主界面的系统属性设置信息
                self.Destroy()
    
    def OnCancel(self,event):
        '''
        :取消按钮功能
        :param event:按钮事件
        '''
        self.Destroy()
