#-*- coding: utf-8 -*-
import sys, os.path
thePath = sys.argv[1]
def listFile(args, dirName, fileNames):
    for fileName in fileNames:
        filePath = os.path.join(dirName, fileName)
        if os.path.isfile(filePath):
            print filePath
os.path.walk(thePath, listFile, None)
