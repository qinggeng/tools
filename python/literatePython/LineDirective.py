
#-*-coding: utf-8-*-
import functools, sys, inspect, re, traceback, pickle
#line 293, 使用noweb对python进行文学编程.nw
def revealLiterate(originFile, thisFile, chunks, stacks):
	replaced = []
	for dstPath, lineNumber, frame, source in stacks:
		if dstPath == thisFile:
			lineNumber = sourceLine(chunks, lineNumber - 71)
			dstPath = originFile
	replaced.append((dstPath.decode('utf-8'), lineNumber, frame, source))
	return replaced
def replaceStackTrace(nextHandler, thisFile, type, value, tb):
	chunks = [[202, 1], [293, 6], [217, 74], [250, 105]]
	if len(value.args) == 0:
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		resultDict["stackInfo"] = traceback.extract_tb(tb)
		value.args = value.args +(resultDict, ) 
	else:
		resultDict = value.args[-1]

	if type(resultDict) != type({}):
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		resultDict["stackInfo"] = traceback.extract_tb(tb)
		value.args = value.args +(resultDict, ) 

	if "dictId" not in resultDict or resultDict["dictId"] != u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1":
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		resultDict["stackInfo"] = traceback.extract_tb(tb)
		value.args = value.args +(resultDict, ) 

	resultDict['stackInfo'] = revealLiterate("使用noweb对python进行文学编程.nw", thisFile, chunks, resultDict["stackInfo"])
	if '<built-in function excepthook>' == str(nextHandler):
		print 'Unhandled Exception, trace back:'
		for stackInfo in resultDict['stackInfo']:
			print ur' File "' + unicode(stackInfo[0]) + ur'", line ' + unicode(stackInfo[1]) + ur' in ' + unicode(stackInfo[2])
			print ur'   ' + unicode(stackInfo[3])
		value.args = value.args[:-1]
		print re.compile(r"<type '([^']+)'>").match(str(type)).group(1)+":", value
	elif None != nextHandler:
		nextHandler(type, value, tb)

def seekInsertPos(arr, dstLine):
	if len(arr) == 0:
		return -1
	if arr[0][1] > dstLine:
		return 0
	if arr[-1][1] < dstLine:
		return len(arr)
	lb = 0
	ub = len(arr)
	while True:
		if lb >= ub:
			return lb
		mid = lb + (ub - lb)/2
		if dstLine > arr[mid][1]:
			lb = mid + 1
		elif dstLine < arr[mid][1]:
			ub = mid
		else:
			return mid

def sourceLine(arr, dstLine):
	pos = seekInsertPos(arr, dstLine)
	srcLine, inDst = arr[pos - 1]
	return srcLine + dstLine - inDst
sys.excepthook = functools.partial(replaceStackTrace, sys.excepthook, inspect.getfile(inspect.currentframe()))

#-*-coding: utf-8-*-
#line 202, 使用noweb对python进行文学编程.nw
import sys, re, pickle
codeTemplate = """
#-*-coding: utf-8-*-
import functools, sys, inspect, re, traceback, pickle
#line 293, 使用noweb对python进行文学编程.nw
def revealLiterate(originFile, thisFile, chunks, stacks):
	replaced = []
	for dstPath, lineNumber, frame, source in stacks:
		if dstPath == thisFile:
			lineNumber = sourceLine(chunks, lineNumber - %d)
			dstPath = originFile
	replaced.append((dstPath.decode('utf-8'), lineNumber, frame, source))
	return replaced
def replaceStackTrace(nextHandler, thisFile, type, value, tb):
	chunks = %s
	if len(value.args) == 0:
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		resultDict["stackInfo"] = traceback.extract_tb(tb)
		value.args = value.args +(resultDict, ) 
	else:
		resultDict = value.args[-1]

	if type(resultDict) != type({}):
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		resultDict["stackInfo"] = traceback.extract_tb(tb)
		value.args = value.args +(resultDict, ) 

	if "dictId" not in resultDict or resultDict["dictId"] != u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1":
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		resultDict["stackInfo"] = traceback.extract_tb(tb)
		value.args = value.args +(resultDict, ) 

	resultDict['stackInfo'] = revealLiterate("%s", thisFile, chunks, resultDict["stackInfo"])
	if '<built-in function excepthook>' == str(nextHandler):
		print 'Unhandled Exception, trace back:'
		for stackInfo in resultDict['stackInfo']:
			print ur' File "' + unicode(stackInfo[0]) + ur'", line ' + unicode(stackInfo[1]) + ur' in ' + unicode(stackInfo[2])
			print ur'   ' + unicode(stackInfo[3])
		value.args = value.args[:-1]
		print re.compile(r"<type '([^']+)'>").match(str(type)).group(1)+":", value
	elif None != nextHandler:
		nextHandler(type, value, tb)

def seekInsertPos(arr, dstLine):
	if len(arr) == 0:
		return -1
	if arr[0][1] > dstLine:
		return 0
	if arr[-1][1] < dstLine:
		return len(arr)
	lb = 0
	ub = len(arr)
	while True:
		if lb >= ub:
			return lb
		mid = lb + (ub - lb)/2
		if dstLine > arr[mid][1]:
			lb = mid + 1
		elif dstLine < arr[mid][1]:
			ub = mid
		else:
			return mid

def sourceLine(arr, dstLine):
	pos = seekInsertPos(arr, dstLine)
	srcLine, inDst = arr[pos - 1]
	return srcLine + dstLine - inDst
sys.excepthook = functools.partial(replaceStackTrace, sys.excepthook, inspect.getfile(inspect.currentframe()))
"""
#line 217, 使用noweb对python进行文学编程.nw
class Chunks:
	def __init__(self):
		self.chunkList = []
	def insertChunk(self, srcLine, dstLine):
		pos = self.seekInsertPos(dstLine)
		self.chunkList.insert(pos, [srcLine, dstLine])
	def seekInsertPos(self, dstLine):
		arr = self.chunkList
		if len(self.chunkList) == 0:
			return -1
		if arr[0][1] > dstLine:
			return 0
		if arr[-1][1] < dstLine:
			return len(arr)
		lb = 0
		ub = len(self.chunkList)
		while True:
			if lb >= ub:
				return lb
			mid = lb + (ub - lb)/2
			if dstLine > arr[mid][1]:
				lb = mid + 1
			elif dstLine < arr[mid][1]:
				ub = mid
			else:
				return mid
	def sourceLine(self, dstLine):
		pos = self.seekInsertPos(dstLine)
		srcLine, inDst = self.chunkList[pos - 1]
		return srcLine + dstLine - inDst
#line 250, 使用noweb对python进行文学编程.nw
def scan(srcPath):
	src = open(srcPath, 'r')
	lines = list(src)
	pattern = re.compile('^#line (\d+), (.+)')
	chunks = Chunks()
	for line, lineNum in zip(lines, range(len(lines))):
		m = pattern.match(line)
		if m != None:
			nwLine = m.group(1)
			nwName = m.group(2)
			chunks.insertChunk(int(nwLine), lineNum)
	#line 361, 使用noweb对python进行文学编程.nw
	srcString = codeTemplate % (len(codeTemplate.split('\n')), str(chunks.chunkList), nwName)
	print srcString
	for line in lines:
		print line[:-1]
if __name__ == '__main__':
	if (sys.argv) > 1:
		scan(sys.argv[1])
