import pdb
import lib601.sm as sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

class Sum(BinaryOp):
    opStr = 'Sum'
    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return operator.add(left, right)

class Prod(BinaryOp):
    opStr = 'Prod'
    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return operator.mul(left, right)    

class Quot(BinaryOp):
    opStr = 'Quot'
    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return operator.div(left, right)    

class Diff(BinaryOp):
    opStr = 'Diff'
    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return operator.sub(left, right)

class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self, env):
        right = self.right.eval(env)
        env[self.left.name] = right

class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__
    def eval(self, env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
    # Return the value associated with the variable.
    def eval(self, env):
        return env[self.name]

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize(string):
    sup_str = ''
    # Concatenating the string in other string(sup_string).
    for char in string:
        # But if the char is a special one, I plub a space after and before the special char.
        if char in seps:
            sup_str = sup_str + ' ' + char + ' ' 
        else:
            sup_str = sup_str + char
    # By this way when I split up, I will get the result I want.
    list_str = sup_str.split()
    return list_str
# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        # If the token at this index is a number.
        if numberTok(tokens[index]):
            # Return the token instantiated as a Num and the next index.
            return (Number(float(tokens[index])), index+1)
        # IF the token is a variable.
        elif variableTok(tokens[index]):
            # Return the token instantiated as a Var and the next index.
            return (Variable(tokens[index]), index+1)
        # Otherwise, It is a parentheses '('.
        else:
            # For example (3 + 5)
            # '(' --> index / '3' --> index + 1 / '+' --> op(index+2) /'5' --> op + 1/ ')' --> nextIndex 
            (leftTree, op) = parseExp(index + 1)
            # Parse the expression and call RightTree then return it and the next index beyond the expression.
            (rightTree, nextIndex) = parseExp(op + 1)
            # Analyzi op to decide what kind of Instatiate to take.
            if tokens[op] == '+':
                return (Sum(leftTree, rightTree), nextIndex + 1)
            elif tokens[op] == '*':
                return (Prod(leftTree, rightTree), nextIndex + 1)
            elif tokens[op] == '/':
                return (Quot(leftTree, rightTree), nextIndex + 1)
            elif tokens[op] == '-':
                return (Diff(leftTree, rightTree), nextIndex + 1)
            elif tokens[op] == '=':
                return (Assign(leftTree, rightTree), nextIndex + 1)        
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        print '%', e, '\n', parse(tokenize(e)).eval(env)# your expression here
        print '   env =', env

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession
        print parse(tokenize(e)).eval(env)        # your expression here
        print '   env =', env

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)

class Tokenizer(sm.SM):
    startState = ''
    def getNextValues(self, state, inp):  # inp is a single character.

        if inp in seps:
            return (inp, state)
        elif inp == ' ':
            return ('', state)
        else:
            if state in seps:
                output = state
                state = ''
                return (state+inp, output)
            else:
                return (state+inp, '')

def tokenize(inputString):
    tokens_des = Tokenizer().transduce(inputString+' ')
    tokens_org = []
    for token in tokens_des:
        if token != '':
            tokens_org.append(token) 
    return tokens_org
