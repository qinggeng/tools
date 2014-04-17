# -*- coding: gbk -*-
from wx import *
from itemGrid import ItemGrid
kIconHeight = 16
def loadBitmapFromPNGFile(path, bitmapSize):
	img = wx.Image(path)
	img.LoadFile(path, wx.BITMAP_TYPE_PNG)
	factor = 2.4
	img = img.Resize((bitmapSize[0] * factor, bitmapSize[1] * factor), (-20, -20))
	img = img.Scale(bitmapSize[0], bitmapSize[1])
	return wx.BitmapFromImage(img)

class Reminder(Frame):
	def __init__(self):
		Frame.__init__(self, None)
		self.SetTitle(u'提醒和倒计时')
		self.initialLayout()
		self.SetBackgroundColour('#E0E0E0')
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
		alarmsPanel = Panel(self)
		alarmsPanel.SetSize((200, 100))
		alarmsPanel.SetBackgroundColour('#8080FF')
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
		#poolSizer.Add((0, 1))
		alarmsGrid = ItemGrid(poolPanel)
		poolSizer.Add(alarmsGrid, proportion = 1, flag = EXPAND | ALL)

		#poolPanel.SetBackgroundColour('#C0C0C0')
		poolPanel.SetBackgroundColour('#FFFFFF')
		self.Layout()
	
	def initializePoolTools(self, toolsPanel):
		p = toolsPanel
		sz = BoxSizer(HORIZONTAL)
		p.SetSizer(sz)
		createBtn = BitmapButton(p, style = 0)
		createBtn.SetSize((kIconHeight, kIconHeight))
		createBtn.SetBackgroundColour('#FFFFFF')
		createBtn.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.add.png', (kIconHeight, kIconHeight)))
		sz.Add(createBtn, flag = SHAPED)
		sz.Add((2, 2))
		filterBtn = BitmapButton(p, style = 0)
		filterBtn.SetSize((kIconHeight, kIconHeight))
		filterBtn.SetBackgroundColour('#FFFFFF')
		filterBtn.SetBitmapLabel(loadBitmapFromPNGFile(u'appbar.filter.png', (kIconHeight, kIconHeight)))
		sz.Add(filterBtn, flag = SHAPED)
		pass
		
if __name__ == '__main__':
	a = wx.App(redirect = False)
	p = Reminder()
	p.SetSize((800, 600))
	p.Show()
	a.MainLoop()
