# -*- coding: utf-8 -*-
from wx import *
def loadBitmapFromPNGFile(path, bitmapSize):
	img = Image(path)
	img.LoadFile(path, BITMAP_TYPE_PNG)
	img = img.Resize(bitmapSize, ((bitmapSize[0] - img.GetSize()[0]) / 2, (bitmapSize[1] - img.GetSize()[1]) / 2))
	#img = img.Scale(bitmapSize[0], bitmapSize[1])
	return BitmapFromImage(img), img

def makeBitmapButton(
		parent,
		size,
		labelPath,
		hoverPath = None,
		pressPath = None):
	label, img = loadBitmapFromPNGFile(labelPath, size)
	btn = BitmapButton(parent, style = 0)
	btn.SetBitmapLabel(label)
	if hoverPath == None:
		hoverImg = img.Copy()
		hoverImg.Replace(0, 0, 0, 255, 0, 0)
		btn.SetBitmapHover(BitmapFromImage(hoverImg))
	return btn

