#-*- coding: utf-8 -*-
from ptk.parser import LRParser, production, leftAssoc, nonAssoc
from ptk.lexer import ReLexer, token
from fraction import Fraction
from matrix import Matrix
from traceback import format_exc as fme
kRow = 'row'
kElement = 'element'
kMatrix = 'matrix'
class ParserContext(object):
	def __init__(self):
		self.unnamedVariables_ = []

	@property
	def unnamedVariables(self):
		return self.unnamedVariables_

	@unnamedVariables.setter
	def unnamedVariables(self, val):
		self.unnamedVariables_ = val

@leftAssoc('+', '-')
@leftAssoc('*', '/')
@nonAssoc('UNARYMINUS') 
class Parser(LRParser, ReLexer):
	def __init__(self):
		LRParser.__init__(self)
		ReLexer.__init__(self)
		self.stack = []

	@token('[1-9][0-9]*')
	def number(self, tok):
		tok.value = int(tok.value)

	@token(r'\$[0-9a-zA-Z_]+')
	def namedVariable(self, tok):
		tok.value = 'variable'

	@production('Expr -> "-" Expr<e>', priority = 'UNARYMINUS')
	def minusExpr(self, e):
		return -1 * e

	@production('Expr -> Expr<l> "+" Expr<r>')
	def binaryAdd(self, l, r):
		return l + r

	@production('Expr -> Expr<l> "-" Expr<r>')
	def binaryMinus(self, l, r):
		return l - r

	@production('Expr -> Expr<l> "*" Expr<r>')
	def binaryMul(self, l, r):
		return l * r
		
	@production('Expr -> Matrix<m> | Factor<f>')
	def expr(self, m = None, f = None):
		if m != None:
			return m
		elif f != None:
			return f

	@production('Factor -> Num<val>')
	def factor(self, val):
		return val

	@production('Matrix -> "[" Row<first> Rows*<rest> "]"')
	def matrix(self, first, rest = None):
		return Matrix([first] + rest)
	
	@production('Rows -> "," Row<row>')
	def rows(self, row):
		return row

	@production('Row -> E+<vals>')
	def row(self, vals):
		return vals

	@production('E -> Num<val>')
	def elem(self, val):
		self.stack.append((kElement, val))
		return val

	@production('Num -> Int<val> | Frac<val>')
	def Num(self, val):
		return val

	@production('Int -> number<val>')
	def Int(self, val):
		return val

	@production('Frac -> Expr<n> "/" Expr<d>')
	def Frac(self, n, d):
		return Fraction(n, d)


	def newSentence(self, sentence):
		print 'newSentence:', sentence
		self.ret = sentence
		return sentence
if __name__ == '__main__':
	c = Parser()
	c.parse('1+2')
	assert c.ret == 3
	c.parse('[1/3 2, 3 4]')
	assert c.ret == Matrix([[Fraction(1, 3), 2], [3, 4]])
	print c.parse('1')
	print c.parse('-1')
	print c.parse('-[-1/3 2, 3 4]')
	print c.parse('1/2')
	print c.parse('-1/2')
	print c.parse('-1/2 + 1')
	print c.parse('-1/2 + 1')
	print c.parse('-1/2 - 1')
	print c.parse('-1/2 + 1/3')
	print c.parse('-1/2 - 1/3')
	print c.parse('1/2 - 1/3')
	print c.parse('-1/2 * 1')
	print c.parse('1 * 1/2')
	print c.parse('1/2 * 1/2')
	#TODO running tests
	pass
