import sympy

class Printer(sympy.printing.repr.ReprPrinter):
    def emptyPrinter(self, expr):
        class_name = type(expr).__name__
        if hasattr(sympy, class_name):
            return "sympy." + super().emptyPrinter(expr)
        else:
            return super().emptyPrinter(expr)

# Let's check how sympy prints something that is evaluated from sympy.
print("srepr original:", sympy.srepr(sympy.Symbol('t') * 3))

# Wait, `super()._print(expr)` returns a string like "Mul(Integer(3), Symbol('t'))".
# But it does so recursively! If we override emptyPrinter, does it prefix recursively?
