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

	@property
	def context(self):
		return self.context_
	@context.setter
	def context(self, val):
		self.context_ = val

	@token('[1-9][0-9]*')
	def number(self, tok):
		tok.value = int(tok.value)

	@token(r'\$[0-9a-zA-Z_]+')
	def positionalVariable(self, tok):
		variableIndex = int(tok.value[1:]) - 1
		tok.value = self.context.unnamedVariables[variableIndex]

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

	@production('Variable -> positionalVariable<v>')
	def variable(self, v):
		return v
		
	@production('Expr -> Matrix<m> | Factor<f> | Variable<v>')
	def expr(self, m = None, f = None, v = None):
		if m != None:
			return m
		elif f != None:
			return f
		elif v != None:
			return v

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
		self.ret = sentence
		return sentence
if __name__ == '__main__':
	c = Parser()
	c.parse('1+2')
	assert c.ret == 3
	c.parse('[1/3 2, 3 4]')
	assert c.ret == Matrix([[Fraction(1, 3), 2], [3, 4]])
	c.parse('1')
	assert c.ret == 1
	c.parse('-1')
	assert c.ret == -1
	c.parse('-[-1/3 2, 3 4]')
	assert c.ret == -1 * Matrix([[Fraction(-1, 3), 2], [3, 4]])
	c.parse('1/2')
	assert c.ret == Fraction(1, 2)
	c.parse('-1/2')
	assert c.ret == Fraction(-1, 2)
	c.parse('-1/2 + 1')
	assert c.ret == Fraction(-1, 2) + 1
	c.parse('-1/2 - 1')
	assert c.ret == Fraction(-1, 2) - 1
	c.parse('-1/2 + 1/3')
	assert c.ret == Fraction(-1, 2) + Fraction(1, 3)
	c.parse('-1/2 - 1/3')
	assert c.ret == Fraction(-1, 2) - Fraction(1, 3)
	c.parse('1/2 - 1/3')
	assert c.ret == Fraction(1, 2) - Fraction(1, 3)
	c.parse('-1/2 * 1')
	assert c.ret == Fraction(-1, 2)
	c.parse('1 * 1/2')
	assert c.ret == Fraction(1, 2)
	c.parse('1/2 * 1/2')
	assert c.ret == Fraction(1, 4)
	unnamedVariables = [1, 2, 3, Fraction(1, 2), Matrix([[1, 2], [3, 4]])]
	context = ParserContext()
	context.unnamedVariables = unnamedVariables
	c.context = context
	c.parse('$1')
	assert c.ret == 1
	c.parse('$2')
	assert c.ret == 2
	c.parse('$3')
	assert c.ret == 3
	c.parse('$4')
	assert c.ret == Fraction(1, 2)
	c.parse('$5')
	assert c.ret == Matrix([[1, 2], [3, 4]])
	c.parse('$1 + $2')
	assert c.ret == 3
	#TODO running tests
