#-*- coding: utf-8 -*-
import os, re
from traceback import format_exc as fme

class Shell:
	echo = False
	echoStrs = {
		'on': True,
		'off': False,
		'true': True,
		'false': False,
	}
	commands = {}
	history = []
	values = []
	def processEchoCommand(self, args):
		try:
			if len(args) == 0:
				pass
			else:
				echoStateStr = args[0].lower()
				self.echo = self.echoStrs[echoStateStr]
			print 'echo = %r' % (self.echo, )
		except Exception, e:
			self.error('invalid echo setting value %s' % (echoStateStr, ))

	def processExitCommand(self, args):
		self.msg('bye!')
		exit()

	def makeHistoryCommandArgs(self, args):
		h = self.history
		if len(args) > 0:
			arg = args[0]
			if arg.isdigit():
				return int(arg)
		return len(h)

	def processHistoryCommand(self, args):
		h = self.history
		historyLen = self.makeHistoryCommandArgs(args)
		for item, i in zip(h, reversed(range(historyLen))):
			self.msg('%d. %s' % (i + 1, item))

	def msg(self, txt):
		print txt


	def error(self, msg):
		print msg

	def installCommands(self):
		c = self.commands
		self.commands[':echo'] = self.processEchoCommand
		c[':exit'] = self.processExitCommand
		c[':history'] = self.processHistoryCommand

	def inputDeterminant(self, userInput):
		datas = userInput[1:-1]
		rows = datas.split(',')
		d = []
		for row in rows:
			row = row.strip()
			elems = row.split(' ')
			r = []
			for elem in elems:
				r.append(float(elem))
			d.append(r)
		if False == self.isValidDeterminant(d):
			return True
		self.values.append(d)
		self.msg('$%d=' % (len(self.values), ))
		self.printDeterminant(self.values[-1])
		return True

	def isValidDeterminant(self, d):
		rl = -1
		for r in d:
			if rl == -1:
				rl = len(r)
			elif len(r) != rl:
				self.msg('invalid determinant')
				return False
		return True

	def printDeterminant(self, d):
		msg = ''
		for r in d:
			msg += '|'
			for e in r:
				msg +=str(e) + '\t'
			msg += '|\n'
		self.msg(msg)

	def processOperationInput(self, userInput):
		userInput = userInput.strip()
		determinantPattern = re.compile(u'\[[^\]]+\]')
		m = determinantPattern.match(userInput)
		if m != None:
			return self.inputDeterminant(userInput)
		return False

	def runShell(self):
		self.installCommands()
		while 1:
			userInput = raw_input('>>')
			if len(userInput.strip()) == 0:
				continue
			if True == self.echo:
				self.msg(userInput)
			inputs = userInput.split(' ')
			if len(inputs) > 0:
				cmdName = inputs[0]
				if cmdName in self.commands:
					try:
						self.history.append(userInput)
						self.commands[cmdName](inputs[1:])
					except Exception, e:
						print e
						print fme()
				elif self.processOperationInput(userInput):
					pass
				else:
					self.error('unknow command/operation "%s"' % (userInput))

if __name__ == '__main__':
	s = Shell()
	s.runShell()
