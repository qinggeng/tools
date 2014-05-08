# -*- coding: utf-8 -*-
from wx import *
def loadBitmapFromPNGFile(path, bitmapSize):
	img = Image(path)
	img.LoadFile(path, BITMAP_TYPE_PNG)
	img = img.Resize(bitmapSize, ((bitmapSize[0] - img.GetSize()[0]) / 2, (bitmapSize[1] - img.GetSize()[1]) / 2))
	#img = img.Scale(bitmapSize[0], bitmapSize[1])
	return BitmapFromImage(img)

def makeBitmapButton(
		parent,
		size,
		labelPath,
		hoverPath = None,
		pressPath = None):
	label = loadBitmapFromPNGFile(labelPath, size)
	btn = BitmapButton(parent, style = 0)
	btn.SetBitmapLabel(label)
	return btn

