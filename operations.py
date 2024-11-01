import operator
import math


operation2 = {}

operation2['+'] = lambda a,b: a+b
operation2['-'] = operator.sub
operation2['*'] = operator.mul
operation2['/'] = operator.truediv
operation2['//'] = operator.floordiv
operation2['%'] = operator.mod
operation2['**'] = lambda a,b: a**b

