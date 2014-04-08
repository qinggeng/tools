#-*-coding:utf-8-*-
import time
import wx
import wx.lib.newevent
import functools
import win32con
import threading
import win32file
import win32event
import notificationParser
partition = lambda xs, p: reduce(lambda (a, b), c: p(c) and (a + [c], b) or (a, b + [c]), xs, ([], []))
kPanelSpacing = 2
kMarginRight = 20
kMarginTop = 20
NotificationEvent, EVT_NOTIFICATION = wx.lib.newevent.NewEvent()
class NtEvt(NotificationEvent):
	def __init__(self):
		NotificationEvent.__init__(self)
		self.notification = None

NoMoreNotifications, EVT_NO_MORE_NOTIFICATION = wx.lib.newevent.NewEvent()

def monitorMailSlot(commands):
	slot = win32file.CreateMailslot(r'\\.\mailslot\notificationCenter', 100, 1, None)
	while commands['next'] == 'continue':
		try:
			maxMsgSize, nextMsgSize, msgCount, timeout = win32file.GetMailslotInfo(slot)
			while msgCount != 0:
				buf = win32file.AllocateReadBuffer(nextMsgSize + 1)
				actualSize, msg = win32file.ReadFile(slot, buf)
				wnd = commands['center']
				evt = NtEvt()
				evt.notification = str(buf)
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
		notification = notificationParser.parseNotification(notification)
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
			panel.Destroy()
			self.notificationRemoved(theNotification)
		panel = wx.Panel(self)
		panel.SetSize((width, height))
		panel.Move((panelWidth - width - kMarginRight, kMarginTop))
		self.livedNotificaitons.append((notification, panel))
		closeBtn = self.presentNotification(notification, panel)
		closeBtn.Bind(wx.EVT_BUTTON, functools.partial(self.panelWillClose, self.livedNotificaitons[-1]))
		self.updateNotificationLayout()
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
		if len(self.livedNotificaitons) == 0:
			wx.PostEvent(self.GetParent(), NoMoreNotifications())
			return
		for notification, panel in reversed(self.livedNotificaitons):
			x, y = panel.GetPosition()
			w, h = panel.GetSize()
			panel.Move((x, yPos))
			yPos = yPos + h + kPanelSpacing

def panelSize(notification, refSize):
	return (300, 60)

def createNotification(notification, panel):
	kMarginTop = 5
	kMarginLeft = 5
	kIconWidth = 24
	kIconHeight = 24
	kIconSize = (kIconWidth, kIconHeight)
	if 'background' in notification:
		background = notification['background']
	else:
		background = '#FFFFFF'
	font = panel.GetFont()
	font.SetPointSize(12)
	panel.SetFont(font)
	panel.SetBackgroundColour(background)
	st = wx.StaticText(panel)
	st.SetLabel(notification['content'])
	st.Wrap(panel.GetSize().width - kIconHeight)
	print st.GetSize()
	panelSize = panel.GetSize()
	panelSize.height = st.GetSize().height + kMarginTop * 2
	panel.SetSize(panelSize)
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
	btn.SetBackgroundColour(background)
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

class NotificationCenter(wx.Frame):
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
		self.Bind(EVT_NO_MORE_NOTIFICATION, self.onNoMoreNotifications)
		self.Hide()
	def onNotification(self, ev):
		self.stack.pushNotification(ev.notification)
		self.Show()

	def onNoMoreNotifications(self, ev):
		self.Hide()
	def onMinimize(self, ev):
		self.Hide()

	def onClose(self, ev):
		self.tbIcon.RemoveIcon()
		self.tbIcon.Destroy()
		self.Destroy()
	def onQuit(self, ev):
		self.onMinimize(ev)
	def onEsc(self, ev):
		self.minimize()
	def minimize(self):
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
	f = NotificationCenter()
	commands = dict()
	commands['next'] = "continue"
	commands["center"] = f
	t = threading.Thread(target = monitorMailSlot, args = (commands,))
	t.start()
	f.stack.pushNotification(u'''{notification: {content: "
　　　　　春江花月夜
春江潮水连海平，海上明月共潮生。
滟滟随波千万里，何处春江无月明![1]
江流宛转绕芳甸，月照花林皆似霰。
空里流霜不觉飞，汀上白沙看不见。
江天一色无纤尘，皎皎空中孤月轮。
江畔何人初见月？江月何年初照人？
人生代代无穷已，江月年年望相似。
不知江月待何人，但见长江送流水。
白云一片去悠悠，青枫浦上不胜愁。
谁家今夜扁舟子？何处相思明月楼？
可怜楼上月徘徊，应照离人妆镜台。
玉户帘中卷不去，捣衣砧上拂还来。
此时相望不相闻，愿逐月华流照君。
鸿雁长飞光不度，鱼龙潜跃水成文。
昨夜闲潭梦落花，可怜春半不还家。
江水流春去欲尽，江潭落月复西斜。
斜月沉沉藏海雾，碣石潇湘无限路。
不知乘月几人归，落月摇情满江树。[2]
	"}, {background: "#FFFF00"}}''')
	a.MainLoop()
	commands['next'] = 'stop' 

if __name__ == '__main__':
	showAlert()
