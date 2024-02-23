#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dev: Host1let
"""
BufferArgv Library
~~~~~~

Controll Your Data in Terminal 
```
from Buffer.BufferArgv import BufferConsole
```
"""

import sys
import threading

actions = []
commands: dict = {}

class BufferAttribute(object):
    def __init__(self, dic):
        self.dic = dic
        for key in dic.keys():
            setattr(self, key, dic[key])

class BufferForm(BufferAttribute):
    def __init__(self, dic):
        super().__init__(dic)
        
class BufferList(object):
    def __init__(self,
                 List: list = [],
                 ):
        
        self.list = List
        
    def parse(self):
        bfd = {}

        for i in range(len(self.list)):
            bfd["_"+str(i+1)] = self.list[i]

        return bfd

    def isexists(self, target):
        if target in self.list:
            return True
        else:return False

    def isinfrontof(self, target, indexes):
        isit = False

        if target in self.list:
            try:
                indx = self.list.index(target)
                if indx == indexes:
                    isit = True
                else:isit = False
            except Exception as e:return e
        
        return isit
    
    def indexexists(self, target):
        if target in self.list:
            return self.list.index(target)
        else:return False

class BufferConsole(object):
    def __init__(self,
                 __help: str = "",
                 __discription: str = ""
                 ):
    
        self.forHelp = __help
        self.dis = __discription
        self.status_help = True
        self.status_dis = True
        self.pyVersion = "3"
        self.data = []
    
    def __setcommands__(self, __key, __value):
        commands[__key] = __value
        return commands
        
    def activeHelp(self):
        self.status_help = True
        
    def deactiveHelp(self):
        self.status_help = False
        
    def activeDis(self):
        self.status_dis = True
    
    def deactiveDis(self):
        self.status_dis = False
        
    def getArgv(self):
        return sys.argv
    
    def getOriginalArgv(self):
        return sys.orig_argv
    
    def getDictArgv(self):
        return BufferList(sys.argv).parse()

    def setExt(self) -> str:
        if self.status_help == True:
            if not self.status_dis == True:
                if len(self.getArgv()) <= 1 or "-h" in self.getArgv() or "--help" in self.getArgv():
                    sshx = "Usage: python{} {} => Options:\n".format(self.pyVersion, self.getArgv()[0])
                    sshx += "\n".join([f"{str(k)}: {str(v)}" for k, v in commands.items()])
                    return sshx
            else:return ""
    
    def addFlag(self, *flags, mode: str = "in_front_of"):
        flg = list(flags)
        for i in range(len(flg)):
            self.__setcommands__(str(i+1), flg[i])

        if mode == "in_front_of":
            for key, val in BufferConsole().getDictArgv().items():
                if str(val) in flg:
                    keyx = int(str(key).replace("_", ""))
                    keyx += 1
                    if not f"_{keyx}" in BufferConsole().getDictArgv().keys():
                        self.data.append("Null")
                        pass
                    else:
                        self.data.append(BufferConsole().getDictArgv()[f"_{keyx}"])
                        pass
                
                else:
                    pass

            return self.data
        
    def addListener(self, flag, function_, getData: bool = False):
        if getData == False:
            if flag in self.getArgv():
                function_()
                
        else:
            lis = self.addFlag(flag)
            arg = self.getArgv()
            if flag in arg:
                flgIndex = arg.index(flag)
                data = lis[flgIndex]
                thread = threading.Thread(target=function_, args=(data,))
                thread.start()
                thread.join()

