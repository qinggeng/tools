#-*- coding: utf-8 -*-
import wx
from wx._controls import *
from wx.lib.masked.timectrl import TimeCtrl
from alarmSetting import AlarmSetting
from alarmData import Alarm
class AlarmSetter(wx.Panel):
	def __init__(self, parent, data = Alarm()):
		spacing = 5
		wx.Panel.__init__(self, parent)
		vsz = wx.BoxSizer(wx.VERTICAL)
		sz = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(vsz)
		vsz.Add(sz)
		rbtn = wx.RadioButton(self)
		rbtn.SetLabel(u"定时")
		datePicker = DatePickerCtrl(self)
		timePicker = TimeCtrl(self)
		sz.Add((spacing, -1))
		vsz = wx.BoxSizer(wx.VERTICAL)
		sz.Add(vsz, proportion = 0, flag = wx.EXPAND | wx.TOP | wx.BOTTOM)
		vsz.Add(rbtn, proportion = 1, flag = wx.ALIGN_CENTER_VERTICAL)
		sz.Add((spacing, -1), flag = wx.ALIGN_CENTER_VERTICAL)
		sz.Add(datePicker, proportion = 0, flag = wx.ALIGN_LEFT)
		sz.Add((spacing, -1))
		sz.Add(timePicker, flag = wx.ALIGN_RIGHT)
		sz = wx.BoxSizer(wx.HORIZONTAL)
		vsz = self.GetSizer()
		vsz.Add(sz)
		rbtn = wx.RadioButton(self)
		rbtn.SetLabel(u"倒计时")
		vsz = wx.BoxSizer(wx.VERTICAL)
		sz.Add((spacing, -1))
		sz.Add(vsz, proportion = 0, flag = wx.EXPAND | wx.TOP | wx.BOTTOM)
		vsz.Add(rbtn, proportion = 1, flag = wx.ALIGN_CENTER_VERTICAL)
		cb = TimeCtrl(self, fmt24hr = True)
		sz.Add((spacing, -1))
		sz.Add(cb, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		self.Layout()

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
	def onOk(self, ev):
		self.EndModal(wx.ID_OK)
	def onCancel(self, ev):
		self.EndModal(wx.ID_CANCEL)
if __name__ == '__main__':
	app = wx.App(redirect = False)
	#f = wx.Frame(None)
	#sz = wx.BoxSizer(wx.VERTICAL)
	#f.SetSizer(sz)
	#a = AlarmSetting(f)
	#sz.Add(a, proportion = 1, flag = wx.EXPAND)
	#f.Layout()
	d = AlarmSettingDialog(None)
	d.ShowModal()
	#f.Show()
	app.MainLoop()
