#-*- coding: utf-8 -*-
from win32file import *
import sys
if len(sys.argv) != 2:
	print "useage: %s notification" % (sys.argv[0])
notification = sys.argv[1]
f = CreateFile(r'\\.\mailslot\notificationCenter', GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
WriteFile(f, notification)
f.Close()
