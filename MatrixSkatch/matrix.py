#-*- coding: utf-8 -*-
from fraction import Fraction
class Matrix(object):
	def __init__(self, rows):
		self.rows = rows
	def __str__(self):
		ret = ''
		for row in self.rows:
			ret += '\n| '
			for elem in row:
				ret += str(elem) + '\t'
			ret = ret[:-1]
			ret += ' |'
		return ret

	def __mul__(self, val):
		ret = map(lambda row: map(lambda elem: elem * val, row), self.rows)
		return Matrix(ret)

	def __rmul__(self, val):
		ret = map(lambda row: map(lambda elem: elem * val, row), self.rows)
		return Matrix(ret)

	def rowSwiching(self, l, r):
		ret = map(lambda row: map(lambda elem: elem * 1, row), self.rows)
		ret[l], ret[r] = ret[r], ret[l]
		return Matrix(ret)

	def rowMul(self, r, k):
		ret = map(lambda row: map(lambda elem: elem * 1, row), self.rows)
		ret[r] = map(lambda elem: elem * k, ret[r])
		return Matrix(ret)

	def rowAdd(self, l, r, k = 1):
		ret = map(lambda row: map(lambda elem: elem * 1, row), self.rows)
		ret[l] = map(lambda x: x[0] + x[1] * k, zip(ret[l], ret[r]))
		return Matrix(ret)

if __name__ == '__main__':
	m1 = Matrix([[1, 2], [3, 4]])
	m2 = Matrix([[5, 6], [7, 8]])
	print Fraction(3, 2) * m1
	print m1 * Fraction(3, 2)
	print -1 * m1
	print m1 * -1
	print m1.rowSwiching(0, 1)
	print m1.rowMul(0, 2)
	print m1.rowMul(0, Fraction(2, 5))
	print m1.rowAdd(0, 1, 1)
	print m1.rowAdd(0, 1, 2)
	print 'm1 * 2 =', m1 * 2
	print 'm1 * 3/2 =', m1 * Fraction(3, 2)
	print '2 * m1 =', 2 * m1
	print m1
	print m2
