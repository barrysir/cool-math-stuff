from sympy import Abs, Wild
a,b,c = map(Wild, 'abc')

def abssimp(expr):
    '''Attempt to simplify an expression with absolute values in it'''
    expr = expr.replace(abs(a)**2, a**2)
    expr = expr.replace(c*abs(a)*abs(b), c*abs(a*b))
    return expr