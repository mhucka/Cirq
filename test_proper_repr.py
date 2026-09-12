import sympy
from cirq._compat import proper_repr
v = sympy.Symbol('t') * 3

print("srepr(v):", sympy.srepr(v))
print("proper_repr(v):", proper_repr(v))

try:
    print("eval srepr:", eval(sympy.srepr(v)))
except Exception as e:
    print("eval srepr failed:", e)

try:
    print("eval proper_repr:", eval(proper_repr(v)))
except Exception as e:
    print("eval proper_repr failed:", e)
