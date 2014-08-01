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
def constantTime(timeStr):
	dt = DateTime()
	dt.ParseFormat(timeStr, u'%Y %m %d %H:%M:%S')
	return dt
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
	dt = DateTime()
	dt.SetTimeT(value)
	return dt.Format('%Y-%m-%d\n%H:%M:%S')
	return (DateTime.Today() + TimeSpan(labelIndex * 24)).Format(ur'%Y-%m-%d')
	return value

class SettingDialog(Dialog):
	def __init__(self, parent):
		Dialog.__init__(self, parent)
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
		self.drawPlot(self.axes)
		lowerBoundDateTime = DateTime()
		#lowerBoundDateTime.ParseFormat(u'1970 1 1 00:00:00', u'%Y %m %d %H:%M:%S')
		lowerBoundDateTime.ParseFormat(u'2014 5 3 00:00:00', u'%Y %m %d %H:%M:%S')
		self.defaultLowerBoundDateTime = lowerBoundDateTime
		self.activityLowerBound = self.getDefaultLowerBound
		#self.activityUpperBound = DateTime.Now
		self.activityUpperBound = functools.partial(constantTime, u'2014 5 3 12:00:00')

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
		configButton = wxTools.makeBitmapButton(
			tb,
			ActivitiesViewer.kToolbarButtonSize,
			u'appbar.cog.png')
		sz.Add(configButton)
		configButton.Bind(EVT_BUTTON, self.onConfigButton)
		self.Bind(EVT_PAINT, self.OnPaint)

	def onConfigButton(self, ev):
		pass

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
		activityNames = []
		lb = 0xFFFFFFFF
		ub = 0
		for activity in a:
			beginTime = DateTime()
			endTime = DateTime()
			beginTime.ParseFormat(activity.begin, '%m/%d/%Y %H:%M:%S')
			endTime.ParseFormat(activity.end, '%m/%d/%Y %H:%M:%S')
			last = endTime - beginTime
			dt = DateTime()
			dt.SetTimeT(beginTime.GetTicks())
			if activity.name in activityNames:
				base = activityNames.index(activity.name)
			else:
				base = len(activityNames)
				activityNames.append(activity.name)
			#print activity.name, base
			#ax.plot([beginTime.GetTicks(), endTime.GetTicks(), endTime.GetTicks(), beginTime.GetTicks(), beginTime.GetTicks()], [base + 1, base + 1, base + 1.1, base + 1.1, base + 1], color = 'blue')
			ax.bar(beginTime.GetTicks(), 0.1, endTime.GetTicks() - beginTime.GetTicks(), base + 1, label = activity.name)
			b = ax.annotate((endTime - beginTime).Format(u'%H:%M:%S'), xy = (beginTime.GetTicks(), base + 1), xycoords = 'data')
			#print dir(b.get_fontproperties())
			#print b.get_fontproperties().get_size()
			#print type(b)
			lb = min(beginTime.GetTicks(), lb)
			ub = max(endTime.GetTicks(), ub)
		#print lb, ub
		ax.axis([lb - 50, ub + 50, 0, 3])
		formatter = matplotlib.ticker.FuncFormatter(utc2Date)
		ax.xaxis.set_major_formatter(formatter)
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
