#-*- coding: utf-8 -*-
from ptk.parser import LRParser, production, leftAssoc, nonAssoc
from ptk.lexer import ReLexer, token
from fraction import Fraction
kRow = 'row'
kElement = 'element'
kMatrix = 'matrix'
class Parser(LRParser, ReLexer):
	def __init__(self):
		LRParser.__init__(self)
		ReLexer.__init__(self)
		self.stack = []
	@token('[1-9][0-9]*')
	def number(self, tok):
		tok.value = int(tok.value)

	@production('Matrix -> "[" Row<first> Rows*<rest> "]"')
	def matrix(self, first, rest = None):
		print first
		print rest
		return [first] + rest
	
	@production('Rows -> "," Row<row>')
	def rows(self, row):
		return row

	@production('Row -> E+<vals>')
	def row(self, vals):
		return vals

	@production('E -> Num<val>')
	def expr(self, val):
		self.stack.append((kElement, val))
		return val

	@production('Num -> Int<val> | Frac<val>')
	#@production('Num -> Int<val>')
	def Num(self, val):
		print 'Num:', val
		return val

	@production('Int -> number<val>')
	def Int(self, val):
		return val

	@production('Frac -> Int<n> "/" Int<d>')
	def Frac(self, n, d):
		return Fraction(n, d)


	def newSentence(self, sentence):
		print 'newSentence:', sentence
		return sentence
if __name__ == '__main__':
	c = Parser()
	print c.parse('[1/3 2, 3 4]')
	#TODO running tests
	pass
