#-*- coding: utf-8 -*-
import wx
from wx._controls import *
from wx.lib.masked.timectrl import TimeCtrl
from alarmSetting import AlarmSetting
from alarmData import Alarm

class AlarmSettingDialog(wx.Dialog):
	def __init__(self, paent, data = Alarm()):
		wx.Dialog.__init__(self, paent, title = u'闹钟设置')
		sz = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sz)
		a = AlarmSetting(self)
		sz.Add(a, proportion = 1, flag = wx.EXPAND)
		sz.Add((0, 5))
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		sz.Add(btnSizer, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		btnOK = wx.Button(self, label = u'OK')
		btnCancel = wx.Button(self, label = u'Cancel')
		btnSizer.Add((4, 0), proportion = 1, flag = wx.EXPAND)
		btnSizer.Add(btnOK, flag = wx.ALIGN_RIGHT)
		btnSizer.Add((20, 0))
		btnSizer.Add(btnCancel)
		btnSizer.Add((5, 0))
		sz.Add((0, 5))
		self.Layout()
		btnOK.Bind(wx.EVT_BUTTON, self.onOk)
		btnCancel.Bind(wx.EVT_BUTTON, self.onCancel)
		self.data = data
		self.settingPanel = a
		self.updateControls()
	def updateControls(self):
		d = self.data
		a = self.settingPanel
		a.briefEdit.SetValue(d.brief)
		a.detailedEdit.SetValue(d.content)
		if d.alarmTime != None:
			dt = wx.DateTime()
			a.datePicker.SetValue(dt.ParseDateTime(d.alarmTime))
		a.countDownTimePicker.SetValue(wx.TimeSpan.Seconds(d.countDown))
		a.repeatCheck.SetValue(d.repeat)
		if d.alarmType == u"alarm":
			a.onAlarmRadioButton(None)
		elif d.alarmType == u"count down":
			a.onCountDownRadioButton(None)

	def updateData(self):
		d = Alarm()
		a = self.settingPanel
		d.brief = a.briefEdit.GetValue()
		d.content = a.detailedEdit.GetValue()
		d.alarmTime = str(a.datePicker.GetValue())
		d.countDown = a.countDownTimePicker.GetValue(as_wxTimeSpan = True).GetSeconds()
		if a.alarmRadio.GetValue() == True:
			d.alarmType = u"alarm"
		elif a.countDownRadio.GetValue() == True:
			d.alarmType = u"count down"
		d.repeat = a.repeatCheck.GetValue()
		self.data = d
	def onOk(self, ev):
		self.updateData()
		self.EndModal(wx.ID_OK)
	def onCancel(self, ev):
		self.EndModal(wx.ID_CANCEL)
if __name__ == '__main__':
	app = wx.App(redirect = False)
	d = AlarmSettingDialog(None)
	d.ShowModal()
	app.MainLoop()
