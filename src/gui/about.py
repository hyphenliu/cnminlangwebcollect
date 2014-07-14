# -*- coding:utf-8 -*-
'''
Created on 2013年12月31日

@author: Hyphen.Liu
'''
import wx
import wx.html

import globalvar.guiGlobalVar as ggv

class About(wx.Dialog):
    '''
    :关于本软件的功能等信息界面
    '''
    text = ggv.aboutText
    def __init__(self, parent):
        '''
        :创建窗口并显示软件功能相关信息
        :param parent:主界面窗口
        '''
        wx.Dialog.__init__(self, parent, -1, '关于本软件',
                          size=(330, 290) )

        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, u"确认")

        sizer = wx.BoxSizer(wx.VERTICAL)                    #使用容器包含部件
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 0)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(sizer)                                #添加容器到窗口
        self.Layout()