import sympy
from test_dynamic_pi import Printer

v = sympy.pi * sympy.Symbol('t') + sympy.Rational(1, 2)
v2 = sympy.Eq(sympy.Symbol('x'), sympy.Integer(5))
v3 = sympy.Not(sympy.Symbol('y'))

def test_expr(expr):
    s = Printer().doprint(expr)
    print(f"Original: {expr}")
    print(f"Printed: {s}")
    eval(s)
    print("Eval successful\n")

test_expr(v)
test_expr(v2)
test_expr(v3)
