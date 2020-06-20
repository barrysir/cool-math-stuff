from sympy import symbols, oo, sympify, Rational, sqrt, acos, cos, pi
x = symbols('x')

def Ramp(pt, slope, side):
    '''Generates the "ramp" function (left-sided or right-sided).

    Example of the right-sided ramp function:
        f(x) =  { y1         if x <= x1
                { line starting at (pt) with given slope if x > x1
    For the left-sided version, the line occurs when x <= x1 instead.

    Put 'left' or 'right' into the side argument to indicate which one to generate.
    '''
    fundamental = (abs(x)+x)/2
    fundamental *= slope
    if side == 'left':
        fundamental = -fundamental.subs(x, -x)
    elif side == 'right':
        pass
    else:
        raise ValueError("invalid value for side argument: {}".format(side))
    return fundamental.subs(x, x-pt[0]) + pt[1]

def Incline(pt1, pt2):
    '''Generates the "incline" function between two points:
            { y1        if x < x1
    f(x) =  { line segment between (x1,y1) and (x2,y2)   if x1 <= x <= x2
            { y2        if x > x2
    '''
    # direct calculation
    # a,b = pt1
    # c,d = pt2
    # return Rational(1,2) * Rational(d-b,c-a) * (abs(x-a) + abs(x-c)) + Rational(b+d, 2)
    
    # this is the function Ramp((0,0), (1,1))    
    fundamental = ((abs(x)+x) - (abs(x-1) + x-1))/2
    
    # scale the function to arbitrary points
    start = pt1[:]
    size = [pt2[0]-pt1[0], pt2[1]-pt1[1]]
    return fundamental.subs(x, (x-start[0])/size[0])*size[1] + start[1]

def Clip(expr, x1, x2):
    '''
    Clips a function to the window [x1,x2].
    
            { expr(x1)  if x < x1
    f(x) =  { expr(x)   if x1 <= x <= x2
            { expr(x2)  if x > x2

    x1,x2 can also be set to -oo and oo respectively, to have
    the function go off to infinity instead.
    '''
    if x1 == -oo and x2 == oo:
        x_function = x
    elif x1 == -oo:
        x_function = Ramp((x2, x2), 1, 'left')
    elif x2 == oo:
        x_function = Ramp((x1, x1), 1, 'right')
    else:
        x_function = Incline((x1, x1), (x2, x2))
    return expr.subs(x, x_function)

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
    
    return Clip(x_function+c, x1, x2)

    # ramp = Ramp((x1, 0), -1, 'left') + Ramp((x2, 0), 1, 'right')
    # absolute = abs(x - Rational(x1+x2, 2)) - Rational(x2-x1, 2)
    # return absolute/ramp - 1
    # inner = abs((x1+x2)/2) - (x2-x1)/2
    # return e**ln(inner) - inner
    # return sqrt((x-x1)**2 + (x-x2)**2 -2*abs((x-x1)*(x-x2)) - (x1-x2)**2)

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

    Assumes that the piecewise function is continuous across its parts
    (each part connects with each other).
    Might do funny things if they're not.
    '''
    func = 0
    is_first = True
    for f, x1, x2 in parts:
        func += Clip(f, x1, x2) 
        if not is_first:
            func += -f.subs(x, x1).simplify()
        is_first = False
    return func

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