#-*- coding: utf-8 -*-
from scopeParsers import *

notificationScopePattern = re.compile(r'notification', re.U)

def trySetKey(dest, src, key):
	if key in src:
		dest[key] = src[key]

def setNotificationContent(symbols, string):
	print 'notification content is:', string

def makeNotification(symbols, string):
	symbols.setResult(symbols['notification'])

def setNotificationProperty(propName, symbols, string):
	symbols['notification'][propName] = string[1:-1]

SIMPLE_NOTIFICATION = functools.partial(
		token,
		stringPattern,
		setNotificationContent)

NOTIFICATION_CONTENT = functools.partial(
		token,
		stringPattern,
		functools.partial(setNotificationProperty, "content"))

NOTIFICATION_TITLE = functools.partial(
		token,
		stringPattern,
		functools.partial(setNotificationProperty, "title"))

NOTIFICATION_SOURCE = functools.partial(
		token,
		stringPattern,
		functools.partial(setNotificationProperty, "source"))

NOTIFICATION_BACKGROUND = functools.partial(
		token,
		stringPattern,
		functools.partial(setNotificationProperty, "background"))

bodyParsers['content'] = NOTIFICATION_CONTENT
bodyParsers['title'] = NOTIFICATION_TITLE
bodyParsers['source'] = NOTIFICATION_SOURCE
bodyParsers['background'] = NOTIFICATION_BACKGROUND

NOTIFICATION_PROPERTY = SCOPE
dummy = [NOTIFICATION_PROPERTY, COMMA, None]
NOTIFICATION_PROPERTIES = functools.partial(
		select,
		[NOTIFICATION_PROPERTY, 
		functools.partial(
			sequence,
			dummy,
			None)],
		None)
dummy[-1] = NOTIFICATION_PROPERTIES
dummy = None

def setVariableAndContinue(setSymbol, continuation, symbols, string):
	setSymbol(symbols)
	continuation(symbols, string)

def setNotification(symbols):
	symbols['notification'] = dict()

COMPLEX_NOTIFICATION = functools.partial(
		sequence,
		[NOTIFICATION_PROPERTIES],
		makeNotification)

COMPLEX_NOTIFICATION = functools.partial(
		setVariableAndContinue,
		setNotification,
		COMPLEX_NOTIFICATION)

NOTIFICATION = functools.partial(
		select,
		[SIMPLE_NOTIFICATION, COMPLEX_NOTIFICATION],
		None)

bodyParsers['notification'] = NOTIFICATION
def parseNotification(notification):
	return parse(notification)

if __name__ == '__main__':
	print parseNotification('{   notification :   {content: "hello world!"},{source: "a source"},{title: "a title"}}')
