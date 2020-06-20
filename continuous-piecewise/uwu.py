from absolute import Glue, Undefined, Oscillate
from abssimp import abssimp
from sympy import symbols, pi, sympify, latex, Rational, lambdify, oo

x = symbols('x')

# -------------------------------
#   PARAMETERS
# -------------------------------
# The U is made from an inverse quadratic function n/((x-a)(x-b))
#   the minimum of U is at x=1/2 (the function is centered around x=1/2)
#   the slice from [0,1] is used to make the U
#   a,b are set to slightly before 0 and slightly after 1, so there is a "margin" between a,b and 0,1
#   n is calibrated such that U(0) = U(U_WIDTH) = U_LEVEL
# The V is made from an absolute value centered around x=0
#   The absolute value is cut within a window [V_LEFT, V_RIGHT] to make a V
#   one side is less than the other to make the shorter middle peak in the W
#   V(0) = 0
#   V(V_LEFT) = (height of U)
# the whole thing is reflected across the y-axis so UV -> UWU
# this also makes it possible to make a repeating UWU by oscillating over UV

# UWU_PERIOD    - period to repeat the uwu graph
# (UWU_SIZE     - width of the whole UWU, calculated below)
# UWU_HEIGHT    - height of the UWU
# U_WIDTH       - width of the U
# U_LEVEL       - calibration value for U(0)
# U_MARGIN      - margin between the asymptotes a,b and 0,U_WIDTH
# LETTER_GAP    - spacing to put between the U and W
# V_WIDTH       - width of a V
# V_LEFT        - left cutoff x value
# V_RIGHT       - right cutoff x value
# I tried to choose these fractions to make the numbers as simple as possible
# (while keeping the UWU from looking too weird)
UWU_PERIOD = Rational(69, 10)
UWU_HEIGHT = Rational(4, 3)
U_WIDTH = sympify(1)
U_LEVEL = Rational(6, 4)
U_MARGIN = sympify(3)/96
LETTER_GAP = sympify(3)/16
V_WIDTH = 1 - LETTER_GAP
V_LEFT = V_WIDTH * Rational(-4, 7)
V_RIGHT = V_WIDTH * Rational(3, 7)

# -------------------------------
#   CODE
# -------------------------------
def make_u(a, b):
    # set n so that U(0) = U(U_WIDTH) = U_LEVEL
    n = U_LEVEL*a*b
    return n/((x-a)*(x-b))

def simplify_abs(expr):
    expr = sum(i.simplify() for i in expr.args)
    expr = abssimp(expr)
    return expr

assert V_RIGHT - V_LEFT == V_WIDTH
assert V_LEFT < 0
assert V_RIGHT > 0
UWU_SIZE = U_WIDTH + LETTER_GAP + (V_RIGHT - V_LEFT)*2 + LETTER_GAP + U_WIDTH
spacing = (UWU_PERIOD - UWU_SIZE) / 2
assert UWU_SIZE < UWU_PERIOD

u = make_u(-U_MARGIN, U_WIDTH+U_MARGIN)
u_min = u.subs(x, U_WIDTH/2).simplify()
v = (U_LEVEL-u_min)/(-V_LEFT)*abs(x)

uv = Glue([
    (sympify(0), 0, spacing),
    (u, 0, U_WIDTH),
    (sympify(0), 0, LETTER_GAP),
    (v, V_LEFT, V_RIGHT),
], start_point=(-UWU_PERIOD/2, 0))
uv *= UWU_HEIGHT / (U_LEVEL-u_min)  # scale to the correct height

# a version of uv where the blanks are replaced with undefined functions
# uv = Glue([
#     (Undefined(0, spacing), 0, spacing),
#     (u, 0, U_WIDTH),
#     (Undefined(0, LETTER_GAP), 0, LETTER_GAP),
#     (sympify(0), 0, LETTER_GAP),
#     (v, V_LEFT, V_RIGHT),
# ], start_point=(-UWU_PERIOD/2, 0), left=(Undefined(-oo, 0), -oo, 0))

uwu = uv.subs(x, -abs(x))
# uwu = uv + uv.subs(x, -x) - uv.subs(x, 0).simplify()  # alternative way of writing it
uwu = simplify_abs(uwu)
print(str(uwu).replace('**', '^').replace('Abs', 'abs'))

uwu_repeat = Oscillate(
    uv,
    [-UWU_PERIOD/2, 0],
    [-UWU_PERIOD/2, 0]
)
uwu_repeat = simplify_abs(uwu_repeat)
print(str(uwu_repeat).replace('**', '^').replace('Abs', 'abs'))