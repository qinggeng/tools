# -*- coding: gbk -*-
from wx import *
import pickle
from itemGrid import ItemGrid
from itemGrid import ItemDropTarget
from alarmSetter import AlarmSettingDialog
from wx.lib.masked.timectrl import TimeCtrl
import functools
import utils
import alarmData
kIconHeight = 16
def loadBitmapFromPNGFile(path, bitmapSize):
	img = wx.Image(path)
	img.LoadFile(path, wx.BITMAP_TYPE_PNG)
	factor = 2.4
	img = img.Resize((bitmapSize[0] * factor, bitmapSize[1] * factor), (-20, -20))
	img = img.Scale(bitmapSize[0], bitmapSize[1])
	return wx.BitmapFromImage(img)
class AlarmsPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.dropTarget = ItemDropTarget(self)
		self.SetDropTarget(self.dropTarget)
		sz = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sz)
		self.SetBackgroundColour('#FFFFFF')
		self.livedAlarms = []
		self.timer = wx.Timer(self, 100)
		self.Bind(wx.EVT_TIMER, self.onTimer)
		self.timer.Start(1 * 1000, oneShot = False)
		self.livedActivities = {}
		self.finishedActivities = []
		self.Bind(EVT_CLOSE, self.onClose)

	def onClose(self, ev):
		print "close event"
		f = open(DateTime.Now().Format(u'activities.%Y-%m-%d-%H-%M-%S.dat'), 'w')
		pickle.dump(self.finishedActivities, f)
		f.close()
		ev.Skip()

	def SetSize(self, sz):
		self.GetSizer().SetMinSize(sz)
		wx.Panel.SetSize(self, sz)

	def onDragIn(self, x, y, d):
		#print "drag in"
		pass

	def onDragOut(self):
		#print "drag out"
		pass

	def onDragOver(self, x, y, d):
		#print "drag over"
		pass

	def onDragData(self, x, y, dropAction, data):
		dragTraits = pickle.loads(data)
		itemIndex = dragTraits.index
		if self.dataSource == None:
			return
		alarm = self.dataSource[itemIndex]
		self.makeAlarmPanel(alarm)

	def makeAlarmPanel(self, alarm):
		panel = wx.Panel(self)
		vBorderSizer = wx.BoxSizer(wx.HORIZONTAL)
		hBorderSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		panel.SetSizer(vBorderSizer)
		vBorderSizer.Add((0, 5))
		vBorderSizer.Add(hBorderSizer, proportion = 1, flag = wx.EXPAND)
		vBorderSizer.Add((0, 5))
		hBorderSizer.Add((5, 0))
		hBorderSizer.Add(mainSizer, proportion = 1, flag = wx.EXPAND | wx.ALL)
		hBorderSizer.Add((5, 0))
		briefText = wx.StaticText(panel)
		briefText.SetLabel(alarm.brief)
		timeCtrl = TimeCtrl(panel, fmt24hr = True, style = wx.TE_PROCESS_TAB | wx.NO_BORDER)
		timeCtrl.SetEditable(False)
		timeCtrl.SetValue(wx.TimeSpan.Seconds(alarm.countDown))
		mainSizer.Add(briefText, proportion = 0)
		mainSizer.Add((0, 10), proportion = 1, flag = wx.EXPAND | wx.ALL)
		mainSizer.Add(timeCtrl, proportion = 0)
		sz = self.GetSizer()
		panel.SetBackgroundColour('#FFFFFF')
		timeCtrl.SetBackgroundColour('#FFFFFF')
		briefText.SetBackgroundColour('#FFFFFF')
		panel.Layout()
		sz.Add(panel, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		self.Layout()
		self.livedAlarms.append(functools.partial(self.updateCountDown, panel, timeCtrl, alarm))
		if alarm.alarmType == 'count down':
			newAcitvity = alarmData.Activity()
			newAcitvity.name = alarm.brief
			newAcitvity.content = alarm.content
			newAcitvity.begin = DateTime.Now().Format('%m/%d/%Y %H:%M:%S')
			self.livedActivities[alarm] = newAcitvity

	def onTimer(self, ev):
		updatedPanels = []
		for updateFunc in self.livedAlarms:
			if True == updateFunc():
				updatedPanels.append(updateFunc)
		self.livedAlarms = updatedPanels
				

	def updateCountDown(self, panel, timerCtrl, alarm):
		stillAlive = False
		t = timerCtrl.GetValue(as_wxTimeSpan = True)
		t -= wx.TimeSpan.Seconds(1)
		if t.GetSeconds() == 0:
			utils.runCmd(u'sendNotification.py "{0}"'.format(alarm.brief))
			panel.Destroy()
			if alarm in self.livedActivities:
				activity = self.livedActivities[alarm]
				activity.end = DateTime.Now().Format('%m/%d/%Y %H:%M:%S')
				self.finishedActivities.append(activity)
				self.livedActivities.pop(alarm)
		else:
			timerCtrl.SetValue(t)
			stillAlive = True
		return stillAlive
		
		

class Reminder(Frame):
	def __init__(self):
		Frame.__init__(self, None)
		self.SetTitle(u'提醒和倒计时')
		self.loadAlarms()
		self.initialLayout()
		self.SetBackgroundColour('#E0E0E0')
	def loadAlarms(self):
		self.alarms = []
		self.displayedAlarms = []
		try:
			f = open(u'alarms.dat', 'r')
			self.alarms = pickle.load(f)
			self.displayedAlarms = self.alarms[:]
			f.close()
		except Exception, e:
			pass

	def presentAlarm(self, alarm, panel):
		pass
	def initialLayout(self):
		sz = BoxSizer(VERTICAL)
		self.SetSizer(sz)
		hsz = BoxSizer(HORIZONTAL)
		sz.Add((0, 8))
		sz.Add(hsz, proportion = 1, flag = EXPAND|ALL)
		sz.Add((0, 8))
		mainSizer = BoxSizer(HORIZONTAL)
		hsz.Add((8, 0))
		hsz.Add(mainSizer, proportion = 1, flag = EXPAND|ALL)
		hsz.Add((8, 0))
		alarmsPanel = AlarmsPanel(self)
		alarmsPanel.SetSize((200, 100))
		#alarmsPanel.SetBackgroundColour('#8080FF')
		alarmsPanel.dataSource = self.displayedAlarms
		mainSizer.Add(alarmsPanel, proportion = 0, flag = EXPAND | TOP | BOTTOM)
		mainSizer.Add((2, 0))
		poolPanel = Panel(self)
		poolPanel.SetBackgroundColour('#FF808080')
		mainSizer.Add(poolPanel, proportion = 1, flag = EXPAND | ALL)
		poolSizer = BoxSizer(VERTICAL)
		poolToolsPanel = Panel(poolPanel)
		poolToolsPanel.SetSize((0, kIconHeight))
		poolPanel.SetSizer(poolSizer)
		poolSizer.Add(poolToolsPanel, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		self.initializePoolTools(poolToolsPanel)
		line = StaticLine(poolPanel)
		line.SetBackgroundColour('#FF0000');
		poolSizer.Add(line, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		alarmsGrid = ItemGrid(poolPanel)
		self.alarmsGrid = alarmsGrid
		poolSizer.Add(alarmsGrid, proportion = 1, flag = EXPAND | ALL)

		poolPanel.SetBackgroundColour('#FFFFFF')
		alarmsGrid.itemCount = self.alarmsCount
		alarmsGrid.itemDesiredHeight = self.alarmPanelHeight
		alarmsGrid.prepareItemPanel = self.displayAlarmPanel
		self.Layout()
		self.Bind(wx.EVT_CLOSE, self.onDestory)
		self.alarmPanel = alarmsPanel
	
	def onDestory(self, ev):
		pickle.dump(self.alarms, open(u'alarms.dat', 'w'))
		self.alarmPanel.Close()
		ev.Skip()

	def initializePoolTools(self, toolsPanel):
		p = toolsPanel
		sz = BoxSizer(HORIZONTAL)
		p.SetSizer(sz)
		sz.Add((4, 2))
		createBtn = BitmapButton(p, style = 0)
		createBtn.SetSize((kIconHeight, kIconHeight))
		createBtn.SetBackgroundColour('#FFFFFF')
		createBtn.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.add.png', (kIconHeight, kIconHeight)))
		createBtn.Bind(EVT_BUTTON, self.createNewAlarm)
		sz.Add(createBtn, flag = SHAPED)
		sz.Add((4, 2))
		filterBtn = BitmapButton(p, style = 0)
		filterBtn.SetSize((kIconHeight, kIconHeight))
		filterBtn.SetBackgroundColour('#FFFFFF')
		filterBtn.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.filter.png', (kIconHeight, kIconHeight)))
		sz.Add(filterBtn, flag = SHAPED)


		plotButton = BitmapButton(p, style = 0)
		plotButton.SetSize((kIconHeight, kIconHeight))
		plotButton.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.graph.line.png', (kIconHeight, kIconHeight)))
		plotButton.SetBackgroundColour('#FFFFFF')
		sz.Add(plotButton, proportion = 1, flag = SHAPED | ALIGN_RIGHT)
		sz.Add((4, 2))
		configButton = BitmapButton(p, style = 0)
		configButton.SetSize((kIconHeight, kIconHeight))
		configButton.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.cog.png', (kIconHeight, kIconHeight)))
		configButton.SetBackgroundColour('#FFFFFF')
		sz.Add(configButton, proportion = 1, flag = SHAPED | ALIGN_RIGHT)

	def onConfigBtn(self, ev):
		pass

	def createNewAlarm(self, ev):
		dlg = AlarmSettingDialog(self)
		if wx.ID_OK != dlg.ShowModal():
			return
		self.addAlarm(dlg.data)
	def addAlarm(self, newAlarm):
		self.alarms.append(newAlarm)
		self.displayedAlarms.append(newAlarm)
		self.alarmsGrid.refresh()

	def SetSize(self, size):
		Frame.SetSize(self, size)
		self.alarmsGrid.refresh()
	
	def alarmsCount(self):
		return len(self.displayedAlarms)

	def alarmPanelHeight(self, itemIndex, maximumWidth, maximumHeight):
		return 100

	def displayAlarmPanel(self, panel, itemIndex):
		d = self.displayedAlarms[itemIndex]
		sz = wx.BoxSizer(wx.VERTICAL)
		panel.SetSizer(sz)
		vsz = BoxSizer(HORIZONTAL)
		hsz = BoxSizer(VERTICAL)
		briefText = wx.StaticText(panel, style = ALIGN_CENTER_VERTICAL)
		briefText.SetLabel(d.brief)
		vsz.Add(hsz, proportion = 0, flag = wx.EXPAND | BOTTOM | TOP)
		hsz.Add(briefText, proportion = 1, flag = SHAPED | ALIGN_CENTER_VERTICAL)
		closeBtn = BitmapButton(panel, style = 0)
		closeBtn.SetSize((kIconHeight, kIconHeight))
		closeBtn.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.close.png', (kIconHeight, kIconHeight)))
		closeBtn.SetBackgroundColour('#FFFFFF')

		editBtn = BitmapButton(panel, style = 0)
		editBtn.SetSize((kIconHeight, kIconHeight))
		editBtn.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.edit.png', (kIconHeight, kIconHeight)))
		editBtn.SetBackgroundColour('#FFFFFF')

		vsz.Add((5, 0), proportion = 1, flag = EXPAND | LEFT | RIGHT)
		vsz.Add(editBtn, proportion = 0, flag = SHAPED | ALIGN_RIGHT)
		vsz.Add((8, 0))
		vsz.Add(closeBtn, proportion = 0, flag = SHAPED | ALIGN_RIGHT)
		sz.Add(vsz, proportion = 0, flag = EXPAND| LEFT | RIGHT)
		sz.Add((0, 5))
		timeText = wx.StaticText(panel)
		sz.Add(timeText, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT)
		if d.alarmType == u'alarm':
			timeText.SetLabel(u'At %s' %(str(d.alarmTime), ))
		elif d.alarmType == u'count down':
			timeText.SetLabel(u'After %s' % (str(wx.TimeSpan.Seconds(d.countDown)), ))

		closeBtn.Bind(EVT_BUTTON, functools.partial(self.deleteAlarm, panel, d))
		editBtn.Bind(EVT_BUTTON, functools.partial(self.editAlarm, briefText, timeText, d))
		panel.Layout()

	def deleteAlarm(self, panel, alarm, delEvent):
		index = self.displayedAlarms.index(alarm)
		self.displayedAlarms.remove(alarm)
		self.alarms.remove(alarm)
		panel.Destroy()
		self.alarmsGrid.itemDeleted(index)

	def editAlarm(self, briefText, timeText, alarm, editEvent):
		dlg = AlarmSettingDialog(self, alarm)
		if dlg.ShowModal() == ID_OK:
			d = dlg.data
			alarm.brief = d.brief
			alarm.content = d.content
			alarm.alarmType = d.alarmType
			alarm.alarmTime = d.alarmTime
			alarm.countDown = d.countDown
			briefText.SetLabel(alarm.brief)
			if alarm.alarmType == u'alarm':
				timeText.SetLabel(u'At %s' %(str(alarm.alarmTime), ))
			elif alarm.alarmType == u'count down':
				timeText.SetLabel(u'After %s' % (str(wx.TimeSpan.Seconds(alarm.countDown)), ))

		
if __name__ == '__main__':
	a = wx.App(redirect = False)
	p = Reminder()
	p.SetSize((800, 600))
	p.Show()
	a.MainLoop()
