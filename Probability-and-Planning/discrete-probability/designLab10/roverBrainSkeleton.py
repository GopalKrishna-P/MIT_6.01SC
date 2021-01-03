import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
    print 'setting labPath to', labPath

from boundaryFollower import boundaryFollowerClass
        
class MySMClass(boundaryFollowerClass):
    def __init__(self):
        pass

    def getNextValues(self, state, inp):
        V4 = inp.analogInputs[2]
        V6 = inp.analogInputs[1]
        # print 'inputs ==>',inp.analogInputs
        print 'V4 ===>', V4
        print 'V6 ===>', V6
        # neckVoltage = inp.analogInputs[1]
        # outputVoltage = io.Action(fvel=0, rvel=0,voltage = V0)
        V0 = ((5 * (V6 - V4) / 2.08)* 0.5 + 5)
        print 'V0 ===>', V0
        if V0 < 0:
            V0 = 0
        if V0 > 10:
            V0 = 10

        V_light = 6.2
        # return state, io.Action(fvel=0.0, rvel=0, voltage=V0)
        if V6 > V_light:
            print 'find light'
            return state, io.Action(fvel = 0.1, rvel = 0.3 * (V0 - 5), voltage=V0)
        else:
            print 'boundaryFollower'
            return boundaryFollowerClass.getNextValues(self, state, inp)


mySM = MySMClass()
mySM.name = 'brainSM'
    

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)

def brainStart():
    robot.behavior = mySM
    robot.behavior.start(robot.gfx.tasks())
    robot.data = []

def step():
    inp = io.SensorInput()
    robot.behavior.step(inp).execute()

def brainStop():
    pass

def shutdown():
    pass
