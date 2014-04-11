#-*- coding:utf-8 -*-
import datetime
import time
import subprocess as sp
def nowStr():
	return datetime.datetime.now().strftime("%Y年%m月%d日%H点%M分%S秒").decode('utf-8')
def runCmd(cmd, echo = False, staging = False):
	if True == echo:
		print cmd
	if True == staging:
		return (True, "", "")
	pipe = sp.Popen(cmd, shell=True, stdin=sp.PIPE, stderr=sp.PIPE, stdout = sp.PIPE)
	stdout, stderr = pipe.communicate()
	ret = pipe.returncode
	return (ret == 0, stdout, stderr)

def isFileUpdated(path):
	st = os.stat(path)
	return st.st_atime <= st.st_mtime
