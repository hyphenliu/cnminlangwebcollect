# -*- coding:utf-8 -*-
'''
Created on 2014年1月10日

@author: Hyphen.Liu
'''
import globalvar.guiGlobalVar as ggv
import globalvar.crawlerGlobalVar as cgv
import globalvar.utilGlobalVar as ugv

class InitialVar():
    '''
    :为系统变量赋值
    '''
    def __init__(self):
        '''
        :主窗口赋值给全局变量
        '''
        self.window = ggv.window
        self.initialVar()
        
    def engineChoice(self,lang):
        '''
        :根据不同的语言选择不同的搜索引擎
        :因为不同的搜索引擎只能搜索特定的几个语言文字
        :param lang:待搜索的语言
        '''
        if lang in ggv.gbs:
            englist = [cgv.google_engine,cgv.bing_engine,cgv.so_engine]
        elif lang == 'za':                                  #壮文属于拉丁文，故可以使用所有的搜索引擎搜索到
            englist = cgv.engines
        elif lang == 'ii':                                  #彝文只能通过谷歌引擎和美国雅虎搜到
            englist = [cgv.google_engine]
        elif lang == 'tl':
            englist = [cgv.google_engine,cgv.so_engine]
        return englist
        
    def initialVar(self):
        '''
        :为后续程序与语言相关的变量赋值
        :如，搜索引擎列表的排列，关键字的填补等
        '''
        ggv.lang_use = ggv.langIds[ggv.langs.index(ggv.personSetList[0])]
        if ggv.lang_use == 'mn':                            #蒙古文需要将检测到的iso-8859-2的编码使用gb18030解码
            cgv.CHARSET.append('iso-8859-2')
        elif ggv.lang_use in ['ug','kk','ky']:
            pass
        ggv.keyword_use = ggv.keywordslist[ggv.lang_use]
        if not ggv.personSetList[1] == u'所有':               #搜索引擎全选情况另外考虑
            ggv.engine_use[0] = cgv.engines[ggv.engines.index(ggv.personSetList[1])]
        elif ggv.personSetList[1] == u'所有':
            ggv.engine_use = self.engineChoice(ggv.lang_use)
        ggv.URLTEMPF = ugv.DATAPATH+ggv.lang_use+ugv.URLTEMPF
        ggv.ENGTEMPF = ugv.DATAPATH+ggv.lang_use+ugv.ENGURLTEMPF
        ggv.OUTTEMPF = ugv.DATAPATH+ggv.lang_use+ugv.OUTURLTEMPF
                