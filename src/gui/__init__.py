# -*- coding:utf-8 -*-
import os
import ConfigParser
from globalvar import utilGlobalVar as ugv
from globalvar import guiGlobalVar as ggv

class GuiInit():
    def __init__(self):
        self.uDirList = ugv.mtrPath
        self.mkDir()
    
    def mkDir(self):
        if not os.path.isdir(self.uDirList):
            os.mkdir(self.uDirList)
    
    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.read('guiconfig.ini')

if __name__ == '__main__':
    GuiInit()