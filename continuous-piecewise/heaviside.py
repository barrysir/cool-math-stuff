from sympy import symbols, oo, sympify, Heaviside, sqrt, acos, cos, pi
x = symbols('x')

def U(a, side):
    '''The unit function: 0 when x<a and 1 when x>a.
    The value at x=a is determined by the 'side' argument.
        side = 'left'   -> 0 at x=a
        side = 'right'  -> 1 at x=a
    '''
    # Using the definition of Heaviside where it's 1 at x=0
    # uncomment these if you want it when it's 0 at x=0
    # H0 = Heaviside(x, 0)    # heaviside, 0 at x=0
    # H1 = 1-H0.subs(x,-x)    # heaviside, 1 at x=0
    H1 = Heaviside(x, 1)
    H0 = 1-H1.subs(x,-x)
    if side == 'left':
        return H0.subs(x, x-a)
    elif side == 'right':
        return H1.subs(x, x-a)
    else:
        raise ValueError("side was not left or right (%s)" % (side))
    
def Boxcar(x1, x2, left=True, right=True):
    '''The boxcar function: 1 when x1 < x < x2, 0 otherwise.
    x1 and x2 can also be set to -oo and oo respectively for no boundaries.
    
    The 'left' and 'right' arguments determine whether the endpoints
    are included in the region or not.
    (default: the left and right endpoints are included)
    '''
    assert x1 <= x2

    if x1 == -oo:   fleft = 1
    else:   fleft = U(x1, 'right' if left else 'left')
    if x2 == oo:    fright = 0
    else:   fright = U(x2, 'left' if right else 'right')
    
    return fleft - fright

def Chop(expr, x1, x2, left=True, right=True):
    '''
            { 0         if x < x1
    f(x) =  { expr(x)   if x1 <= x <= x2
            { 0         if x > x2

    x1,x2 can also be set to -oo and oo respectively, to have
    the function go off to infinity instead.
    '''
    return expr * Boxcar(x1, x2, left, right)

def Undefined(x1, x2, c=0):
    '''Return a function which is undefined within (x1, x2) and c otherwise'''
    if x1 == -oo and x2 == oo:
        x_function = sqrt(-1)
    elif x1 == -oo:
        x_function = sqrt(x-x2)
    elif x2 == oo:
        x_function = sqrt(-(x-x1))
    else:
        x_function = sqrt((x-x1)*(x-x2))
    
    return Chop(x_function, x1, x2) + c

def Oscillate(f, src, dest):
    '''
    Create a function which oscillates from f(x0) to f(x1), from f(x1) to f(x0), ...
    src = (x0, x1) is the slice of the function to oscillate over
    dest = (x2, x3) is where the slice from (x0, x1) gets mapped in the returned function
    '''
    #create a function which oscillates between [0,1] over [x0,x1]
    x0,x1 = src
    x2,x3 = dest
    x_function = (x-x2)/(x3-x2)
    # use acos here because the math lines up nicer
    oscillator = acos(cos(x_function*pi))/pi   #[x2,x3] -> [0,1]
    return f.subs(x, oscillator*(x1-x0) + x0)  #[x2,x3] -> [0,1] -> [x0,x1]

# ----------------------------------
#  Piecewise function generators
# ----------------------------------
def Piecewise(parts):
    '''
    parts is a list of tuples in the format
        (func1, left x bound, right x bound),
        (func2, left x bound, right x bound),
        etc ...

    Assumes that the piecewise function is continuous
    (each part connects with each other).
    Might do funny things if they're not.
    '''
    return sum(map(lambda x: Chop(*x), parts))

def Glued(parts, start_point=(0,0), left=None, right=None):
    '''
    Cuts out regions from given functions and glues them together
    to form a continuous piecewise function.

    Returns a list of function parts you can pass into Piecewise().

    parts - a list of function regions, in the format [(f, x1, x2), ...]
    start_point - an (x,y) coordinate specifying where the first function part should start
    left - a function region to use off to -oo (e.g. [x**2, -oo, 0])
    right - a function region to use off to oo (e.g. [x**2, 0, oo])
    '''

    def translate(f, src, dest):
        '''translate f so that the point `src` moves to the point `dest`'''
        dx = dest[0]-src[0]
        dy = dest[1]-src[1]
        return f.subs(x, x-dx) + dy
    
    new_parts = []
    if left:        
        f,x1,x2 = left
        assert x1 == -oo, "left bound of `left` argument must be -oo"
        moved_f = translate(f, (x2, f.subs(x, x2)), start_point)
        new_parts.append((moved_f, -oo, start_point[0]))
    
    for f,x1,x2 in parts:
        length = x2 - x1
        delta = f.subs(x, x2) - f.subs(x, x1)
        moved_f = translate(f, (x1, f.subs(x, x1)), start_point)
        new_parts.append((moved_f, start_point[0], start_point[0]+length))
        start_point = (start_point[0]+length, start_point[1]+delta)
    
    if right:
        f,x1,x2 = right
        assert x2 == oo, "right bound of `right` argument must be oo"
        moved_f = translate(f, (x1, f.subs(x, x1)), start_point)
        new_parts.append((moved_f, start_point[0], oo))
    
    return new_parts

def Glue(*args, **kwargs):
    '''
    Cuts out regions from given functions and glues them together
    to form a continuous piecewise function.
    Alias for Piecewise(Glued([arguments])).
    '''
    return Piecewise(Glued(*args, **kwargs))