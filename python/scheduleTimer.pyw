#-*- coding: utf-8 -*-
from wx import *
import wxTools
import re
import functools
from wx.lib.masked.timectrl import TimeCtrl
import uuid
import pickle
from wx.lib.floatcanvas.NavCanvas import NavCanvas
from wx.lib.floatcanvas import FloatCanvas
"""
关于议程数据结构的设计
= 议程的开始有三种方式：
== 手动开始
== 自动开始于绝对时间点
== 自动开始于相对时间点
= 两个议程有重合部分，则分离，否则顺序排列
= 最右边为当前时间点
= 取所有手动开始的议程竖直分布，放在最右边
= 取所有绝对时间点的议程，放置在对应的时间点
== 如果时间点早于当前时间，则该议程变为手动开始的议程
== 
"""
kMarginDefault = 2
kMarginTop = kMarginDefault
kMarginBottom = kMarginDefault
kMarginLeft = kMarginDefault
kMarginRight = kMarginDefault
kTouchButtonSize = (48, 48)
kDlgSize = (640, 480)
kDefaultMargins = (kMarginTop, kMarginBottom, kMarginLeft, kMarginRight)
kTimerStyle = DEFAULT_FRAME_STYLE ^ (MAXIMIZE_BOX | MINIMIZE_BOX | CLOSE_BOX | SYSTEM_MENU | RESIZE_BORDER )
kTick = 5
def partition(func, seq):
	trueSeq = []
	falseSeq = []
	for elem in seq:
		if True == func(elem):
			trueSeq.append(elem)
		else:
			falseSeq.append(elem)
	return (trueSeq, falseSeq)

class Schedule:
	kBeginManually = 0
	kBeginAutomatically = 1
	kRefPointTime = 2
	kRefPointSchedule = 3
	kBeginAfterStart = 4
	kBeginAfterFinish = 5
	kEndManually = 6
	kEndAutomatically = 7
	def __init__(self, caption = r''):
		self.beginMethod = Schedule.kBeginManually
		self.refMethod = Schedule.kRefPointTime
		self.startPoint = Schedule.kBeginAfterFinish
		self.finishMethod = Schedule.kEndManually
		self.beginTime = 0
		self.limitTime = 0
		self.refTime = 0
		self.caption = caption
		self.detail = r""
		self.guid = uuid.uuid4()
		self.refGuid = None
	
	def startAfterFinish(self, refSchedule, timespan = TimeSpan(0, 0, 0)):
		self.beginMethod = Schedule.kBeginAutomatically
		self.refMethod = Schedule.kRefPointSchedule
		self.startPoint = Schedule.kBeginAfterFinish
		self.setRefTime(timespan)
		self.refGuid = refSchedule.guid

	def startAfterBegin(self, refSchedule, timespan = TimeSpan(0, 0, 0)):
		self.beginMethod = Schedule.kBeginAutomatically
		self.refMethod = Schedule.kRefPointSchedule
		self.startPoint = Schedule.kBeginAfterStart
		self.setRefTime(timespan)
		self.refGuid = refSchedule.guid

	def setBeginMethod(self, method):
		self.beginMethod = method

	def setRefMethod(self, method):
		self.refMethod = method

	def setStartPoint(self, refPoint):
		self.startPoint = refPoint

	def setFinishedMethod(self, method):
		self.finishMethod = method

	def setBeginTime(self, dt):
		self.beginTime = dt.GetTicks()

	def getBeginTime(self):
		dt = DateTime()
		dt.SetTimeT(self.beginTime)
		return dt

	def setLimitTime(self, ts):
		self.limitTime = ts.GetSeconds()

	def getLimitTime(self):
		ts = TimeSpan().Seconds(self.refTime)
		return ts

	def setRefTime(self, ts):
		self.refTime = ts.GetSeconds()

	def getRefTime(self):
		ts = TimeSpan()
		ts.SetSeconds(self.refTime)
		return ts

