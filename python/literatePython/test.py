#-*-coding: utf-8-*-
#line 204, 使用noweb对python进行文学编程.nw
import sys, re
#line 213, 使用noweb对python进行文学编程.nw
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
	def sorceLine(self, dstLine):
		pos = self.seekInsertPos(dstLine)
		srcLine, inDst = self.chunkList[pos - 1]
		return srcLine + dstLine - inDst
			
def sourceLine(srcRef, lineNum):
		chunk = srcRef.nearestChunk(lineNUm)
		return chunk.srcLine + lineNum - chunk.lineNum
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
	print chunks.chunkList
	
#line 330, 使用noweb对python进行文学编程.nw
srcString = """
#line 294, 使用noweb对python进行文学编程.nw
def revealLiterate(originFile, thisFile, chunks, stacks):
	replaced = []
	for dstPath, lineNumber, frame, source in stacks:
		if dstPath == thisFile:
			lineNumber = chunks.sourceLine(lineNumber)
			dstPath = originFile
		replaced.append((dstPath, lineNUmber, frame, source))
	return replaced
def replaceStackTrace(nextHandler, thisFile, type, value, tb):
	chunks = %s
	if len(values.args) == 0:
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		retulstDict["stackInfo"] = stacktrace.extract_tb(tb)
		value.args = value.args +(resultDict, ) 
	else:
		resultDict = value.args[-1]

	if type(resultDict) != type({}):
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		retulstDict["stackInfo"] = stacktrace.extract_tb(tb)
		value.args = value.args +(resultDict, ) 

	if "dictId" not in resultDict or resultDict["dictId"] != u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1":
		resultDict = {}
		resultDict["dictId"] = u"9D6B6AA1-92FC-453E-8B9A-91D0E02A17B1"
		retulstDict["stackInfo"] = stacktrace.extract_tb(tb)
		value.args = value.args +(resultDict, ) 

	revealLiterate(%s, thisFile, chunks, resultDict["stackInfo"])
	if None != nextHandler:
		nextHandler(type, value, traceback)
#line 332, 使用noweb对python进行文学编程.nw
sys.execepthook = functools.partial(sys.execepthook, inspect.getfile(inspect.currentframe()))
""" % (str(chunks.chunkList), nwname)
print scriptString
#line 207, 使用noweb对python进行文学编程.nw
if __name__ == '__main__':
	if (sys.argv) > 1:
		scan(sys.argv[1])
