#-*- coding: utf-8 -*-
from wx import *
import wxTools
import re
from wx.lib.masked.timectrl import TimeCtrl
kMarginDefault = 2
kMarginTop = kMarginDefault
kMarginBottom = kMarginDefault
kMarginLeft = kMarginDefault
kMarginRight = kMarginDefault
kTouchButtonSize = (48, 48)
kDlgSize = (640, 480)
kDefaultMargins = (kMarginTop, kMarginBottom, kMarginLeft, kMarginRight)
kTimerStyle = DEFAULT_FRAME_STYLE ^ (MAXIMIZE_BOX | MINIMIZE_BOX | CLOSE_BOX | SYSTEM_MENU | RESIZE_BORDER )
def makeMargin(window, sizer, margins):
	vBorderSizer = BoxSizer(VERTICAL)
	hBorderSizer = BoxSizer(HORIZONTAL)
	vBorderSizer.Add((0, margins[0]))
	vBorderSizer.Add(hBorderSizer, proportion = 1, flag = EXPAND)
	vBorderSizer.Add((0, margins[1]))
	hBorderSizer.Add((margins[2], 0))
	hBorderSizer.Add(sizer, proportion = 1, flag = EXPAND)
	hBorderSizer.Add((margins[3], 0))
	window.SetSizer(vBorderSizer)

class ScheduleElementEditor(Panel):
	def __init__(self, parent):
		Panel.__init__(self, parent)
		self.SetBackgroundColour("white")
		sz = BoxSizer(HORIZONTAL)
		makeMargin(self, sz, kDefaultMargins)
		contentSizer = BoxSizer(VERTICAL)
		sz.Add(contentSizer, proportion = 1, flag = EXPAND)
		configSizer = BoxSizer(VERTICAL)
		sz.Add(configSizer, proportion = 1, flag = EXPAND)
		titleEdit = TextCtrl(self)
		contentSizer.Add(titleEdit, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		contentSizer.Add((0, kMarginBottom))
		contentSizer.Add((0, kMarginTop))
		detailEdit = TextCtrl(self, style = TE_MULTILINE | TE_LINEWRAP)
		contentSizer.Add(detailEdit, proportion = 1, flag = EXPAND)
		clauseSizer = BoxSizer(HORIZONTAL)
		beginSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY, choices = ['自动启动', '人工启动'])
		beginSelection.SetSelection(0)
		clauseSizer.Add(beginSelection, proportion = 1, flag = EXPAND | LEFT |RIGHT)
		refSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY, choices = ['于时间', '于议题'])
		clauseSizer.Add(refSelection, proportion = 1, flag = EXPAND)
		scheduleSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY)
		clauseSizer.Add(scheduleSelection, proportion = 1, flag = EXPAND)
		datePicker = DatePickerCtrl(self)
		clauseSizer.Add(datePicker, proportion = 1, flag = EXPAND)
		clockPicker = TimeCtrl(self)
		clauseSizer.Add(clockPicker, proportion = 1, flag = EXPAND)
		configSizer.Add(clauseSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		
		

class ScheduleElementDlg(Dialog):
	def __init__(self, parent):
		Dialog.__init__(self, parent, title = '环节设置', size = kDlgSize)
		self.SetBackgroundColour("white")
		sz = BoxSizer(VERTICAL)
		self.SetSizer(sz)
		editor = ScheduleElementEditor(self)
		sz.Add(editor, proportion = 1, flag = EXPAND | ALL)
		line = StaticLine(self, style = LI_HORIZONTAL)
		sz.Add(line, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		buttonsSizer = BoxSizer(HORIZONTAL)
		buttonsSizer.SetMinSize(kTouchButtonSize)
		sz.Add(buttonsSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		okayButton = wxTools.makeBitmapButton(self, kTouchButtonSize, "appbar.check.png")
		okayButton.SetBackgroundColour("white")
		okayButton.SetSize(kTouchButtonSize)
		cancelButton = wxTools.makeBitmapButton(self, kTouchButtonSize, "appbar.close.png")
		cancelButton.SetSize(kTouchButtonSize)
		cancelButton.SetBackgroundColour("white")
		buttonsSizer.Add((1, 0), proportion = 1, flag = EXPAND)
		buttonsSizer.Add(cancelButton, proportion = 0, flag = ALIGN_RIGHT | SHAPED)
		buttonsSizer.Add((12, 0))
		buttonsSizer.Add(okayButton, proportion = 0, flag = ALIGN_RIGHT | SHAPED)
		buttonsSizer.Add((12, 0))

class ScheduleTimer(Frame):
	def __init__(self):
		Frame.__init__(self, None, title = '议程计时器', size = (200, 640), style = kTimerStyle)
		vBorderSizer = BoxSizer(VERTICAL)
		hBorderSizer = BoxSizer(HORIZONTAL)
		mainSizer = BoxSizer(VERTICAL)
		self.SetSizer(vBorderSizer)
		vBorderSizer.Add((0, kMarginTop))
		vBorderSizer.Add(hBorderSizer, proportion = 1, flag = EXPAND)
		vBorderSizer.Add((0, kMarginBottom))
		hBorderSizer.Add((kMarginLeft, 0))
		hBorderSizer.Add(mainSizer, proportion = 1, flag = EXPAND)
		hBorderSizer.Add((kMarginRight, 0))
		self.SetBackgroundColour("white")
		buttonsSizer = BoxSizer(HORIZONTAL)
		powerBtn = wxTools.makeBitmapButton(self, kTouchButtonSize, "appbar.power.png")
		powerBtn.SetBackgroundColour("white")
		startBtn = wxTools.makeBitmapButton(self, kTouchButtonSize, "appbar.control.play.png")
		startBtn.SetBackgroundColour("white")
		buttonsSizer.Fit(powerBtn)
		buttonsSizer.Fit(startBtn)
		buttonsSizer.Add(startBtn, flag = SHAPED)
		buttonsSizer.Add(powerBtn, proportion = 1, flag = SHAPED | ALIGN_RIGHT)
		mainSizer.Add(buttonsSizer, flag = EXPAND | LEFT | RIGHT, proportion = 0)
		line = StaticLine(self, style = LI_HORIZONTAL)
		mainSizer.Add(line, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		powerBtn.Bind(EVT_BUTTON, self.onEditSecheduleElement)

	def onEditSecheduleElement(self, ev):
		dlg = ScheduleElementDlg(self)
		dlg.ShowModal()

if __name__ == '__main__':
	app = wx.App(redirect = False)
	#app = wx.App()
	a = ScheduleTimer()
	a.Show()
	app.MainLoop()
