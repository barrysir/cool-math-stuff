# continuous-piecewise

Writing piecewise functions in a single equation using only "normal" functions. \
Read the post [here [link to be added]]().

## Requirements

 * Python 3.7
 * sympy 1.4

`absolute.py` - writing piecewise functions using absolute values \
`heaviside.py` - writing piecewise functions using the Heaviside step function \
`abssimp.py` - simplify expressions containing absolute values \
`uwu.py` - code to generate the uwu functions

## Example usage

```python
from absolute import Piecewise
from sympy import sympify, oo   # turn numbers into sympy expressions

f = Piecewise([
    (x, -3, 0),
    (x**2, 0, 2),
    (sympify(4), 2, oo)
])
print(f)
```