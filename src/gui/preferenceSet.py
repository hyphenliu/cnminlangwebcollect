# -*- coding:utf-8 -*-
'''
Created on 2014年1月10日

@author: Hyphen.Liu
'''

import wx

import globalvar.guiGlobalVar as ggv

class PreferenceSet(wx.Dialog):
    def __init__(self,parent = ggv.window):
        wx.Dialog.__init__(self,parent=ggv.window,title=u'')
        

if __name__ == '__main__':
    ps = PreferenceSet()