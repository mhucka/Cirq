import sympy

class Printer(sympy.printing.repr.ReprPrinter):
    def _print(self, expr, **kwargs):
        s = super()._print(expr, **kwargs)
        mod = getattr(getattr(expr, '__class__', None), '__module__', '')

        # If it's a sympy object, we prefix it with sympy.
        # But wait! What if it's evaluated to a primitive string somehow?
        # sympy.srepr always returns a constructor-like call or a singleton name.
        if mod.startswith('sympy'):
            return f"sympy.{s}"
        return s

v = sympy.pi * sympy.Symbol('t')
print("pi * t:", Printer().doprint(v))
