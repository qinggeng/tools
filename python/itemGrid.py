#-*- coding: utf-8 -*-
import wx
import pickle
import functools
import wx.lib.newevent
from collections import namedtuple
ItemDisplayTraits = namedtuple('ItemDisplayTraits', ['index', 'rect', 'panel'])
ItemDragTraits = namedtuple('ItemDragTraits', ['index', 'dragPoint'])
ItemPanelCloseEvent, EVT_ITEM_PANEL_CLOSED = wx.lib.newevent.NewEvent()
class ItemDropTarget(wx.PyDropTarget):
	def __init__(self, targetWnd):
		wx.PyDropTarget.__init__(self)
		tdo = wx.CustomDataObject('itemPanel')
		self.SetDataObject(tdo)
		self.target = targetWnd

	def OnEnter(self, x, y, d):
		if hasattr(self.target, 'onDragIn'):
			self.target.onDragIn(x, y, d)
		return d
	
	def OnLeave(self):
		if hasattr(self.target, 'onDragOut'):
			self.target.onDragOut()
		pass
	
	def OnDragOver(self, x, y, d):
		if hasattr(self.target, 'onDragOver'):
			self.target.onDragOver(x, y, d)
		return d
	
	def OnData(self, x, y, dropAction):
		tdo = wx.CustomDataObject('itemPanel')
		self.GetData()
		data = self.GetDataObject().GetDataHere(tdo.GetFormat())
		if hasattr(self.target, 'onDragData'):
			self.target.onDragData(x, y, dropAction, data)
		return dropAction
