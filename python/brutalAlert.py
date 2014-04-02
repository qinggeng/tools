#-*-coding:utf-8-*-
import wx
import functools
import win32con
partition = lambda xs, p: reduce(lambda (a, b), c: p(c) and (a + [c], b) or (a, b + [c]), xs, ([], []))
kPanelSpacing = 2
kMarginRight = 20
kMarginTop = 20
class NotificationStack(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.SetBackgroundColour((0, 0, 0, 255))
		self.livedNotificaitons = []
		self.notificationPanelSize = None
		self.notificationRemoved = None
		self.presentNotification = None
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
		panel.Hide()
		self.RemoveChild(panel)
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

class BrutalAlert(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, parent = None, title = u'粗鲁闹钟', style = wx.STAY_ON_TOP)
		self.layout()
		self.ShowFullScreen(wx.FULLSCREEN_NOMENUBAR)
		self.stack.pushNotification(u"hello world")
		self.stack.pushNotification(u"hello world2")
		self.stack.pushNotification(u"hello world3")
		self.escID = 100
		self.RegisterHotKey(self.escID, 0, win32con.VK_ESCAPE)
		self.Bind(wx.EVT_HOTKEY, self.onEsc, id = self.escID)
	def onEsc(self, ev):
		self.minimize()
	def minimize(self):
		print "minimized"
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
	a.MainLoop()
if __name__ == '__main__':
	showAlert()