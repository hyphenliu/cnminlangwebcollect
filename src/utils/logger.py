# -*- coding:utf-8 -*-
'''
Created on 2013年12月20日

@author: Hyphen.Liu
'''
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from globalvar import guiGlobalVar as ggv

PATH = ggv.LOGPATH

class Logger():
    '''
    :日志记录类只需要在程序开始运行时触发即可
    '''
    def __init__(self):
        '''
        :程序初始化
        '''
        self.prelog()
        self.logger()
        
    def prelog(self):
        '''
        :为当前搜索的语言创建以日期命名和该语言标志的log文档
        :并限制每种语言所拥有的日志文档个数
        '''
        files = os.listdir(PATH) 
        fname = PATH+time.strftime('%Y%m%d')+'-'+ggv.lang_use+'-app'
        fnum = 0
        flist = []
        for fl in files:                                    #该语言log文件的数量
            if fl.find(ggv.lang_use) > 0:
                fnum += 1
                flist.append(PATH+fl)
        if fnum > 4:                                        #如果该语言log文件数量超过5则需要删除最初生成的文件
            tfiles  = sorted(flist)
            fsuf = tfiles[0][-5]                            #新生成的文件命名沿袭被删除的文件的后缀命名
            os.remove(sorted(flist)[0])
        else:fsuf = str(len(flist)+1)
        self.logfile = fname+fsuf+'.log'
            
    def logger(self):
        '''
        :设置日志保存的格式
        '''
        logging.basicConfig(level = logging.DEBUG,\
                            format = '%(asctime)s\t%(filename)s\t[line:%(lineno)d]\t%(levelname)s\t%(message)s',\
                            datefmt = '%Y %b %d: %a %H:%M:%S',
                            filename = self.logfile,
                            filemode='w')
        #定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
#         Rthandler = RotatingFileHandler('myapp.log', maxBytes=10*1024*1024,backupCount=5)
#         Rthandler.setLevel(logging.INFO)
#         formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#         Rthandler.setFormatter(formatter)
#         logging.getLogger('').addHandler(Rthandler)
#         logging.info('test info')

if __name__ == '__main__':
    log = Logger()
    logging.debug('test debug')