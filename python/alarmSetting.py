#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 (standalone edition) on Sun Apr 13 23:20:36 2014
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from wx.lib.masked.timectrl import TimeCtrl
def _(str):
	return str
# end wxGlade


class AlarmSetting(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: AlarmSetting.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.panel_2 = wx.Panel(self, wx.ID_ANY)
		self.briefEdit = wx.TextCtrl(self.panel_2, wx.ID_ANY, "")
		self.detailedEdit = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)
		self.panel_3 = wx.Panel(self, wx.ID_ANY)
		self.alarmRadio = wx.RadioButton(self.panel_3, wx.ID_ANY, _(u"\u5b9a\u65f6"))
		self.datePicker = wx.DatePickerCtrl(self.panel_3, wx.ID_ANY)
		self.clockPicker = TimeCtrl(self.panel_3, wx.ID_ANY)
		self.countDownRadio = wx.RadioButton(self.panel_3, wx.ID_ANY, _(u"\u5012\u8ba1\u65f6"))
		self.countDownTimePicker = TimeCtrl(self.panel_3, wx.ID_ANY)
		self.repeatCheck = wx.CheckBox(self.panel_3, wx.ID_ANY, _(u"\u91cd\u590d\u4f7f\u7528"))

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_RADIOBUTTON, self.onAlarmRadioButton, self.alarmRadio)
		self.Bind(wx.EVT_RADIOBUTTON, self.onCountDownRadioButton, self.countDownRadio)
		# end wxGlade
		self.alarmRadio.SetValue(True)
		self.countDownTimePicker.Disable()

	def __set_properties(self):
		# begin wxGlade: AlarmSetting.__set_properties
		self.detailedEdit.SetFocus()
		self.alarmRadio.SetMinSize((80, 21))
		self.countDownRadio.SetMinSize((80, 21))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: AlarmSetting.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_8 = wx.BoxSizer(wx.VERTICAL)
		sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13 = wx.BoxSizer(wx.VERTICAL)
		sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_11 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_5 = wx.BoxSizer(wx.VERTICAL)
		sizer_6 = wx.BoxSizer(wx.VERTICAL)
		sizer_1.Add((0, 5), 0, 0, 0)
		sizer_3.Add((5, 0), 0, 0, 0)
		sizer_6.Add((0, 3), 0, 0, 0)
		label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, _(u"\u7b80\u8981\u63d0\u9192"))
		label_1.SetMinSize((48, 14))
		sizer_6.Add(label_1, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_3.Add(sizer_6, 0, wx.ALL | wx.EXPAND, 0)
		sizer_3.Add((5, 0), 0, 0, 0)
		sizer_5.Add(self.briefEdit, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_3.Add(sizer_5, 7, wx.ALL | wx.EXPAND, 0)
		sizer_3.Add((5, 0), 0, 0, 0)
		sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
		sizer_2.Add((0, 5), 0, 0, 0)
		sizer_7.Add((5, 0), 0, 0, 0)
		sizer_7.Add(self.detailedEdit, 1, wx.EXPAND, 0)
		sizer_7.Add((5, 0), 0, 0, 0)
		sizer_2.Add(sizer_7, 1, wx.EXPAND, 0)
		self.panel_2.SetSizer(sizer_2)
		sizer_1.Add(self.panel_2, 1, wx.ALL | wx.EXPAND, 0)
		sizer_8.Add((0, 5), 0, 0, 0)
		sizer_9.Add((5, 0), 0, 0, 0)
		sizer_11.Add(self.alarmRadio, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_9.Add(sizer_11, 0, wx.EXPAND, 0)
		sizer_9.Add((5, 0), 0, 0, 0)
		sizer_12.Add(self.datePicker, 0, 0, 0)
		sizer_12.Add((5, 0), 0, 0, 0)
		sizer_12.Add(self.clockPicker, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 0)
		sizer_9.Add(sizer_12, 1, wx.EXPAND, 0)
		sizer_9.Add((5, 0), 0, 0, 0)
		sizer_8.Add(sizer_9, 0, wx.EXPAND, 0)
		sizer_10.Add((5, 0), 0, 0, 0)
		sizer_13.Add(self.countDownRadio, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_10.Add(sizer_13, 0, wx.EXPAND, 0)
		sizer_10.Add((5, 0), 0, 0, 0)
		sizer_10.Add(self.countDownTimePicker, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 0)
		sizer_10.Add((5, 0), 0, 0, 0)
		sizer_8.Add(sizer_10, 0, wx.EXPAND, 0)
		sizer_14.Add((5, 0), 0, 0, 0)
		sizer_14.Add(self.repeatCheck, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_14.Add((5, 0), 0, 0, 0)
		sizer_8.Add(sizer_14, 0, wx.EXPAND, 0)
		sizer_8.Add((0, 5), 0, 0, 0)
		self.panel_3.SetSizer(sizer_8)
		sizer_1.Add(self.panel_3, 0, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		# end wxGlade

	def onAlarmRadioButton(self, event):  # wxGlade: AlarmSetting.<event_handler>
		self.datePicker.Enable()
		self.clockPicker.Enable()
		self.countDownTimePicker.Disable()

	def onCountDownRadioButton(self, event):  # wxGlade: AlarmSetting.<event_handler>
		self.datePicker.Disable()
		self.clockPicker.Disable()
		self.countDownTimePicker.Enable()

	def setValue(self, value):
		self.briefEdit.SetValue(value.brief)
		self.detailedEdit.SetValue(value.detail)
		if value.alarmType == 'countDown':
			self.onCountDownRadioButton(None)
		else if value.alarmType == 'alarm':
			self.onAlarmRadioButton(None)
		self.repeatCheck.SetValue(value.isRepeat)

	def getValue(self):
		return

# end of class AlarmSetting