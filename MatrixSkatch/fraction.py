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

class Fraction:
	def __init__(self, n, d):
		self.n = n
		self.d = d

	def __add__(self, rhs):
		v1 = self.n * rhs.d
		v2 = rhs.n * self.d
		nn = v1 + v2
		nd = self.d * rhs.d
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)

	def __sub__(self, rhs):
		v1 = self.n * rhs.d
		v2 = rhs.n * self.d
		nn = v1 - v2
		nd = self.d * rhs.d
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)
	
	def __mul__(self, rhs):
		nn = self.n * rhs.n
		nd = self.d * rhs.d
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)

	def __div__(self, rhs):
		nn = self.n * rhs.d
		nd = self.d * rhs.n
		if 0 == nn:
			return Fraction(0, nd)
		gcd = getGCD(abs(nn), abs(nd))
		return Fraction(nn / gcd, nd / gcd)

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
	print Fraction(-1, 3)
	print l + r
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
