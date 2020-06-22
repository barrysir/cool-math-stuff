from sympy import Abs, Wild, sqrt
a,b,c = map(Wild, 'abc')

def abssimp(expr):
    '''Attempt to simplify an expression with absolute values in it'''
    expr = expr.replace(abs(a)**2, a**2)
    expr = expr.replace(c*abs(a)*abs(b), c*abs(a*b))
    return expr

def absreplace(expr):
    '''Replace abs(x) with sqrt(x**2)'''
    return expr.replace(abs(a), sqrt(a**2))

def forgraph(expr):
    '''Format a sympy expression so I can paste it into Graph'''
    expr = str(expr)
    expr = expr.replace('**', '^')
    expr = expr.replace('Abs', 'abs')
    return expr