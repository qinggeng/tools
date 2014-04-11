#-*- coding: utf-8 -*-
from win32file import *
import sys
from argparse import ArgumentParser
#notification = '{notification: "%s"}'% (sys.argv[1])
def notify(notification):
	f = CreateFile(r'\\.\mailslot\notificationCenter', GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
	WriteFile(f, notification)
	f.Close()

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

if __name__ == '__main__':
	argsParser = ArgumentParser(u'send notifications')
	#argsParser.add_argument(u'--content', action = 'store', dest='content', default='')
	argsParser.add_argument(u'--type', u'-t', action = 'store', dest='notificationType', required = False, choices=['message', 'warning', 'error'], default='message')
	argsParser.add_argument(u'--brief', u'-b', action = 'store', dest = 'title', required = False)
	argsParser.add_argument(u'content', action = 'store')
	args = argsParser.parse_args()
	notify(makeNotification(args))
