import lib601.poly as poly
import swLab04SignalDefinitions
reload(swLab04SignalDefinitions) # so changes you make in swLab04SignalDefinitions.py will be reloaded
from swLab04SignalDefinitions import *

# Wk.4.1.2
StepSignal().plot(-5,30)

#  Wk.4.1.3
s1 = StepSignal()
s2 = StepSignal()
SummedSignal(s1, s2).plot(-5, 10)
s3 = CosineSignal()
SummedSignal(s1, s3).plot(-5, 10)
ScaledSignal(StepSignal(), 5).plot(-5, 5)
SummedSignal(s1, ScaledSignal(s2, 4)).plot(-5, 5)

# Wk.4.1.4
R(UnitSampleSignal()).plot(-5, 5)
R(StepSignal()).plot(-5, 5)
Rn(UnitSampleSignal(), 3).plot(-5, 5)
Rn(UnitSampleSignal(), 8).plot(-5, 10)
s = UnitSampleSignal()
polyR(StepSignal(), poly.Polynomial([3,4,5,6,4,5,7,8,10,6,5])).plot(-5, 10)