class ItemGrid(wx.ScrolledWindow):
	def __init__(self, 
			parent, 
			id = -1, 
			pos = wx.DefaultPosition, 
			size = wx.DefaultSize, 
			style = wx.TAB_TRAVERSAL | wx.NO_BORDER | wx.HSCROLL, 
			name = wx.PanelNameStr):
		wx.ScrolledWindow.__init__(self, parent, id, pos, size, style, name)
		self.SetBackgroundColour('#FFFFFF')
		self.columnWidth = 200
		self.minimumItemHeight = 80
		self.horizontalMargin = 1
		self.verticalMargin = 1
		self.verticalPadding = 15
		self.SetScrollbars(1, 1, 1, 1)
		self.livedPanels = []
		self.Bind(wx.EVT_SCROLLWIN, self.onScroll)
		self.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.onScrollTrackThumb)
		self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.onScrollRealseThumb)
		self.Bind(wx.EVT_SCROLLWIN_TOP, self.onScrollTop)
		self.Bind(wx.EVT_SCROLLWIN_BOTTOM, self.onScrollBottom)
		self.Bind(wx.EVT_SCROLLWIN_PAGEUP, self.onScrollPageUp)
		self.Bind(wx.EVT_SCROLLWIN_PAGEDOWN, self.onScrollPageDown)
		self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.onScrollLineUp)
		self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.onScrollLineDown)
		dt = ItemDropTarget(self)
		self.SetDropTarget(dt)
		"""data callbacks"""
		self.itemCount = None
		self.itemDesiredHeight = None
		self.prepareItemPanel = None
		self.disposeItemPanel = None
		self.willSwap = None
	
	def refresh(self):
		viewportWidth, viewportHeight = self.GetSize()
		#print viewportWidth, viewportHeight
		scrollLength = self.calculateScrollLength(viewportHeight)
		self.SetVirtualSize((scrollLength, viewportHeight - self.verticalPadding * 2))
		self.showItems()

	def calculateScrollLength(self, viewportHeight):
		if self.itemCount == None or self.itemDesiredHeight == None:
			return
		itemWidth = self.columnWidth - self.horizontalMargin
		count = self.itemCount()
		length = 200
		reservedHeight = viewportHeight - self.verticalMargin * 2
		for index in range(count):
			wantedHeight = self.itemDesiredHeight(index, itemWidth, reservedHeight)
			itemHeight = max(self.minimumItemHeight, min(wantedHeight, reservedHeight))
			reservedHeight -= itemHeight
			if reservedHeight < self.minimumItemHeight:
				reservedHeight = viewportHeight - self.verticalMargin * 2
				if index < count - 1:
					length += self.columnWidth
		return length
	
	def showItems(self):
		if self.itemCount == None or self.itemDesiredHeight == None or self.prepareItemPanel == None:
			return
		itemCount = self.itemCount()
		if 0 == itemCount:
			return
		viewportWidth, viewportHeight = self.GetSize()
		contentHeight = viewportHeight - self.verticalPadding * 2
		panels = self.livedPanels
		if len(panels) == 0:
			originY = self.verticalPadding
			originX = self.horizontalMargin
			itemPanel = self.drawItem(0, contentHeight)
			itemPanel.SetPosition((originX, originY))
			panels.append(ItemDisplayTraits(rect = itemPanel.GetRect(), index = 0, panel = itemPanel))
		self.updateGrid(0)

	def drawItem(self, itemIndex, reservedHeight):
		itemWidth = self.columnWidth - self.horizontalMargin
		wantedHeight = self.itemDesiredHeight(itemIndex, itemWidth, reservedHeight)
		itemHeight = max(self.minimumItemHeight, min(wantedHeight, reservedHeight))
		itemPanel = wx.Panel(self)
		dragPanel = wx.Panel(itemPanel)
		dragPanel.SetSize((-1, 10))
		dragPanel.SetBackgroundColour('#FFFF00')
		contentPanel = wx.Panel(itemPanel)
		sz = wx.BoxSizer(wx.VERTICAL)
		itemPanel.SetSizer(sz)
		sz.Add(dragPanel, proportion = 0, flag = wx.EXPAND | wx.Left | wx.RIGHT)
		sz.Add(contentPanel, proportion = 1, flag = wx.EXPAND | wx.ALL)
		itemPanel.SetSize((itemWidth, itemHeight))
		self.prepareItemPanel(contentPanel, itemIndex)
		dragPanel.Bind(wx.EVT_LEFT_DOWN,  functools.partial(self.startDragItem, itemPanel, itemIndex))
		return itemPanel
	
	def startDragItem(self, panel, index, ev):
		ds = wx.DropSource(panel)
		tdo = wx.CustomDataObject('itemPanel')
		#print ev.GetPosition()
		#print "{0}({1}) start dragging".format(index, panel)
		for dispIndex in range(len(self.livedPanels)):
			traits = self.livedPanels[dispIndex]
			if traits.panel == panel:
				index = dispIndex
		tdo.SetData(pickle.dumps(ItemDragTraits(index = index, dragPoint = ev.GetPosition())))
		ds.SetData(tdo)
		dragResult = ds.DoDragDrop(wx.Drag_DefaultMove)
		#print dragResult
	
	def prepareDisplayRange(self):
		x, y = self.GetViewStart()
		viewportWidth, viewportHeight = self.GetSize()
		scrollWidth, scrollHeight = self.GetVirtualSize()
		left = max(0, x - viewportWidth * 1)
		right = min(scrollWidth, x + viewportWidth * 2)
		return (left, right)

	def itemDeleted(self, index):
		for traits, itemIndex in zip(self.livedPanels, range(len(self.livedPanels))):
			if traits.index == index:
				index = itemIndex
				break
		for traits in self.livedPanels[itemIndex:]:
			traits.panel.Destroy()
		self.livedPanels = self.livedPanels[:itemIndex]
		self.updateGrid(0)

	def updateGrid(self, offset):
		if len(self.livedPanels) == 0:
			return
		self.Freeze()
		left, right = self.prepareDisplayRange()
		currentLeft = self.livedPanels[0].rect.x
		panels = self.livedPanels
		currentRight = self.livedPanels[-1].rect.x + self.livedPanels[-1].rect.width
		viewportWidth, viewportHeight = self.GetSize()
		originY = self.verticalPadding
		contentHeight = viewportHeight - self.verticalPadding * 2
		"""
		#补全左边缺失的item
		while self.itemCount() > 0 and self.livedPanels[0].rect.left >= left:
			traits = self.livedPanels[0]
			if traits.index == 0:
				break
			reservedHeight = viewportHeight - traits.rect.bottom - self.verticalMargin
			x = traits.rect.left
			y = traits.rect.bottom + self.verticalMargin * 2
			if reservedHeight < self.minimumItemHeight:
				x = traits.rect.left - self.columnWidth - self.horizontalMargin
				y = self.verticalMargin + self.verticalPadding
				reservedHeight = viewportHeight - 30
				itemPanel = self.drawItem(traits.index - 1, reservedHeight)
			else:
				itemPanel = self.drawItem(traits.index - 1, reservedHeight)
				itemWidth, itemHeight = itemPanel.GetSize()
				if itemHeight > reservedHeight:
					x = traits.rect.left - self.columnWidth - self.horizontalMargin
					y = self.verticalMargin + self.verticalPadding
			itemPanel.Move((x - viewportWidth, y))
			print itemPanel.GetRect()
			self.livedPanels.insert(0, ItemDisplayTraits(rect = wx.Rect(x, y, itemPanel.GetRect().width, itemPanel.GetRect().height), index = traits.index - 1, panel = itemPanel))
		#删除左边多余的item
		while len(self.livedPanels) > 0 and self.livedPanels[0].rect.right <= left:
			traits = self.livedPanels[0]
			self.livedPanels.pop(0)
			print "remove item", traits.index
			traits.panel.Destroy()
		"""
		#补全右边缺失的item
		while self.itemCount() > 0 and self.livedPanels[-1].rect.left <= right:
			traits = self.livedPanels[-1]
			if traits.index == self.itemCount() - 1:
				break
			#TODO 首先绘制
			itemPanel = self.drawItem(traits.index + 1, contentHeight)
			#TODO 然后确保其大于等于最小高度
			if itemPanel.GetRect().height < self.minimumItemHeight:
				itemPanel.SetSize((itemPanel.GetRect().width, self.minimumItemHeight))
			#决定放置的位置
			if itemPanel.GetRect().height + traits.panel.GetRect().bottom > contentHeight + originY:
				x = traits.panel.GetRect().right + self.horizontalMargin * 2
				y = originY
			else:
				x = traits.panel.GetRect().left
				y = traits.panel.GetRect().bottom + self.verticalMargin * 2
			itemPanel.SetPosition((x, y))
			panels.append(ItemDisplayTraits(index = traits.index + 1, panel = itemPanel, rect = wx.Rect(x, y, self.columnWidth, itemPanel.GetSize().height)))
			"""
			reservedHeight = viewportHeight - traits.rect.bottom - self.verticalMargin
			x = traits.rect.left
			y = traits.rect.bottom + self.verticalMargin * 2
			if reservedHeight < self.minimumItemHeight:
				x = traits.rect.right + self.horizontalMargin * 2
				reservedHeight = viewportHeight - 30
				y = self.verticalMargin + self.verticalPadding
				itemPanel = self.drawItem(traits.index + 1, reservedHeight)
			else:
				itemPanel = self.drawItem(traits.index + 1, reservedHeight)
				itemWidth, itemHeight = itemPanel.GetSize()
				if itemHeight > reservedHeight:
					x = traits.rect.right + self.horizontalMargin * 2
					y = self.verticalMargin + self.verticalPadding
			itemPanel.Move((max(0, x - self.GetViewStart()[0]), y))
			self.livedPanels.append(ItemDisplayTraits(rect = wx.Rect(x, y, itemPanel.GetRect().width, itemPanel.GetRect().height), index = traits.index + 1, panel = itemPanel))
			"""
		#删除右边多余的item
		while len(self.livedPanels) > 0 and self.livedPanels[-1].rect.left > right:
			traits = self.livedPanels[-1]
			self.livedPanels.pop(-1)
			traits.panel.Destroy()
		self.Thaw()

	def onScroll(self, ev):
		#print u'on scroll:'
		#print self.prepareDisplayRange()
		self.Freeze()
		self.updateGrid(0)
		self.Thaw()
		ev.Skip()

	def onScrollTrackThumb(self, ev):
		#print u'scroll thumb button draging'
		ev.Skip()

	def onScrollRealseThumb(self, ev):
		#print u'scroll thumb button up'
		ev.Skip()

	def onScrollTop(self, ev):
		#print u'on scroll top'
		ev.Skip()

	def onScrollBottom(self, ev):
		#print u'on scroll bottom'
		ev.Skip()

	def onScrollPageUp(self, ev):
		#print u'on page up'
		ev.Skip()

	def onScrollPageDown(self, ev):
		#print u'on page down'
		#print self.GetViewStart()
		ev.Skip()

	def onScrollLineUp(self, ev):
		#print u'on line up'
		ev.Skip()

	def onScrollLineDown(self, ev):
		print u'on line down', ev.GetPosition()
		ev.Skip()

	def onDragIn(self, x, y, d):
		#print "drag in"
		pass

	def onDragOut(self):
		#print "drag out"
		pass

	def onDragOver(self, x, y, d):
		#print "drag over"
		pass

	def onDragData(self, x, y, action, data):
		dragTraits = pickle.loads(data)
		dst = wx.FindWindowAtPoint(self.ClientToScreen((x, y)))
		while dst != None and dst.GetParent() != self:
			dst = dst.GetParent()
		panels = self.livedPanels
		lhs = None
		rhs = None
		print 'will drop ', dragTraits.index
		for index in range(len(panels)):
			if panels[index].panel == dst:
				lhs = index
			if dragTraits.index == panels[index].index:
				rhs = index
		print lhs, rhs
		if lhs != None and rhs != None:
			self.swapItem(lhs, rhs)
		return

	def swapItem(self, lhs, rhs):
		if lhs == rhs:
			print 'swap same, return'
			return
		allowSwap, keepsItemsOrder = self.willSwap(lhs, rhs)
		if False == allowSwap:
			return
		l = self.livedPanels
		#re-position range
		first, last = min(lhs, rhs), max(lhs, rhs)
		pt = l[first].panel.GetPosition()
		l[lhs], l[rhs] = l[rhs], l[lhs]
		if keepsItemsOrder == True:
			firstIndex, secondIndex = l[rhs].index, l[lhs].index
			l[lhs] = ItemDisplayTraits(index = firstIndex, panel = l[lhs].panel, rect = l[lhs].rect)
			l[rhs] = ItemDisplayTraits(index = secondIndex, panel = l[rhs].panel, rect = l[rhs].rect)
			print l[lhs]
			print l[rhs]
		l[first].panel.SetPosition(pt)
		r = l[first].panel.GetRect()
		vpw, vph = self.GetSize()
		contentHeight = vph - self.verticalPadding * 2
		x = r.left
		y = r.bottom + self.verticalMargin * 2
		self.Freeze()
		self.layoutRestItems(first + 1)
		self.Thaw()

	def layoutRestItems(self, refItemIndex):
		refTraits = self.livedPanels[refItemIndex]
		r = refTraits.rect
		vpw, vph = self.GetSize()
		contentHeight = vph - self.verticalPadding * 2
		x = r.left
		y = r.bottom + self.verticalMargin * 2
		originY = self.verticalPadding
		for traits in self.livedPanels[refItemIndex + 1: ]:
			if traits.rect.height + y > contentHeight:
				if (traits.panel.GetRect().left <= x):
					x = traits.panel.GetRect().right + self.horizontalMargin * 2
				else:
					x = traits.panel.GetRect().left
				y = originY
			traits.panel.SetPosition((x, y))
			traits.rect.x = x
			traits.rect.y = y
			y = traits.panel.GetRect().bottom + self.verticalMargin * 2
		
	
	def refreshItem(index):
		l = self.livedPanels
		for displayIndex in range(len(l)):
			traits = l[displayIndex]
			if traits.index == index:
				itemPanel = self.drawItem(index)
				l[displayIndex] = ItemDisplayTraits(index = index, rect = itemPanel.GetRect(), panel = itemPanel)
				layoutRestItems(displayIndex)

