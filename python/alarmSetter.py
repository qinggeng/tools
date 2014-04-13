#-*- coding: utf-8 -*-
import wx
from wx._controls import *
from wx.lib.masked.timectrl import TimeCtrl
from alarmSetting import AlarmSetting
class AlarmSetter(wx.Panel):
	def __init__(self, parent):
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
if __name__ == '__main__':
	app = wx.App(redirect = False)
	f = wx.Frame(None)
	sz = wx.BoxSizer(wx.VERTICAL)
	f.SetSizer(sz)
	a = AlarmSetting(f)
	sz.Add(a, proportion = 1, flag = wx.EXPAND)
	f.Layout()
	f.Show()
	app.MainLoop()
