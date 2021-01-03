"""
Discrete probability distributions
"""

import random
import operator
import copy

import lib601.util as util

def removeElt(items, i):
    """
    non-destructively remove the element at index i from a list;
    returns a copy;  if the result is a list of length 1, just return
    the element
    """
    result = items[:i] + items[i+1:]
    if len(result) == 1:
        return result[0]
    else:
        return result

class DDist:
    def __init__(self, dictionary):
        self.d = dictionary
        """ Dictionary whose keys are elements of the domain and values
        are their probabilities. """

    def dictCopy(self):
        """
        @returns: A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        @param elt: an element of the domain of this distribution
        (does not need to be explicitly represented in the dictionary;
        in fact, for any element not in the dictionary, we return
        probability 0 without error.)
        @returns: the probability associated with C{elt}
        """
        if self.d.has_key(elt):
            return self.d[elt]
        else:
            return 0
    
    def marginalizeOut(self,index):
        newDict = {}
        oldStates = []
        newStates = []
        for state in self.d.keys():
            if removeElt(state,0) not in newStates:
                newStates.append(removeElt(state,0))
            if removeElt(state,1) not in oldStates:
                oldStates.append(removeElt(state,1))
        if index == 1:
            intState = oldState
            oldState = newState
            newState = intState
        for state in newStates:
            value = 0
            for oldState in oldStates:
                value += self.prob((oldState,state))
            newDict[state] = value
        return DDist(newDict)

    def conditionOnVar(self, index, value):
        outDict = {}
        nonNormalizedDict = {}
        for state in self.d.keys():
            if removeElt(state,abs(index-1)) == value:
                nonNormalizedDict[state] = self.d[state]
        normalizationCoefficient = sum(nonNormalizedDict.values())
        for state in nonNormalizedDict:
            outDict[state[abs(index-1)]] = nonNormalizedDict[state]/normalizationCoefficient
        return DDist(outDict)

    def support(self):
        """
        @returns: A list (in arbitrary order) of the elements of this
        distribution with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add,
                              [util.prettyString(k)+": "+\
                               util.prettyString(p)+", " \
                               for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__


def PTgD(diseaseValue):
    if diseaseValue == 'disease':
        return DDist({'posTest':0.98,'negTest':0.02})
    elif diseaseValue == "noDisease":
        return DDist({'posTest':0.05,'negTest':0.95})
    else:
        raise Exception, 'invalid value for D'

def RgF(floorValue):
    if floorValue == 'f1':
        return DDist({'r1':0.25,'r2':0.25,'r3':0.25,'r4':0.25})
    elif floorValue == 'f2':
        return DDist({'r1':0.1,'r2':0.1,'r3':0.1,'r4':0.7})
    else:
        raise Exception, 'invalid floor value'

def PTgD(val):
    if val == 'disease':
        return DDist({'posTest':0.9,'negTest':0.1})
    else:
        return DDist({'posTest':0.5,'negTest':0.5})

def JDist(PA, PBgA):
    dict = {}
    aCopy = PA.dictCopy()
    for state in aCopy.keys():
        jointDict = PBgA(state).dictCopy()
        for result in jointDict.keys():
            dict[(state,result)] = PA.prob(state)*PBgA(state).prob(result)
    return DDist(dict)

def bayesEvidence(PBgA, PA, b):
    return JDist(PA,PBgA).conditionOnVar(1,b)

def totalProbability(PBgA, PA):
    return JDist(PA,PBgA).marginalizeOut(0)

######################################################################
#   Utilities


def removeElt(items, i):
    """
    non-destructively remove the element at index i from a list;
    returns a copy;  if the result is a list of length 1, just return
    the element  
    """
    result = items[:i] + items[i+1:]
    if len(result) == 1:
        return result[0]
    else:
        return result

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.
    
    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v

# If you want to plot your distributions for debugging, put this file
# in a directory that contains lib601, and where that lib601 contains
# sig.pyc.  Uncomment all of the following.  Then you can plot a
# distribution with something like:
# plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)

# import lib601.sig as sig

# class IntDistSignal(sig.Signal):
#     def __init__(self, d):
#         self.dist = d
#     def sample(self, n):
#         return self.dist.prob(n)
# def plotIntDist(d, n):
#     IntDistSignal(d).plot(end = n, yOrigin = 0)
