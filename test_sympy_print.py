import sympy
v = sympy.Symbol('t') * 3

class Printer(sympy.printing.repr.ReprPrinter):
    def _print(self, expr, **kwargs):
        # Is there a cleaner way to prefix with sympy?
        # A repr string is usually "Class(args)".
        # If the class is in sympy, we can prefix it.
        pass

# The issue is about removing the "hack". What is a better way to do it?
# In SymPy 1.7 or later, maybe there is `sympy.srepr` with `sympy_integers`? No.
# Maybe we can simply look at the class of `expr` and see its module.
