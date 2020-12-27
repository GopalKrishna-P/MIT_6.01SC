#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

#-----------------------------------------------------------------------------

def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

# Test
print fib(1)   # 1
print fib(5)   # 5
print fib(10)  # 55

#-----------------------------------------------------------------------------

class V2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y)+")"
    def __add__(vector1, vector2):
        return V2(vector1.getX() + vector2.getX(), vector1.getY() + vector2.getY())
    def __mul__(vector1, num):
        return V2(vector1.getX() * num, vector1.getY() * num)

# Test
vec1 = V2(3,4)
vec2 = V2(2,2)
print(vec1 + vec2)
print(vec1*5)

#-----------------------------------------------------------------------------

import itertools

class Polynomial:
    def __init__(self, coefficients):
        self.coeffs = []
        self.length = 0
        for num in coefficients:
            self.coeffs.append(num * 1.0)
            self.length += 1

    def coeff(self, i):
        pos = self.length - i - 1
        return self.coeffs[pos]

    def add(self, other):
        self.added = []
        for item in itertools.izip_longest(reversed(self.coeffs), reversed(other.coeffs), fillvalue=0):
            self.added.insert(0, (item[0] + item[1]))

        return Polynomial(self.added)

    def __add__(self, other):
        return self.add(Polynomial(other.coeffs))

    def mul(self, other):
        self.mult1 = []
        self.mult2 = []
        for item in itertools.izip_longest(reversed(self.coeffs), reversed(other.coeffs), fillvalue=1):
            self.mult1.insert(0, (item[0] * item[1]))

        for i in range(0, (self.length * 2 - 1)):
            self.mult2.append(0)

        for item in self.mult1:
            self.mult2[self.mult1.index(item) * 2] = item

        return Polynomial(self.mult2)

    def __mul__(self, other):
        return self.mul(Polynomial(other.coeffs))

    def __str__(self):
        string = ""
        for i in range (0, self.length):
            if self.coeffs[i] != 0.0:
                if (self.length - (i+1)) > 1:
                    string += str(self.coeffs[i]) + " z**" + str(self.length - (i+1)) + " + "
                elif (self.length - (i+1)) is 1:
                    string += str(self.coeffs[i]) + " z"  + " + "
                elif (self.length - (i+1)) is 0:
                    string += str(self.coeffs[i])
        return string

    def val(self, v):
        total = 0
        for i in range (0, self.length):
            total += self.coeffs[i] * v**(self.length - (i+1))
        return total

    def roots(self):
        root_list = []
        if self.length > 3:
            return "Order too high to solve for roots."
        else:
            if self.length == 1:
                return "Does not have any roots."
            elif self.length == 2:
                return (0 - self.coeffs[1]) / self.coeffs[0]
            elif self.length == 3:
                a = self.coeffs[0]
                b = self.coeffs[1]
                c = self.coeffs[2]

                under_root = b**2 - (4 * a * c)
                denominator = 2 * a

                if under_root >= 0:
                    numerator1 = (-1 * b) + under_root**0.5
                    numerator2 = (-1 * b) - under_root**0.5
                else:
                    numerator1 = (-1 * b) + complex(under_root, 0)**0.5
                    numerator2 = (-1 * b) - complex(under_root, 0)**0.5
                return [(numerator1 / denominator), (numerator2 / denominator)]

    def __repr__(self):
        return str(self)



# Test

P1 = Polynomial([1, 2, 3])
P2 = Polynomial([1, 2])
print P1
print P1.__add__(P2)
print P1(1), P1(-1)
print (P1+P2)(10)
print P1.__mul__(P1)
print (P1*P2) + P1
print P1.roots()
print P2.roots()
P3 = Polynomial([3,2,-1])
print P3.roots()
print (P1*P1).roots()
