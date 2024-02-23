#!/usr/bin/env python3

import os
import platform
import json
import Buffer
import sys

__commands__ = [
    ['-h' , '--help'],
    ['-ap', '--add-path'],
    '--isfile', '--isdir',
    '--exists', '--remove-dir'
]

class Razer(object):
    def __init__(self, path: str = None):
        self.path = path
        self.session = os.path
    
    def isExists(self):
        if not self.path == None:
            if type(self.path) == str:
                if self.session.exists(self.path):
                    return {"path" : self.path, "exists" : True}
                else:
                    return {"path" : self.path, "exists" : False}
            else:raise ValueError(f"The Path Should be String not a '{type(self.path)}'")
        else:raise ValueError("Path cannot be Empty in Razer class")
        
    def isFile(self):
        if Razer(self.path).isExists()['exists'] == True:
            if self.session.isfile(self.path):
                return {"path" : self.path, "isfile" : True, "error" : False}
            else:return {"path" : self.path, "isfile" : False, "error" : True}
        else:return {"path" : self.path, "error" : True, "result" : Razer(self.path).isExists()}
    
    def isDir(self):
        if Razer(self.path).isExists()['exists'] == True:
            if self.session.isdir(self.path):
                return {"path" : self.path, "isdir" : True, "error" : False}
            else:return {"path" : self.path, "isdir" : False, "error" : True}
        else:return {"path" : self.path, "error" : True, "result" : Razer(self.path).isExists()}

    def scan(self):
        razer = Razer(self.path)
        if razer.isExists()['exists'] == True:
            isf = razer.isFile()['isfile']
            isd = razer.isDir()['isdir']
            ise = True
            return {"path" : self.path, "exists" : ise, "isfile" : isf, "isdir" : isd}
        else:return {"path" : self.path, "exists" : False}


addPath = Buffer.BufferConsole().addFlag("-ap", "--add-path")
isFilex = Buffer.BufferConsole().addFlag("--isfile")
isDirFile = Buffer.BufferConsole().addFlag("--isdir")
isExistsFile = Buffer.BufferConsole().addFlag("--exists")
rd = Buffer.BufferConsole().addFlag("--remove-dir")

if len(addPath) == 1 and addPath[0] != "Null":
    adp = addPath[0]
    result = Razer(adp).scan()
    if result['exists']:
        newPath = r"{}".format(result['path'])
        paths = os.getenv("PATH")
        if result['isfile']:
            try:
                newPathString = f"{paths}:{newPath}"
                os.environ['PATH'] = newPathString
                print(f"File Added To Path\nFile Path: {result['path']}\nNew Path String: {newPathString}")
            except Exception as ERROR_FILE:
                print(f"Cannot Add File To Path: {ERROR_FILE}\nFile Path: {result['path']}")
        elif result['isdir']:
            try:
                newPathString = f"{paths}:{newPath}"
                os.environ['PATH'] = newPathString
                print(f"Dir Added To Path\nDir Path: {result['path']}\nNew Path String: {newPathString}")
            except Exception as ERROR_FILE:
                print(f"Cannot Add File To Path: {ERROR_FILE}\nDir Path: {result['path']}")

if len(addPath) == 1 and addPath[0] == "Null":
    print("The Argument (-ad / --add-path) cannot be empty")

if len(isFilex) == 1 and isFilex[0] != "Null":
    print(json.dumps(Razer(isFilex[0]).isFile(), indent=4))

if len(isFilex) == 1 and isFilex[0] == "Null":
    print("The Argument (--isfile) cannot be empty")

if len(isDirFile) == 1 and isDirFile[0] != "Null":
    print(json.dumps(Razer(isDirFile[0]).isDir(), indent=4))

if len(isDirFile) == 1 and isDirFile[0] == "Null":
    print("The Argument (--isdir) cannot be empty")

if len(isExistsFile) == 1 and isExistsFile[0] != "Null":
    print(json.dumps(Razer(isExistsFile[0]).scan(), indent=4))

if len(isExistsFile) == 1 and isExistsFile[0] == "Null":
    print("The Argument (--exists) cannot be empty")

if len(rd) == 1 and rd[0] != "Null":
    if platform.system() == "Windows":
        if Razer(rd[0]).isExists()['exists'] == True:
            if Razer(rd[0]).isDir()['isdir'] == True:
                os.rmdir(rd[0])
                print(json.dumps({"path" : rd[0], "removed" : True}, indent=4))
            else:print(json.dumps({"path" : rd[0], "removed" : False, "error" : f"The Path '{rd[0]}' Does Not a Directory"}, indent=4))
        else:print(json.dumps({"path" : rd[0], "removed" : False, "error" : f"The Path '{rd[0]}' Does Not Exists"}, indent=4))

if len(rd) == 1 and rd[0] == "Null":
    print("The Argument (--remove-dir) cannot be empty")

if "-h" in sys.argv or "--help" in sys.argv:
    print(json.dumps(__commands__, indent=4))
