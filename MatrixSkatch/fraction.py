#-*- coding: utf-8 -*-
def getGCD(a, b):
	ma = max(a, b)
	mi = min(a, b)
	if ma % mi != 0:
		return getGCD(mi, ma % mi)
	return mi

def irreducible(a, b):
	gcd = getGCD(a, b)
	return a/gcd, b/gcd

class Fraction(object):
	def __init__(self, n, d):
		self.n = n
		self.d = d

	def __add__(self, rhs):
		if type(rhs) == int:
			rhs = Fraction(rhs, 1)
		v1 = self.n * rhs.d
		v2 = rhs.n * self.d
		nn = v1 + v2
		nd = self.d * rhs.d
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)

	def __radd__(self, lhs):
		return self.__add__(lhs)

	def __sub__(self, rhs):
		if type(rhs) == int:
			rhs = Fraction(rhs, 1)
		v1 = self.n * rhs.d
		v2 = rhs.n * self.d
		nn = v1 - v2
		nd = self.d * rhs.d
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)

	def __rsub__(self, lhs):
		return lhs + -self
	
	def __mul__(self, rhs):
		if type(rhs) == int:
			rhs = Fraction(rhs, 1)
		if type(rhs) == Fraction:
			nn = self.n * rhs.n
			nd = self.d * rhs.d
			if 0 == nn:
				return Fraction(0, nd)
			gcd = getGCD(abs(nn), abs(nd))
			return Fraction(nn / gcd, nd / gcd)
		else:
			return rhs * self

	def __rmul__(self, lhs):
		try:
			return self * lhs
		except Exception, e:
			return lhs * self

	def __div__(self, rhs):
		if type(rhs) == int:
			rhs = Fraction(rhs, 1)
		nn = self.n * rhs.d
		nd = self.d * rhs.n
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)

	def __rdiv__(self, lhs):
		return lhs * Fraction(self.d, self.n)

	def __neg__(self):
		return Fraction(-self.n, self.d)

	def __cmp__(self, rhs):
		v1 = self.n * rhs.d
		v2 = rhs.n * self.d
		return cmp(v1, v2)

	def __str__(self):
		if self.n == 0:
			return '0'
		if self.d == 1:
			return str(self.n)
		if self.d == -1:
			return str(self.d * -1)
		return '%d/%d' % (self.n, self.d)


if __name__ == '__main__':
	def testpass(val):
		if False == val:
			print 'assertion failed'
	l = Fraction(3, 4)
	r = Fraction(1, 5)
	print 1 / l
	print 2 * l
	print 1 - l
	print 1 + l
	print Fraction(-1, 3)
	print l + r
	print l * 2
	print l + 1
	print Fraction(1, 3) + Fraction(1, 6)
	print Fraction(1, 3) - Fraction(1, 6)
	print Fraction(-1, 3) + Fraction(1, 3)
	print Fraction(-1, 3) - Fraction(1, 3)
	print Fraction(-1, 3) * Fraction(1, 3)
	print Fraction(-1, 3) / Fraction(1, 3)
	#testpass(l > r)
	#testpass(r < l)
	testpass(Fraction(1, 5) < Fraction(2, 5))
	testpass(False == (Fraction(2, 5) != Fraction(2, 5)))
	testpass(Fraction(2, 5) == Fraction(2, 5))
