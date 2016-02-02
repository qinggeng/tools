#-*- coding: utf-8 -*-
import os
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
				else:
					self.error('unknow command/operation "%s"' % (userInput))

if __name__ == '__main__':
	s = Shell()
	s.runShell()
