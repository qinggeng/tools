# -*- coding: utf-8 -*-
from wx import *
import matplotlib
class ActivitiesViewer(Frame):
	def __init__(self, parent = None):
		Frame.__init__(self, parent, title = u'活动查看器')
		self.Maximize(True)
if __name__ == '__main__':
	a = wx.App(redirect = False)
	p = ActivitiesViewer()
	p.Show()
	a.MainLoop()