def testSchedules():
	"""
	总议程，手动开始，两小时"""
	schedules = []
	mainSchedule = Schedule()
	mainSchedule.caption = r'总议程'
	mainSchedule.detail = r'中文演讲俱乐部例行活动'
	mainSchedule.setLimitTime(TimeSpan(2, 0, 0))
	schedules.append(mainSchedule)
	"""接待和签到，15分钟"""
	signIn = Schedule()
	signIn.caption=r'签到'
	signIn.beginMethod = Schedule.kBeginAutomatically
	signIn.refMethod = Schedule.kRefPointSchedule
	signIn.startPoint = Schedule.kBeginAfterStart
	signIn.setLimitTime(TimeSpan(0, 15, 0))
	signIn.refGuid = mainSchedule.guid
	schedules.append(signIn)
	"""问候"""
	sayHello = Schedule(r'问候')
	sayHello.startAfterFinish(signIn, TimeSpan(0, 0, 0))
	sayHello.setLimitTime(TimeSpan(0, 5, 0))
	schedules.append(sayHello)

	"""致辞"""
	chiefToast = Schedule(r"致辞")
	chiefToast.setLimitTime(TimeSpan(0, 2, 0))
	chiefToast.startAfterFinish(sayHello)
	schedules.append(chiefToast)
	"""主持人开场"""
	toast = Schedule(r'开场')
	toast.setLimitTime(TimeSpan(0, 1, 0))
	toast.startAfterFinish(chiefToast)
	schedules.append(toast)
	"""roles introduction"""
	rolesIntroduction = Schedule(r'功能角色介绍')
	rolesIntroduction.setLimitTime(TimeSpan(0, 4, 0))
	rolesIntroduction.startAfterFinish(toast)
	schedules.append(rolesIntroduction)
	"""timer"""
	timerIntroduction = Schedule(r'时间官')
	timerIntroduction.setLimitTime(TimeSpan(0, 1, 0))
	timerIntroduction.startAfterBegin(rolesIntroduction)
	schedules.append(timerIntroduction)
	"""ah counter"""
	ahCounterIntroduction = Schedule(r'时间官')
	ahCounterIntroduction.setLimitTime(TimeSpan(0, 1, 0))
	ahCounterIntroduction.startAfterFinish(timerIntroduction)
	schedules.append(ahCounterIntroduction)
	"""grammian"""
	grammianIntroduction = Schedule(r'时间官')
	grammianIntroduction.setLimitTime(TimeSpan(0, 1, 0))
	grammianIntroduction.startAfterFinish(ahCounterIntroduction)
	schedules.append(grammianIntroduction)
	"""general evaluator"""
	generalEvaluatorIntroduction = Schedule(r'时间官')
	generalEvaluatorIntroduction.setLimitTime(TimeSpan(0, 1, 0))
	generalEvaluatorIntroduction.startAfterFinish(grammianIntroduction)
	schedules.append(generalEvaluatorIntroduction)
	return schedules

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
		sz.Add((kMarginRight, 0))
		sz.Add((kMarginLeft, 0))
		configSizer = BoxSizer(VERTICAL)
		sz.Add(configSizer, proportion = 1, flag = EXPAND)
		titleEdit = TextCtrl(self)
		contentSizer.Add(titleEdit, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		contentSizer.Add((0, kMarginBottom))
		contentSizer.Add((0, kMarginTop))
		detailEdit = TextCtrl(self, style = TE_MULTILINE | TE_LINEWRAP)
		contentSizer.Add(detailEdit, proportion = 1, flag = EXPAND)
		clauseSizer = BoxSizer(HORIZONTAL)
		issueSizer = BoxSizer(HORIZONTAL)
		timeSelectingSizer = BoxSizer(HORIZONTAL)
		beginSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY, choices = ['自动启动', '人工启动'])
		beginSelection.SetSelection(0)
		clauseSizer.Add(beginSelection, proportion = 1, flag = EXPAND | LEFT |RIGHT)
		refSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY, choices = ['于时间', '于议题'])
		clauseSizer.Add(refSelection, proportion = 1, flag = EXPAND)
		scheduleSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY)
		issueSizer.Add(scheduleSelection, proportion = 1, flag = EXPAND)
		startPointSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY, choices = ['开始之后', '结束之后'])
		issueSizer.Add(startPointSelection, proportion = 1, flag = EXPAND)
		datePicker = DatePickerCtrl(self)
		timeSelectingSizer.Add(datePicker, proportion = 1, flag = EXPAND)
		clockPicker = TimeCtrl(self, fmt24hr = True)
		timeSelectingSizer.Add(clockPicker, proportion = 1, flag = EXPAND)
		configSizer.Add(clauseSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		configSizer.Add((0, kMarginTop))
		configSizer.Add(issueSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		configSizer.Add((0, kMarginTop))
		configSizer.Add(timeSelectingSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		timeLimitTitle = StaticText(self)
		timeLimitTitle.SetLabel('议程时长:')
		endMethodTitle = StaticText(self)
		endMethodTitle.SetLabel('议程结束方式:')
		endMethodSelection = ComboBox(self, style = CB_DROPDOWN | CB_READONLY, choices = ['自动结束', '人工结束'])
		timeLimitCtrl = TimeCtrl(self, fmt24hr = True)
		endMethodSizer = BoxSizer(HORIZONTAL)
		limitTimeSizer = BoxSizer(HORIZONTAL)
		endMethodSizer.Add(endMethodTitle, proportion = 1, flag = EXPAND | LEFT | RIGHT)
		endMethodSizer.Add(endMethodSelection, proportion = 1, flag = EXPAND | LEFT | RIGHT)
		limitTimeSizer.Add(timeLimitTitle, proportion = 1, flag = EXPAND | LEFT | RIGHT)
		limitTimeSizer.Add(timeLimitCtrl, proportion = 1, flag = EXPAND | LEFT | RIGHT)
		configSizer.Add((0, kMarginBottom))
		configSizer.Add(StaticLine(self, HORIZONTAL), proportion = 0, flag = EXPAND | LEFT | RIGHT)
		configSizer.Add((0, kMarginTop))
		configSizer.Add(limitTimeSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		configSizer.Add((0, kMarginTop))
		configSizer.Add(endMethodSizer, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		

		beginSelection.Bind(EVT_COMBOBOX, functools.partial(self.onBeginSelection, beginSelection))
		refSelection.Bind(EVT_COMBOBOX, self.onRefSelection)

		self.titleEdit = titleEdit
		self.detailEdit = detailEdit
		self.beginSelection = beginSelection
		self.refSelection = refSelection
		self.scheduleSelection = scheduleSelection
		self.startPointSelection  = startPointSelection
		self.datePicker = datePicker
		self.clockPicker = clockPicker
		self.timeLimitPicker = timeLimitCtrl
		self.endMethodSelection = endMethodSelection
		self.beginSelection.SetSelection(1)
		self.onBeginSelection(beginSelection, None)
		self.schedulesCount = None
		self.scheduleNameAtIndex = None
		self.scheduleUuidAtIndex = None

	def setSchedule(self, schedule):
		self.titleEdit.SetValue(schedule.caption)
		self.detailEdit.SetValue(schedule.detail)
		self.setBeginSelection(schedule.beginMethod)
		self.datePicker.SetValue(schedule.getBeginTime())
		self.clockPicker.SetValue(schedule.getBeginTime())
		self.timeLimitPicker.SetValue(schedule.getLimitTime())
		self.setRefSeelction(schedule.refMethod)
		self.setStartPointSelection(schedule.startPoint)
		self.setFinishMethod(schedule.finishMethod)
		self.scheduleGuid = schedule.guid
		selection = 0
		for index in range(self.schedulesCount()):
			guid = self.scheduleUuidAtIndex(index)
			name = self.scheduleNameAtIndex(index)
			if guid == schedule.refGuid:
				selection = index
			if guid == schedule:
				continue
			self.scheduleSelection.Append(name)
		self.scheduleSelection.SetSelection(selection)
				
		#TODO ref schedule setting

	def getSchedule(self):
		schedule = Schedule()
		schedule.caption = self.titleEdit.GetValue()
		schedule.detail = self.detailEdit.GetValue()
		if self.beginSelection.GetSelection() == 0:
			schedule.beginMethod = Schedule.kBeginManually
		elif self.beginSelection.GetSelection() == 1:
			schedule.beginMethod = schedule.kBeginAutomatically
		if self.refSelection.GetSelection() == 0:
			schedule.refMethod == Schedule.kRefPointTime
		elif self.refSelection.GetSelection() == 1:
			schedule.refMethod == Schedule.kRefPointSchedule
		if self.startPointSelection.GetSelection() == 0:
			schedule.refMethod == Schedule.kBeginAfterStart
		elif self.startPointSelection.GetSelection() == 1:
			schedule.refMethod == Schedule.kBeginAfterFinish
		if self.endMethodSelection.GetSelection() == 0:
			schedule.refMethod == Schedule.kEndManually
		elif self.endMethodSelection.GetSelection() == 1:
			schedule.refMethod == Schedule.kEndAutomatically
		schedule.guid = self.scheduleGuid
		#TODO ref schedule
		return schedule

	def setFinishMethod(self, method):
		if method == Schedule.kEndManually:
			self.endMethodSelection.SetSelection(0)
		elif method == Schedule.kEndAutomatically:
			self.endMethodSelection.SetSelection(1)

	def setStartPointSelection(self, refPoint):
		if refPoint == Schedule.kBeginAfterStart:
			self.startPointSelection.SetSelection(0)
		elif refPoint == Schedule.kBeginAfterFinish:
			self.startPointSelection.SetSelection(1)

	def setRefSeelction(self, method):
		if method == Schedule.kRefPointTime:
			self.refSelection.SetSelection(0)
		elif method == Schedule.kRefPointSchedule:
			self.refSelection.SetSelection(0)
		self.onRefSelection(None)
	
	def setBeginSelection(self, method):
		if method == Schedule.kBeginManually:
			self.beginSelection.SetSelection(0)
		elif method == Schedule.kBeginAutomatically:
			self.beginSelection.SetSelection(1)
		self.onBeginSelection(self.beginSelection, None)

	def onRefSelection(self, ev):
		self.refSelection.Show()
		selIndex = self.refSelection.GetCurrentSelection()
		if selIndex == 0:
			self.scheduleSelection.Hide()
			self.startPointSelection.Hide()
			self.datePicker.Show()
			self.clockPicker.Show()
		elif selIndex == 1:
			self.scheduleSelection.Show()
			self.startPointSelection.Show()
			self.datePicker.Hide()
			self.clockPicker.Show()
		self.Layout()
		
	def onBeginSelection(self, combo, ev):
		selIndex = combo.GetCurrentSelection()
		if selIndex == 1:
			self.refSelection.Hide()
			self.scheduleSelection.Hide()
			self.startPointSelection.Hide()
			self.datePicker.Hide()
			self.clockPicker.Hide()
		else:
			self.refSelection.Show()
			#self.scheduleSelection.Show()
			#self.startPointSelection.Show()
		self.Layout()
		

class ScheduleElementDlg(Dialog):
	def __init__(self, parent):
		Dialog.__init__(self, parent, title = '环节设置', size = kDlgSize)
		self.SetBackgroundColour("white")
		sz = BoxSizer(VERTICAL)
		self.SetSizer(sz)
		editor = ScheduleElementEditor(self)
		self.scheduleEditor = editor
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
		okayButton.Bind(EVT_BUTTON, self.onConfirm)
		cancelButton.Bind(EVT_BUTTON, self.onCancel)
	def onConfirm(self, ev):
		self.EndModal(ID_OK)

	def onCancel(self, ev):
		self.EndModal(ID_CANCEL)

class ScheduleTimer(Frame):
	def __init__(self):
		Frame.__init__(self, None, title = '议程计时器', size = (1024, 768), style = kTimerStyle)
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
		openButton = wxTools.makeBitmapButton(self, kTouchButtonSize, "appbar.folder.open.png")
		openButton.SetBackgroundColour("white")
		addButton = wxTools.makeBitmapButton(self, kTouchButtonSize, "appbar.add.png")
		addButton.SetBackgroundColour("white")
		buttonsSizer.Fit(startBtn)
		buttonsSizer.Fit(openButton)
		buttonsSizer.Fit(addButton)
		buttonsSizer.Fit(powerBtn)
		buttonsSizer.Add(openButton, flag = SHAPED)
		buttonsSizer.Add(addButton, flag = SHAPED)
		buttonsSizer.Add(startBtn, flag = SHAPED)
		buttonsSizer.Add(powerBtn, proportion = 1, flag = SHAPED | ALIGN_RIGHT)
		mainSizer.Add(buttonsSizer, flag = EXPAND | LEFT | RIGHT, proportion = 0)
		line = StaticLine(self, style = LI_HORIZONTAL)
		mainSizer.Add(line, proportion = 0, flag = EXPAND | LEFT | RIGHT)
		#self.canvas = NavCanvas(self, ID_ANY, (0, 0))
		self.canvas = FloatCanvas.FloatCanvas(self, ID_ANY, (0, 0))
		mainSizer.Add(self.canvas, proportion = 1, flag = EXPAND)
		self.canvas.SetBackgroundColour("black")
		powerBtn.Bind(EVT_BUTTON, self.onEditSecheduleElement)
		self.schedules = []
		"""
		draw testing objects
		"""
		#t = FloatCanvas.ScaledTextBox("""你好, 世界 
#Hello world""", (0, 0), 12)
		#t.Move((-400, 0))
		#bottomLeft, topRight = t.BoundingBox
		#print bottomLeft
		#print topRight
		#rect = FloatCanvas.Rectangle((bottomLeft[0], bottomLeft[1]), (topRight[0] - bottomLeft[0], topRight[1] - bottomLeft[1]), FillColor = 'yellow', LineColor = None)
		#self.canvas.AddObject(rect)
		#self.canvas.AddObject(t)
		#t = FloatCanvas.ScaledTextBox("""你好, 世界 
#Hello world""", (0, 16), 12)
		#t = FloatCanvas.ScaledTextBox("""你好, 世界 
#Hello world""", (topRight[0], topRight[1] - bottomLeft[1]), 12)
		#self.canvas.AddObject(t)
		self.Layout()
		self.makeSchedules(testSchedules())
		return
		g = self.makeProgressHint('test progress\n00: 00: 00', progressFactor = 1.2, color = 'yellow')
		self.canvas.AddObject(g)
		#self.canvas.Zoom(0.9)
		zeroPoint = self.canvas.PixelToWorld((0, 0))
		g.Move(zeroPoint)
		bl, tr = g.ObjectList[1].BoundingBox
		lineBegin = (tr[0], bl[1])
		lineEnd = (tr[0], bl[1] - (tr[1] - bl[1]) - 100)
		l = FloatCanvas.Line([lineBegin, lineEnd], LineColor = 'red', LineStyle = 'DotDash')
		self.canvas.AddObject(l)

	def makeSchedules(self, schedules):
		figures = {}
		scheduleByGuid = {}
		scheduleDependencies = {}
		manuallySchedules = []
		automaticallySchedules = []
		screenTopLeft = self.canvas.PixelToWorld((0, 0))
		screenBottomRight = self.canvas.PixelToWorld((self.canvas.GetSize()))
		for schedule in schedules:
			print schedule.limitTime
			g = self.makeProgressHint(schedule.caption, schedule.limitTime/kTick, progressFactor = .0, color = '#C0C0FF')
			self.canvas.AddObject(g)
			scheduleByGuid[schedule.guid] = [schedule, g]
			if schedule.beginMethod == Schedule.kBeginManually:
				manuallySchedules.append(schedule)
			else: 
				automaticallySchedules.append(schedule)
			if schedule.refGuid != None:
				if schedule.refGuid not in scheduleDependencies:
					scheduleDependencies[schedule.refGuid] = []
				scheduleDependencies[schedule.refGuid].append(schedule.guid)
		for schedule in manuallySchedules:
			sc, g = scheduleByGuid[schedule.guid]
			lb, rt = g.BoundingBox
			left, bottom = lb
			right, top = rt
			print left, bottom, right, top
			print screenTopLeft, screenBottomRight
			g.Move(screenTopLeft)
			self.updateFollowedSchedule(schedule.guid, scheduleByGuid, scheduleDependencies)


	def updateFollowedSchedule(self, scheduleGuid, schedules, dependencies):
		refSchedule, refGroup = schedules[scheduleGuid]
		groupBBox = refGroup.BoundingBox
		lb, rt = groupBBox
		left, bottom = lb
		right, top = rt
		if refSchedule.guid in dependencies:
			for depGuid in dependencies[refSchedule.guid]:
				dependSchedule, dependGroup = schedules[depGuid]
				#dependGroup.Move((right, bottom))
				self.adjustDependentPos(dependSchedule, dependGroup, refSchedule, refGroup, bottom)
				right, _0 = dependGroup.BoundingBox[1]
				_0, bottom = dependGroup.BoundingBox[0]
				_1 = self.updateFollowedSchedule(depGuid, schedules, dependencies)
				left, bottom = _1[0]
				right, top = _1[1]
		return [groupBBox[0], [right, top]]

	def adjustDependentPos(self, depSch, depGrp, refSch, refGrp, top):
		"""
		如何确定一个依赖于其他议程的议程的起点？
		  首先，我们需要知道他的依赖项，接着，我们可以计算出它开始的相对时间，如果它是开始于某个议程开始之后，那么它开始的时间的原点就是它所依赖的议程的开始的时间点，否则，就是结束的时间点。有了这个参考点之后，我们还需要知道
		"""
		refSec = depSch.refTime
		refProgress = refGrp.ObjectList[0]
		refLimit = refGrp.ObjectList[1]
		l, b = refProgress.BoundingBox[0]
		r, t = refProgress.BoundingBox[1]
		w = r - l
		ll, lb = refLimit.BoundingBox[0]
		lr, lt = refLimit.BoundingBox[1]
		lw = lr - ll
		passedSecs = w * kTick
		limitSecs = lw * kTick
		refUnits = refSec / kTick
		if depSch.startPoint == Schedule.kBeginAfterStart:
			left = l + refUnits
		elif depSch.startPoint == Schedule.kBeginAfterFinish:
			left = max(lr, r) + refUnits
		if left < refGrp.BoundingBox[1][0]:
			top = min(refGrp.BoundingBox[0][1], top)
		depGrp.Move((left, top))
		pass


	def makeProgressHint(self, text, width = 200, height = 5, progressFactor = 1.0, color = 'red'):
		t = FloatCanvas.ScaledTextBox(text, (0, 0), 12, LineColor = None)
		bl, tr = t.BoundingBox
		#width = tr[0] - bl[0]
		#height = tr[1] - bl[1]
		r = FloatCanvas.Rectangle((bl[0], bl[1] - height), (width * progressFactor, height), LineColor = None, FillColor = color)
		progressBounding = FloatCanvas.Rectangle((bl[0], bl[1] - height), (width, height))
		g = FloatCanvas.Group([r, progressBounding, t])
		return g

	def schedulesCount(self):
		return len(self.schedules)
	def scheduleName(self, index):
		return self.schedules[index].caption
	def scheduleGuid(self, index):
		return self.schedules[index].guid
	def onCreateSecheduleElement(self, ev):
		dlg = ScheduleElementDlg(self)
		dlg.scheduleEditor.schedulesCount = self.schedulesCount
		dlg.scheduleEditor.scheduleNameAtIndex = self.scheduleName
		dlg.scheduleEditor.scheduleUuidAtIndex = self.scheduleGuid

		schedule = Schedule()
		schedule.beginTime = DateTime.Now().GetTicks()
		dlg.scheduleEditor.setSchedule(schedule)
		if ID_OK != dlg.ShowModal():
			return
	def onEditSecheduleElement(self, ev):
		dlg = ScheduleElementDlg(self)
		dlg.scheduleEditor.schedulesCount = self.schedulesCount
		dlg.scheduleEditor.scheduleNameAtIndex = self.scheduleName
		dlg.scheduleEditor.scheduleUuidAtIndex = self.scheduleGuid

		schedule = Schedule()
		schedule.beginTime = DateTime.Now().GetTicks()
		dlg.scheduleEditor.setSchedule(schedule)
		if ID_OK != dlg.ShowModal():
			return

if __name__ == '__main__':
	app = wx.App(redirect = False)
	#app = wx.App()
	a = ScheduleTimer()
	a.Show()
	app.MainLoop()
