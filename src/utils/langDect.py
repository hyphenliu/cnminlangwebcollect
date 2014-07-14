# -*- coding:utf-8 -*-
'''
Created on 2013年11月16日

@author: Hyphen.Liu
'''
import logging

import globalvar.utilGlobalVar as ugv
import globalvar.guiGlobalVar as ggv

CODE = 'utf8'

class LangDect():
    '''
    :语言检测主程式
    '''
    def langDect(self,lang,text,coding='unicode'):
        '''
        :对传入的文本进行语言的检测
        :param lang:给定待检测语言
        :param text:给定文本
        :param coding:文本编码方式
        '''
        if ggv.pterminate:return None
        self.lang = 'unknown'                               #默认为未知语言
        self.charStr = ''                                   #对于同种语言不同编码的文字进行的一个暂存容器
        self.langN = 0                                      #待检测语言字符集的个数
        self.langRe = 0                                     #共有字符集个数，有的语言同属一个大类，如，维哈柯同属阿拉伯语系，共用一些阿拉伯文字
        self.langOt = 1                                     #不属于这个字符集的其它字符
        if lang not in ggv.langIds:                         #检测的语言超出了本系统的能力范围
            return {self.lang:'The language not in this system\'s language list'}
        self.txtOri = text.decode(CODE)
        self.txt = set(self.txtOri)                         #对字符去重
        self.coding = coding
        
        if lang == 'bo':    self.boDect()                   #藏文识别
        elif lang == 'ug' or lang == 'kk' or lang == 'ky':     self.ukyDect()                       #维吾尔文、哈萨克文、柯尔克孜文识别
        elif lang == 'mn':  self.mnDect()                   #蒙古文识别
        elif lang == 'kit' or lang == 'ko' or lang == 'ii' or lang == 'tl':    self.kitDect(lang)   #朝鲜文、彝文、傣文识别
        else: self.zaDect()                                 #壮文
        language = self.returnlang()
        return language, self.coding
    
    def returnlang(self):
        '''
        :计算语言的识别的可信度并返回相应数据
        '''
        language = {}
        rst = 1.0*(self.langN + self.langRe) / (self.langN + self.langRe + self.langOt)             #计算有效字符所占比例
        language[self.lang] = rst
        return language
            
    def puncDect(self,char):
        '''
        :识别字符是否为标点符号
        :param char:输入的字符
        '''
        for punct in ugv.puctuation:
            if char <= punct[1] and char >= punct[0]:
                return True
        return False

    def mnDect(self):
        '''
        :蒙古文的识别
        '''
        uniN = 0                                            #Unicode字符数量
        gbkN = 0                                            #其他编码的字符数量，包括蒙科力、赛因等编码
        for char in self.txt:
            if self.puncDect(char):                         #标点符号识别
                continue
            if char >= ugv.mnCode[0][0] and char <= ugv.mnCode[0][1]:
                uniN += 1
            if char >= ugv.mnCode[1][0] and char <= ugv.mnCode[1][1]: 
                gbkN += 1
            self.charStr += char
        if uniN > gbkN:
            self.coding = 'utf-8'
            mncode = ugv.mnCode[0]
        elif uniN < gbkN:
            self.coding = 'gbk'
            mncode = ugv.mnCode[1]
        else:
            return self.lang
        for char in self.charStr:
            if char >= mncode[0] and char <= mncode[1]:
                self.langN += self.txtOri.count(char)
            else:
                self.langOt += self.txtOri.count(char)
        if self.langN:
            self.lang = 'mn'
    
    def boDect(self):
        '''
        :藏文识别
        '''
        count = 0
        for char in self.txt:
            if self.puncDect(char):
                continue
            self.charStr += char
            if char == u'\uFE3D' or char == u'\uFE40':      #同元编码范围
                count += self.txtOri.count(char)
                continue
            if (char >= ugv.boCode[0][0] and char <= ugv.boCode[0][1]) or \
                (char >= ugv.boCode[1][0] and char <= ugv.boCode[1][1]):
                self.langN += self.txtOri.count(char)
            else:
                self.langOt += self.txtOri.count(char)
        freq = 1.0 * count / (count + self.langOt)
        #if freq > 0.25:
        if freq > 0.125:                                    #网页语言共存情况，使得频率下降，本数据根据相关文献得到并做了相应处理
            self.langN = 0
            self.langOt = 0
            langN1 = 0
            langN2 = 0
            for char in self.charStr:
                if char in ugv.boCode[2]:
                    langN1 += self.txtOri.count(char)
                if char in ugv.boCode[3]:
                    langN2 += self.txtOri.count(char)
                else:
#                     print char
                    self.langOt += self.txtOri.count(char)
            if langN1 > langN2:
                self.coding = 'tonguer'
                self.langN = langN1
            else:
                self.coding = 'bzd'
                self.langN = langN2
        if self.langN:
            self.lang = 'bo'
    
    def ukyDect(self):
        '''
        :维吾尔文哈萨克文柯尔克孜文的识别
        :因为属于同一语系故同时处理
        '''
        ugN = 0                                         #维吾尔文字符数量
        kyN = 0                                         #柯尔克孜字符数量
        kkN = 0                                         #哈萨克文字符数量
        arN = 0                                         #阿拉伯字符数量
        for char in self.txt:
            if self.puncDect(char):
                continue
            if char in ugv.arCode:
                arN += 1
            if char in ugv.ugCode:
                ugN += 1
            if char in ugv.kyCode:
                kyN += 1
            if char in ugv.kkCode:
                kkN += 1
            self.charStr += char
        if arN > 3:                                     #根据统计数据进行的匹配顺序，不可以打乱顺序
            self.lang = 'ar'
            ukyCode = ugv.arCode
        elif ugN > kyN and ugN >kkN:
            self.lang = 'ug'
            ukyCode = ugv.ugCode
        elif kyN > ugN and kyN >kkN:
            self.lang = 'ky'
            ukyCode = ugv.kyCode
        elif kkN:
            self.lang = 'kk'
            ukyCode = ugv.kkCode
        else:
            return self.lang
        for char in self.charStr:
            if self.lang == 'ar':
                if char >= u'\u0600' and char <= u'\u06FF':
                    self.langN += self.txtOri.count(char)
            elif char in ukyCode:
                self.langN += self.txtOri.count(char)
            elif char in ugv.totalCode:
                self.langRe += self.txtOri.count(char)
            else:
                self.langOt += self.txtOri.count(char)
    
    def kitDect(self,lang):
        '''
        :朝鲜文彝文傣文的识别
        :因为这几种语言编码集单一为减少代码量故放在一起
        :param lang:待识别的语言
        '''
        flag = 0                                            #朝鲜文有两个编码范围，需要做区分
        if lang == 'ko':
            flag = 1
            kitCode = ugv.koCode
        elif lang == 'ii':
            kitCode = ugv.iiCode
        elif lang == 'tl':
            kitCode = ugv.tlCode
        else:
            return self.lang
        for char in self.txt:
            if self.puncDect(char):
                continue
            if flag and (char >= ugv.koCode[0][0] and char <= ugv.koCode[0][1]) or \
                (char >= ugv.koCode[1][0] and char <= ugv.koCode[1][1]):
                self.langN += self.txtOri.count(char)
            elif char >= kitCode[0] and char <= kitCode[1]:
                self.langN += self.txtOri.count(char)
            else:
                self.langOt += self.txtOri.count(char)
        if self.langN:
            self.lang = lang
    
    def zaDect(self):
        '''
        :壮文的识别
        '''
        pass

if __name__ == '__main__':
    ld = LangDect()
    