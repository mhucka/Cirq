import sympy

v = sympy.Symbol('t') * 3

# To avoid using the hack in cirq, cirq needs a proper repr.
# Proper repr for a sympy expr in cirq used to manually prepend 'sympy.' to all these tokens:
# 'Symbol', 'pi', 'Mul', 'Pow', 'Add', ...

# But wait, in python we can just evaluate the srepr using `sympy` namespace dict!
# The whole point of `proper_repr` is to produce a string that can be evaluated.
# E.g. `eval(proper_repr(v))` works.
# But wait, cirq is used by users. When users print a cirq circuit, they want `proper_repr` of a sympy expression to be copy-pasteable.
# If they copy paste `sympy.Mul(sympy.Integer(3), sympy.Symbol('t'))`, they just need `import sympy`.
# But wait! The issue says "Refactor to remove hack."
# Can we just use `sympy.srepr(..., fully_qualified=True)`? Let's check if sympy has such an option in some version.
import sys
# Is there a setting `fully_qualified_modules` or something?
