import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io

class DynamicMoveToPoint(sm.SM):
    def getNextValues(self, state, inp):
        # Replace this definition
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp[1].sonars[3], inp[1].sonars[4]
        assert isinstance(inp,tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0],util.Point), 'inp[0] should be a Point'
        ang = inp[1].odometry.point().angleTo(inp[0])
        sig = 1
        if 0 > inp[1].odometry.point().angleTo(inp[0]) - inp[1].odometry.theta > -math.pi:
            sig = -1
        if not util.nearAngle(ang, inp[1].odometry.theta, 0.01):
            return (state, io.Action(fvel=0.0 , rvel=sig*0.08))
        elif not inp[0].isNear(inp[1].odometry.point(), 0.01):
            return (state, io.Action(fvel=0.08 , rvel=0.0))
        return (state, io.Action(fvel=0.0 , rvel=0.0))

class stopPedestrians(sm.SM):
    def getNextValues(self, state, inp):
        return (state, io.Action(fvel=0.0 , rvel=0.0))

def stop_P(inp):
    return inp[1].sonars[3] <=0.300 or inp[1].sonars[4] <= 0.300