if __name__ == '__main__':
	a = wx.App(redirect = False)
	frm = wx.Frame(None)
	frm.SetSize((1200, 720))
	p = ItemGrid(frm)
	sz = wx.BoxSizer(wx.HORIZONTAL)
	frm.SetSizer(sz)
	sz.Add(p, proportion = 1, flag = wx.EXPAND | wx.ALL)
	def fakeItemCount():
		return 420
	def fakeItemHeight(index, width, height):
		return 100 * (1 + 0.00 * index)
	def fakePreparePanel(panel, itemIndex):
		panel.SetBackgroundColour('#808080')
		sz = wx.BoxSizer(wx.VERTICAL)
		panel.SetSizer(sz)
		sz.Add((-1, 10))
		dc = wx.ClientDC(panel)
		brush = dc.GetBrush()
		brush.SetColour('#FFFF00')
		dc.SetBrush(brush)
		r = panel.GetRect()
		dc.DrawRectangle(10, 10, 10, 10)
		st = wx.StaticText(panel)
		sz.Add(st, proportion = 1, flag = wx.EXPAND | wx.ALL)
		st.SetLabel(str(itemIndex))
		ft = st.GetFont()
		ft.SetPointSize(ft.GetPointSize() * 4)
		st.SetFont(ft)
	def fakeSwapHandler(lhs, rhs):
		return (True, True)
	p.itemCount = fakeItemCount
	p.itemDesiredHeight = fakeItemHeight
	p.prepareItemPanel = fakePreparePanel
	p.willSwap = fakeSwapHandler
	frm.Show()
	p.refresh()
	a.MainLoop()
