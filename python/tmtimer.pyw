#-*- coding: utf-8 -*-
from wx import *
class TmTimer(Frame):
	def __init__(self):
		Frame.__init__(self, parent = None)
		sz = BoxSizer(HORIZONTAL)
		self.SetSizer(sz)
		l = ListCtrl(self)
		style = l.GetWindowStyle()
		l.SetWindowStyle(style | BORDER_NONE)
		sz.Add(l, proportion = 15, flag = EXPAND)
		p = Panel(self)
		sz.Add(p, proportion = 85, flag = EXPAND)
		

if __name__ == '__main__':
	a = wx.App(redirect = False)
	f = TmTimer()
	f.ShowFullScreen(True)
	a.MainLoop()
