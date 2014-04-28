# -*- coding: utf-8 -*-
from wx import *
import matplotlib
matplotlib.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, sin, pi
def makeBorder(window, sizer, left, right, top, bottom):
	vBorderSizer = BoxSizer(VERTICAL)
	hBorderSizer = BoxSizer(HORIZONTAL)
	window.SetSizer(vBorderSizer)
	vBorderSizer.Add((0, top))
	vBorderSizer.Add(hBorderSizer, proportion = 1, flag = EXPAND)
	vBorderSizer.Add((0, bottom))
	hBorderSizer.Add((left, 0))
	hBorderSizer.Add(sizer, proportion = 1, flag = EXPAND)
	return sizer

class ActivitiesViewer(Frame):
	kMargin = 4
	kMarginLeft = kMargin
	kMarginRight = kMargin
	kMarginTop = kMargin
	kMarginBottom = kMargin
	def __init__(self, parent = None):
		Frame.__init__(self, parent, title = u'活动查看器')
		sz = makeBorder(
			self, 
			BoxSizer(HORIZONTAL), 
			ActivitiesViewer.kMarginLeft, 
			ActivitiesViewer.kMarginRight, 
			ActivitiesViewer.kMarginTop, 
			ActivitiesViewer.kMarginBottom)
		toolbarPanel = wx.Panel(self)
		toolbarPanel.SetSize((40, 0))
		sz.Add(toolbarPanel, proportion = 0, flag = EXPAND | TOP | BOTTOM)
		toolbarPanel.SetBackgroundColour('#FFFFFF')
		self.toolbar = toolbarPanel
		self.figure = Figure()
		f = self.figure
		self.axes = f.add_subplot(111)

		canvas = FigureCanvas(self, -1, self.figure)
		self.canvas = canvas
		sz.Add(canvas, proportion = 1, flag = EXPAND)
		self.Maximize(True)

	#def OnPaint(self, ev):
	#	self.canvas.draw()
if __name__ == '__main__':
	a = wx.App(redirect = False)
	p = ActivitiesViewer()
	p.Show()
	a.MainLoop()
