#-*-coding:utf-8-*-
import time
import wx
import wx.lib.newevent
import functools
import win32con
import threading
import winsys
import win32file
import win32event
partition = lambda xs, p: reduce(lambda (a, b), c: p(c) and (a + [c], b) or (a, b + [c]), xs, ([], []))
kPanelSpacing = 2
kMarginRight = 20
kMarginTop = 20
NotificationEvent, EVT_NOTIFICATION = wx.lib.newevent.NewEvent()
class NtEvt(NotificationEvent):
	def __init__(self):
		NotificationEvent.__init__(self)
		self.notification = None

def monitorMailSlot(commands):
	slot = win32file.CreateMailslot(r'\\.\mailslot\notificationCenter', 0, 1, None)
	while commands['next'] == 'continue':
		try:
			maxMsgSize, nextMsgSize, msgCount, timeout = win32file.GetMailslotInfo(slot)
			while msgCount != 0:
				buf = win32file.AllocateReadBuffer(nextMsgSize + 1)
				actualSize, msg = win32file.ReadFile(slot, buf)
				wnd = commands['center']
				evt = NtEvt()
				evt.notification = str(buf)
				print "send event to ", wnd
				wx.PostEvent(wnd, evt)
				maxMsgSize, nextMsgSize, msgCount, timeout = win32file.GetMailslotInfo(slot)
		except Exception, e:
			print "exception:", e
			pass
	slot.close()

class NotificationStack(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.SetBackgroundColour((0, 0, 0, 255))
		self.livedNotificaitons = []
		self.notificationPanelSize = None
		self.notificationRemoved = None
		self.presentNotification = None
	def onNotification(self, ev):
		notification = ev.notification
		self.pushNotification(notification)
	def pushNotification(self, notification):
		if None == self.notificationPanelSize:
			return
		width, height = self.notificationPanelSize(notification, self.GetSize())
		tail = 0
		panelWidth, panelHeight = self.GetSize()
		for theNotification, panel in self.livedNotificaitons:
			tail = tail + 1
			pos = panel.GetPosition()
			pos.y = pos.y + height + kPanelSpacing
			if pos.y >= panelHeight:
				break
			panel.Move(pos)
		while len(self.livedNotificaitons) < tail:
			theNotification, panel = self.livedNotificaitons.pop()
			self.RemoveChild(panel)
			self.notificationRemoved(theNotification)
		panel = wx.Panel(self)
		panel.SetSize((width, height))
		panel.Move((panelWidth - width - kMarginRight, kMarginTop))
		self.livedNotificaitons.append((notification, panel))
		closeBtn = self.presentNotification(notification, panel)
		closeBtn.Bind(wx.EVT_BUTTON, functools.partial(self.panelWillClose, self.livedNotificaitons[-1]))
		print panel.GetSize()
		print panel.GetPosition()
		print self.GetSize()
		self.Refresh()
		
	def calcNotificationRect(self, w, h):
		pass
	
	def panelWillClose(self, traits, ev):
		notification, panel = traits
		panel.Destroy()
		self.livedNotificaitons.remove(traits)
		self.updateNotificationLayout()
	
	def updateNotificationLayout(self):
		yPos = kMarginTop
		for notification, panel in reversed(self.livedNotificaitons):
			x, y = panel.GetPosition()
			w, h = panel.GetSize()
			panel.Move((x, yPos))
			yPos = yPos + h + kPanelSpacing
		pass

def panelSize(notification, refSize):
	return (300, 60)

def createNotification(notification, panel):
	kMarginTop = 5
	kMarginLeft = 5
	kIconWidth = 24
	kIconHeight = 24
	kIconSize = (kIconWidth, kIconHeight)
	panel.SetBackgroundColour((255, 255, 255, 255))
	st = wx.StaticText(panel)
	st.SetLabel(notification)
	vsz = wx.BoxSizer(wx.VERTICAL)
	vsz.Add((-1, kMarginTop))
	sz = wx.BoxSizer(wx.HORIZONTAL)
	sz.Add((kMarginLeft, -1))
	vsz.Add(sz, proportion = 0)
	panel.SetSizer(vsz)
	sz.Add(st, proportion = 0, flag = wx.EXPAND|wx.LEFT|wx.RIGHT)
	img = wx.Image("check.png")
	img.LoadFile("check.png", wx.BITMAP_TYPE_PNG)
	img = img.Scale(kIconWidth, kIconHeight)
	bmp = wx.BitmapFromImage(img)
	btn = wx.BitmapButton(panel, style = 0)
	btn.SetBitmapLabel(bmp)
	btn.SetSize(kIconSize)
	width, height = panel.GetSize()
	btn.Move((width - kIconWidth - kMarginLeft, kMarginTop))

	panel.Layout()
	return btn

def notificationRemoved(notification):
	pass

class CustomTaskBarIcon(wx.TaskBarIcon):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, frame):
		"""Constructor"""
		wx.TaskBarIcon.__init__(self)
		self.frame = frame
 
		img = wx.Image("appbar.speakerphone.png", wx.BITMAP_TYPE_ANY)
		img = img.Scale(24, 24)
		bmp = wx.BitmapFromImage(img)
		self.icon = wx.EmptyIcon()
		self.icon.CopyFromBitmap(bmp)
 
		self.SetIcon(self.icon, "Restore")
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
 
	#----------------------------------------------------------------------
	def OnTaskBarActivate(self, evt):
		""""""
		pass
 
	#----------------------------------------------------------------------
	def OnTaskBarClose(self, evt):
		"""
		Destroy the taskbar icon and frame from the taskbar icon itself
		"""
		self.frame.Close()
 
	#----------------------------------------------------------------------
	def OnTaskBarLeftClick(self, evt):
		"""
		Create the right-click menu
		"""
		self.frame.Show()

