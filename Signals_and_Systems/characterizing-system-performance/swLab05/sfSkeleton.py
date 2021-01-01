"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    def __init__(self, numeratorPoly, denominatorPoly):
        self.numerator = numeratorPoly
        self.denominator = denominatorPoly
    def poles(self):
        poles_coeffs = self.denominator.coeffs[:]
        poles_coeffs.reverse()
        return poly.Polynomial(poles_coeffs).roots()
    def poleMagnitudes(self):
        poles_list = self.poles()
        poles_magnitude = []
        for pole in poles_list:
            poles_magnitude.append(abs(pole))
        return poles_magnitude
    def dominantPole(self):
        poles_magnitude = self.poleMagnitudes()
        return util.argmax(poles_magnitude, lambda x: x)
    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    """
    The output of the fisrt system function is the input of the second.
    """
    return SystemFunction(sf1.numerator * sf2.numerator, sf1.denominator * sf1.denominator)

def FeedbackSubtract(sf1, sf2=None):
    """
    Make the generic expression for the FeedbackSubtract block diagram.
    """
    numerator = sf1.numerator*sf1.denominator*sf2.denominator
    denominator = ((sf1.denominator*sf1.denominator)*sf2.denominator) + (sf1.denominator*sf1.numerator*sf2.numerator)
    return SystemFunction(numerator, denominator)