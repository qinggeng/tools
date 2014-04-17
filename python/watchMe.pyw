#-*- coding: utf-8 -*-
import wx
import re
import sendNotification
from collections import namedtuple
import utils
from wx.lib.masked.timectrl import TimeCtrl
kTimerID = 400
secondsPattern = re.compile(ur'\s*\d+\s*')

def loadBitmapFromPNGFile(path, bitmapSize):
	img = wx.Image(path)
	img.LoadFile(path, wx.BITMAP_TYPE_PNG)
	img = img.Scale(bitmapSize[0], bitmapSize[1])
	return wx.BitmapFromImage(img)

class AlarmPanel(wx.Panel):
	def __init__(self, parent):
		kMarginTop = kMarginBottom = 4
		kMarginLeft = kMarginRight = 4
		kIconWidth = kIconHeight = 24
		wx.Panel.__init__(self, parent)
		verticalMargin = wx.BoxSizer(wx.VERTICAL)
		horizontalMargin = wx.BoxSizer(wx.HORIZONTAL)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		verticalMargin.Add((0, kMarginTop))
		verticalMargin.Add(horizontalMargin, proportion = 1, flag = wx.EXPAND)
		verticalMargin.Add((0, kMarginBottom))
		horizontalMargin.Add((kMarginLeft, 0))
		horizontalMargin.Add(mainSizer, proportion = 1, flag = wx.EXPAND)
		horizontalMargin.Add((kMarginRight, 0))
		self.SetSizer(verticalMargin)
		briefText = wx.StaticText(self, label = u'this is a brief text', style = wx.ALIGN_BOTTOM)
		briefText.SetBackgroundColour('#FFFFFF')
		#briefText.SetLabel(u'this is a brief text')
		sz = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(sz, proportion = 1, flag = wx.EXPAND | wx.ALL)
		sz.Add((0, 6))
		sz.Add(briefText, proportion = 0, flag =  wx.ALIGN_CENTER_VERTICAL)
		mainSizer.Add((0, 10), proportion = 1, flag = wx.EXPAND)
		#TODO count down control
		countDownCtrl = TimeCtrl(self, fmt24hr = True, style = wx.TE_PROCESS_TAB | wx.NO_BORDER)
		countDownCtrl.SetBackgroundColour('#FFFFFF')
		self.SetBackgroundColour('#FFFFFF')
		sz = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(sz, proportion = 1)
		sz.Add((0, 6))
		sz.Add(countDownCtrl)
		mainSizer.Add((10, 0))
		playButton = wx.BitmapButton(self, style = 0)
		playButton.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.control.play.png', (kIconWidth, kIconHeight)))
		playButton.SetBitmapHover(loadBitmapFromPNGFile(u'appbar.control.play_dark.png', (kIconWidth, kIconHeight)))
		playButton.SetSize((kIconWidth, kIconHeight))
		playButton.SetBackgroundColour('#FFFFFF')
		playButton.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOverBtn)
		playButton.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeaveBtn)
		mainSizer.Add(playButton, proportion = 0)
		self.countDownCtrl = countDownCtrl
		self.playButton = playButton
		self.play = None

	def onMouseOverBtn(self, ev):
		btn = ev.GetEventObject()
		btn.SetBackgroundColour("#000000")
	def onMouseLeaveBtn(self, ev):
		btn = ev.GetEventObject()
		btn.SetBackgroundColour("#FFFFFF")

	def onPlayButton(self, ev):
		self.countDownCtrl.SetEditable(False)
		self.playButton.Hide()
		if self.play == None:
			return
		self.play()
	
	def stop(self):
		self.countDownCtrl.SetEditable(True)
		self.playButton.Show()

	def setCountDownStart(self, t):
		self.countDownCtrl.SetValue(t)
	
	def countDown(self):
		t = self.countDownCtrl.GetValue(as_wxTimeSpan = True)
		t -= wx.TimeSpan(0, 0, 1)
		self.countDownCtrl.SetValue(t)
		return str(t)

class AlarmSetter(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, parent = None, title = u'定时通知配置')
		self.SetWindowStyle(wx.TAB_TRAVERSAL | self.GetWindowStyle())
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
		self.messageInputBox.SetValue(u'测试')
		self.timeInputBox.SetValue('1')
		stub = AlarmPanel(self)
		sz.Add(stub, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		self.alarmPanel = stub

	def onGoBtn(self, ev):
		msg = self.messageInputBox.GetValue()
		countDown = self.timeInputBox.GetValue()
		if len(msg) == 0:
			return
		if None == secondsPattern.match(countDown):
			return
		seconds = int(countDown)
		self.alarmPanel.setCountDownStart(wx.TimeSpan.Seconds(seconds))
		self.alarmPanel.onPlayButton(None)
		self.messageInputBox.Disable()
		self.timeInputBox.Disable()
		self.btn.Disable()
		self.timer.Start(1 * 1000, oneShot = False)
	def onTimer(self, ev):
		if self.timeInputBox.GetValue() == u'0':
			NotifyArgs = namedtuple('NotifyArgs', [u'content', u'title', u'notificationType']);
			utils.runCmd(u'sendNotification.py "{0}"'.format(self.messageInputBox.GetValue()))
			self.timer.Stop()
			self.messageInputBox.Enable()
			self.timeInputBox.Enable()
			self.btn.Enable()
			self.timeInputBox.SetValue('300')
			self.SetLabel(u'定时通知配置')
			self.alarmPanel.stop()
		else:
			seconds = int(self.timeInputBox.GetValue())
			seconds = max(0, seconds - 1)
			self.timeInputBox.SetValue(str(seconds))
			label = u'定时通知配置: ' + self.alarmPanel.countDown()
			self.SetLabel(label)
			
if __name__ == '__main__':
	#app = wx.App(redirect = False)
	app = wx.App()
	a = AlarmSetter()
	a.Show()
	app.MainLoop()

