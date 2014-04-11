#-*- coding: utf-8 -*-
import wx
import re
import sendNotification
from collections import namedtuple
import utils
kTimerID = 400
secondsPattern = re.compile(ur'\s*\d+\s*')
class AlarmSetter(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, parent = None, title = u'定时通知配置')
		self.SetSize((240, 640))
		sz = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sz)
		te = wx.TextCtrl(self)
		sz.Add(te, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		sz.Add((10, 2))
		self.messageInputBox = te
		te = wx.TextCtrl(self)
		sz.Add(te, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		sz.Add((10, 4))
		self.timeInputBox = te
		btn = wx.Button(self, label = u"go")
		sz.Add(btn, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		btn.Bind(wx.EVT_BUTTON, self.onGoBtn)
		self.btn = btn
		self.timer = wx.Timer(self, kTimerID);
		self.Bind(wx.EVT_TIMER, self.onTimer)
		self.messageInputBox.SetValue('hello')
		self.timeInputBox.SetValue('1')
	def onGoBtn(self, ev):
		msg = self.messageInputBox.GetValue()
		countDown = self.timeInputBox.GetValue()
		if len(msg) == 0:
			return
		if None == secondsPattern.match(countDown):
			return
		seconds = int(countDown)
		print seconds
		self.messageInputBox.Disable()
		self.timeInputBox.Disable()
		self.btn.Disable()
		self.timer.Start(1 * 1000, oneShot = False)
	def onTimer(self, ev):
		print 'timer'
		if self.timeInputBox.GetValue() == u'0':
			NotifyArgs = namedtuple('NotifyArgs', [u'content', u'title', u'notificationType']);
			utils.runCmd(u'sendNotification.py "%s"' % self.messageInputBox.GetValue())
			self.timer.Stop()
			self.messageInputBox.Enable()
			self.timeInputBox.Enable()
			self.btn.Enable()
			self.timeInputBox.SetValue('1')
		else:
			seconds = int(self.timeInputBox.GetValue())
			seconds = max(0, seconds - 1)
			self.timeInputBox.SetValue(str(seconds))
if __name__ == '__main__':
	app = wx.App(redirect = False)
	a = AlarmSetter()
	a.Show()
	app.MainLoop()

