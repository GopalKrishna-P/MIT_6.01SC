import lib601.poly as poly
import lib601.sig
from lib601.sig import *

## You can evaluate expressions that use any of the classes or
## functions from the sig module (Signals class, etc.).  You do not
## need to prefix them with "sig."

class ConstantSignal(Signal):
    def __init__(self, c):
        self.c = c
    def sample(self, n):
        return self.c
    
class CosineSignal(Signal):
    def __init__(self, omega = 1, phase = 0):
        self.omega = omega
        self.phase = phase
    def sample(self, n):
        return math.cos(self.omega * n + self.phase)
    
class UnitSampleSignal(Signal):
    def sample(self, n):
        return n == 0

# WK.4.1.1
step1 = polyR(ScaledSignal(StepSignal(), 3), poly.Polynomial([1,0,0,0]))
step1.plot(-5, 10)
step2 = polyR(ScaledSignal(StepSignal(), -3), poly.Polynomial([1,0,0,0,0,0,0,0]))
step2.plot(-5,10)
stepUpDown = SummedSignal(step1, step2)
stepUpDown.plot(-5,10)
stepUpDownPoly_1 = polyR(UnitSampleSignal(), poly.Polynomial([1,0]))
stepUpDownPoly_3 = polyR(UnitSampleSignal(), poly.Polynomial([3,0,0,0]))
stepUpDownPoly_5 = polyR(UnitSampleSignal(), poly.Polynomial([5,0,0,0,0,0]))
stepUpDownPoly = SummedSignal(SummedSignal(stepUpDownPoly_1, stepUpDownPoly_3), stepUpDownPoly_5)
stepUpDownPoly.plot(-5,10)

usamp = UnitSampleSignal()
polyR(usamp, poly.Polynomial([3, 5, -1, 0, 0, 3, -2])).plot(-5, 15)
