# -*- coding: utf-8 -*-
from wx import *
import matplotlib
import matplotlib.ticker
matplotlib.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, sin, pi
import wxTools
import os, sys, os.path
import re
import functools
import pickle
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

def utc2Date(value, labelIndex):
	return (DateTime.Today() + TimeSpan(labelIndex * 24)).Format(ur'%Y-%m-%d')
	return value
class ActivitiesViewer(Frame):
	kMargin = 4
	kMarginLeft = kMargin
	kMarginRight = kMargin
	kMarginTop = kMargin
	kMarginBottom = kMargin
	kToolbarWidth = 40
	kToolbarButtonSize = (kToolbarWidth, kToolbarWidth)
	kToolbarSpacing = 4
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
		toolbarPanel.SetSize((ActivitiesViewer.kToolbarWidth, 0))
		sz.Add(toolbarPanel, proportion = 0, flag = EXPAND | TOP | BOTTOM)
		toolbarPanel.SetBackgroundColour('#FFFFFF')
		self.toolbar = toolbarPanel
		self.initToolbar(toolbarPanel)
		self.figure = Figure()
		f = self.figure

		canvas = FigureCanvas(self, -1, self.figure)
		self.canvas = canvas
		sz.Add(canvas, proportion = 1, flag = EXPAND)
		self.Maximize(True)

		self.axes = f.add_subplot(111)
		formatter = matplotlib.ticker.FuncFormatter(utc2Date)
		#self.axes.xaxis.set_major_formatter(formatter)
		self.drawPlot(self.axes)
		lowerBoundDateTime = DateTime()
		#lowerBoundDateTime.ParseFormat(u'1970 1 1 00:00:00', u'%Y %m %d %H:%M:%S')
		lowerBoundDateTime.ParseFormat(u'2014 5 3 12:00:00', u'%Y %m %d %H:%M:%S')
		self.defaultLowerBoundDateTime = lowerBoundDateTime
		self.activityLowerBound = self.getDefaultLowerBound
		self.activityUpperBound = DateTime.Now

	def getDefaultLowerBound(self):
		return self.defaultLowerBoundDateTime

	def initToolbar(self, tb):
		sz = BoxSizer(VERTICAL)
		tb.SetSizer(sz)
		refreshBtn = wxTools.makeBitmapButton(
			tb, 
			ActivitiesViewer.kToolbarButtonSize, 
			u'appbar.refresh.png')
		sz.Add(refreshBtn)
		sz.Add((0, ActivitiesViewer.kToolbarSpacing))
		refreshBtn.Bind(EVT_BUTTON, self.onRefreshButton)
		self.Bind(EVT_PAINT, self.OnPaint)

	def onRefreshButton(self, ev):
		#walk through current folder, enumerate activities file
		self.reloadActivities()
		pass

	def reloadActivities(self):
		os.path.walk(
			u'.', 
			functools.partial(self.enumerateActivities, self.activityLowerBound(), self.activityUpperBound()), 
			None)
		self.updatePlot()

	def OnPaint(self, ev):
		self.canvas.draw()
		ev.Skip()

	def updatePlot(self):
		a = self.activities
		ax = self.axes
		ax.clear()
		activitiesNames = set()
		lb = 0xFFFFFFFF
		ub = 0
		for activity in a:
			beginTime = DateTime()
			endTime = DateTime()
			beginTime.ParseFormat(activity.begin, '%m/%d/%Y %H:%M:%S')
			endTime.ParseFormat(activity.end, '%m/%d/%Y %H:%M:%S')
			print beginTime, endTime
			last = endTime - beginTime
			dt = DateTime()
			dt.SetTimeT(beginTime.GetTicks())
			ax.plot([beginTime.GetTicks(), endTime.GetTicks()], [1, 1])
			lb = min(beginTime.GetTicks(), lb)
			ub = max(endTime.GetTicks(), ub)
		print lb, ub
		ax.axis([lb, ub, 0, 3])
		self.Refresh()

	def enumerateActivities(self, lower, upper, placeHolder, currentFolder, names):
			pattern = re.compile(ur'^activities\.[\d-]+\.dat$')
			names = filter(lambda x: pattern.match(x) != None, names)
			pattern = re.compile(ur'activities\.([\d-]+)\.dat')
			activities = []
			for name in names:
				savedTimeStr = pattern.match(name).group(1)
				dt = wx.DateTime()
				dt.ParseFormat(savedTimeStr, u'%Y-%m-%d-%H-%M-%S')
				if dt < lower:
					continue
				f = open(name, 'r')
				activitiesSegment = pickle.load(f)
				f.close()
				if dt > upper:
					for activity in activitiesSegment:
						activityBeginTime = DateTime()
						activityBeginTime.ParseFormat(
							activity.begin, 
							u'%m/%d/%Y %H:%M:%S')
						if activityBeginTime < upper:
							activities.append(activities)
				else:
					activities += activitiesSegment
			self.activities = activities

	def drawPlot(self, ax):
		ax.plot([1, 2], [1, 1])
		#ax.broken_barh([(1, 0.5), (2, 0.5)], [(1, 0.1), (1, 0.1)])
		#ax.axis([0, 5, 0, 5])
		annotation = ax.annotate(u'活动测试', xy=(2., 1.), xycoords='data', xytext=(1., 1.), textcoords='data')
		"""
		print dir(annotation)
		print annotation.get_size()
		print annotation.get_position()
		#print annotation.get_window_extent()
		"""

	#def OnPaint(self, ev):
	#	self.canvas.draw()
if __name__ == '__main__':
	a = wx.App(redirect = False)
	p = ActivitiesViewer()
	p.Show()
	a.MainLoop()
