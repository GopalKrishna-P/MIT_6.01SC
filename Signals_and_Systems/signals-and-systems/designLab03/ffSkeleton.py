import lib601.sm as sm

class FollowFigure(sm.SM):
    def __init__(self, points):
        self.points = points
        self.startState = 0
        self.len = len(self.points)
    def getNextValues(self, state, inp):
        for i in range(self.len):
            if inp.odometry.point().isNear(self.points[i], 0.01):
                if i == self.len -1:
                    return (0, self.points[0])
                else:
                    return (i + 1, self.points[i + 1])
        return (state, self.points[state])
