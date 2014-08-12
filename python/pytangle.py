#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys, os, os.path
import re
import argparse
ap = argparse.ArgumentParser(description='notangle python version, to solve stupid indent problem')
ap.add_argument('-R', '--root', action = 'store', nargs = 1, required = True, help = 'root chunk name for tangling', dest='root')
ap.add_argument('-L', '--line-directive', action = 'store', nargs = 1, help = 'form of line directive', dest='directiveFormat', default='')
ap.add_argument('nw_file', nargs='?')
"""
doc:
	transition:
		event: chunk begin
		dest: chunking
chunking:
	onEnter:
		set chunkName
	onExit:
		make chunk
	transition:
		event: line
		dest: internal
		action:
			check chunk ref
	transition:
		event: chunk end
		dst: doc
	transition:
		chunk begin
		dst: chunking
"""
class Chunks():
	def __init__(self):
		self.chunkList = {}
		self.currentBlock = {}
		pass
	def startChunk(self, line, lineNo):
		chunkPattern = re.compile(r'<<(.+)>>=[\b\t]*$')
		m = chunkPattern.match(line)
		chunkName = m.group(1)
		chunks = self.chunkList
		if chunkName not in chunks:
			chunks[chunkName] = []
		chunk = chunks[chunkName]
		self.currentChunk = chunkName
		block = {}
		block['begin'] = lineNo
		block['ref'] = []
		chunk.append(block)
		self.currentBlock = block

	def endChunk(self, line, lineNo):
		self.currentBlock['end'] = lineNo

	def processSource(self, line, lineNo):
		chunkRef = re.compile(r'([\b\t]*)<<(.+)>>')
		m = chunkRef.match(line)
		if m == None:
			return
		indent = m.group(1)
		name = m.group(2)
		self.currentBlock['ref'].append((lineNo, indent, name))

def generateChunk(chunkName, chunks, lines, nwFileName = '', lineFormat = '', indent = ''):
	chunk = chunks[chunkName]
	for block in chunk:
		if len(lineFormat) != 0:
			directive = lineFormat.replace('%L', str(block['begin'])).replace('%F', nwFileName).replace(r'%N', '')
			print indent + directive
		for lineNo in xrange(block['begin'] + 1, block['end']):
			chunkRef = re.compile(r'([\b\t]*)<<(.+)>>')
			m = chunkRef.match(lines[lineNo])
			if m == None:
				print indent + lines[lineNo][:-1]
			else:
				generateChunk(m.group(2), chunks, lines, nwFileName, lineFormat, indent + m.group(1))
			
def tangle(options):
	f = open(options.nw_file, 'r')
	lines = list(f)
	f.close()
	chunkBegin = re.compile(r'^<<.+>>=(\b|\t)*$')
	chunkEnd = re.compile(r'^@(\b|\t)*$')
	chunkRef = re.compile(r'<<.+>>')
	state = 'doc'
	chunks = Chunks()
	for line, lineNo in zip(lines, xrange(len(lines))):
		if state == 'doc':
			if None != chunkBegin.match(line):
				state = 'chunking'
				#on enter chunking: add chunk
				chunks.startChunk(line, lineNo)
		elif state == 'chunking':
			if None != chunkBegin.match(line):
				state = 'chunking'
				#on exit chunking: end currentChunk
				chunks.endChunk(line, lineNo)
				#on enter chunking: add chunk
				chunks.startChunk(line, lineNo)
			elif None != chunkEnd.match(line):
				state = 'doc'
				#on exit chunking: end currentChunk
				chunks.endChunk(line, lineNo)
			else:
				#on line transition: process line
				chunks.processSource(line, lineNo)
	generateChunk(options.root[0], chunks.chunkList, lines, os.path.basename(options.nw_file), options.directiveFormat[0])

if __name__ == '__main__':
	options = ap.parse_args()
	#options = ap.parse_args(['-R', 'LineDirective.py', '-L', '#%L, %F%N', ur'literatePython\使用noweb对python进行文学编程.nw'.encode('utf-8')])
	tangle(options)
