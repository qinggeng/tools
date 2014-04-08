#-*- coding: utf-8 -*-
from win32file import *
import sys
from argparse import ArgumentParser
argsParser = ArgumentParser(u'send notifications')
#argsParser.add_argument(u'--content', action = 'store', dest='content', default='')
argsParser.add_argument(u'--type', u'-t', action = 'store', dest='notificationType', required = False, choices=['message', 'warning', 'error'], default='message')
argsParser.add_argument(u'--brief', u'-b', action = 'store', dest = 'title', required = False)
argsParser.add_argument(u'content', action = 'store')
args = argsParser.parse_args()
print args
def makeNotification(args):
	backgroundColors = dict()
	backgroundColors['warning'] = '#FFFF00'
	backgroundColors['error'] = '#FF4040'
	backgroundColors['message'] = '#FFFFFF'
	notificationStr = '{notification: {content: "%s"}' %(args.content);
	if None != args.title:
		notificationStr += ', {title: "%s"}' % (args.title)
	notificationStr += ', {background: "%s"}' % (backgroundColors[args.notificationType])
	notificationStr +='}'
	return notificationStr
	
notification = makeNotification(args)
#notification = '{notification: "%s"}'% (sys.argv[1])
f = CreateFile(r'\\.\mailslot\notificationCenter', GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
WriteFile(f, notification)
f.Close()
