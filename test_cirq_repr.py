import sympy
from cirq._compat import proper_repr

v5 = sympy.I
print("I:", proper_repr(v5))

# Wait, `proper_repr(sympy.I)` is `sympy.I` with sympy 1.14.
# Previously it might have been `I`.
