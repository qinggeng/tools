#-*- coding:utf-8-*-
import sys
import re
import functools
"""
2014年4月6日
明天干什么？
集成到通知中心去
"""
bodyParsers = dict()

spacePattern = re.compile(r'\s+', re.U)
scopeBeginPattern = re.compile(r'\s*\{\s*', re.U)
scopeEndPattern = re.compile(r'\s*\}\s*', re.U)
namePattern = re.compile(r'[a-zA-Z_]\w*', re.U)
colonPattern = re.compile(r'\s*:\s*', re.U)

class SymbolsIterator(object):
	def __init__(self, symbols):
		keys = set()
		for d in symbols.stack:
			keys.union(set(d.keys()))
		self.keys = list(keys)
		self.symbols = symbols
		self.index = 0
	def next():
		if index == len(self.keys):
			raise StopIetration
		return self.symbols[self.keys[index]]
		index = index + 1
	def __iter__(self):
		return self

class Symbols(object):
	def __init__(self):
		self.stack = []
		self.stack.append(dict())
	def enterScope(self):
		self.stack.append(dict())
	def leaveScope(self):
		self.stack.pop()
	def __getitem__(self, key):
		for d in reversed(self.stack):
			if key in d:
				return d[key]
		raise KeyError
	def __setitem__(self, key, value):
		self.stack[-1][key] = value
	def __iter__():
		return SymbolsIterator(self)

def token(pattern, action, symbols, string):
	matched = pattern.match(string)
	if None == matched:
		return None
	if action != None:
		action(symbols, matched.group(0))
	return matched.group(0)

def sequence(tokenStrings, action, symbols, string):
	startIndex = 0
	for tok in tokenStrings:
		matchedString = tok(symbols, string[startIndex:])
		if None == matchedString:
			return None
		startIndex = startIndex + len(matchedString)
	if action != None:
		action(symbols, string[:startIndex])
	return string[:startIndex]

def select(tokenStrings, action, symbols, string):
	matchLen = 0
	for tok in tokenStrings:
		matchedString = tok(symbols, string)
		if None == matchedString:
			continue
		matchLen = max(len(matchedString), matchLen)
	if matchLen == 0:
		return None
	if action != None:
		action(symbols, string[:matchLen])
	return string[:matchLen]

def enterScope(symbols, string):
	symbols.enterScope()

def exitScope(symbols, string):
	symbols.leaveScope()

def setScopeName(symbols, name):
	symbols['__scope_name__'] = symbols['__value__']

def setName(symbols, name):
	symbols['__value__'] = name

SCOPE_BEGIN = functools.partial(
		token,
		scopeBeginPattern,
		enterScope)
SCOPE_END = functools.partial(
		token,
		scopeEndPattern,
		exitScope)
NAME = functools.partial(
		token,
		namePattern,
		setName)
COLON = functools.partial(
		token,
		colonPattern,
		None)
SCOPE_NAME = functools.partial(
		sequence,
		[NAME, COLON],
		setScopeName)

notificationScopePattern = re.compile(r'notification', re.U)
stringPattern = re.compile(r'"([^\\|"]|\\.)*"', re.U)

def setNotificationContent(symbols, string):
	print 'notification content is:', string

SIMPLE_NOTIFICATION = functools.partial(
		token,
		stringPattern,
		setNotificationContent)

NOTIFICATION = functools.partial(
		select,
		[SIMPLE_NOTIFICATION],
		None)

bodyParsers['notification'] = NOTIFICATION

def parseBody(bodyParsers, symbols, string):
	parserName = symbols['__scope_name__']
	if parserName not in bodyParsers:
		return None
	parser = bodyParsers[parserName]
	return parser(symbols, string)


SCOPE_BODY = functools.partial(
		parseBody,
		bodyParsers)

SCOPE = functools.partial(
		sequence,
		[SCOPE_BEGIN, SCOPE_NAME, SCOPE_BODY, SCOPE_END],
		None)

def parse(string):
	symbols = Symbols()
	SCOPE(symbols, string)

if __name__ == '__main__':
	p = re.compile('[a-z]+')
	m = p.match('acs111')
	print dir(m)
	print m.group(0)
	parse('{   notification :   "hello world!" }')