class BrutalAlert(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, parent = None, title = u'粗鲁闹钟', style = wx.STAY_ON_TOP)
		self.layout()
		self.ShowFullScreen(wx.FULLSCREEN_NOMENUBAR)
		self.escID = wx.NewId()
		#self.RegisterHotKey(self.escID, 0, win32con.VK_ESCAPE)
		self.Bind(wx.EVT_HOTKEY, self.onEsc, id = self.escID)
		testID = wx.NewId()
		self.Bind(wx.EVT_MENU, self.onQuit, id = testID)
		accel = wx.AcceleratorTable([(wx.ACCEL_NORMAL, ord('q'), testID)])
		self.SetAcceleratorTable(accel)
		self.tbIcon = CustomTaskBarIcon(self)
 
		self.Bind(wx.EVT_ICONIZE, self.onMinimize)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(EVT_NOTIFICATION, self.onNotification)
		self.Hide()
	def onNotification(self, ev):
		self.stack.pushNotification(ev.notification)
		self.Show()
	def onMinimize(self, ev):
		self.Hide()

	def onClose(self, ev):
		self.tbIcon.RemoveIcon()
		self.tbIcon.Destroy()
		self.Destroy()
	def onQuit(self, ev):
		print "will quit"
		self.onMinimize(ev)
	def onEsc(self, ev):
		self.minimize()
	def minimize(self):
		print "minimized"
		quit()
	def layout(self):
		sz = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(sz)
		notificationStack = NotificationStack(self)
		notificationStack.notificationPanelSize = panelSize
		notificationStack.presentNotification = createNotification
		notificationStack.notificationRemoved = notificationRemoved
		self.stack = notificationStack
		sz.Add(notificationStack, proportion = 1, flag = wx.EXPAND|wx.ALL)
def showAlert():
	a = wx.App(redirect = False)
	f = BrutalAlert()
	commands = dict()
	commands['next'] = "continue"
	commands["center"] = f
	t = threading.Thread(target = monitorMailSlot, args = (commands,))
	t.start()
	a.MainLoop()
	commands['next'] = 'stop' 

if __name__ == '__main__':
	showAlert()
