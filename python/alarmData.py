#-*- coding: utf-8 -*-
import pickle
import functools
from collections import namedtuple
class Alarm():
	def __init__(self):
		self.alarmTime = None
		self.brief = u""
		self.content = u""
		self.countDown = 0
		self.alarmType = u"alarm"
def newAlarm(dateTime, brief, content):
	a = Alarm()
	a.alarmTime = time
	a.brief = brief
	a.content = content
	return a

def newCountDown(countDownTime, brief, content):
	a = Alarm()
	a.countDown = countDownTime
	a.brief = brief
	a.content = content
	a.alarmType = u"countDown"
	return a
