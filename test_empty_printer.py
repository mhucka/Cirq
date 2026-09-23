import sympy
class Printer(sympy.printing.repr.ReprPrinter):
    def emptyPrinter(self, expr):
        class_name = type(expr).__name__
        if hasattr(sympy, class_name) and getattr(sympy, class_name) is type(expr):
            return "sympy." + super().emptyPrinter(expr)
        else:
            return super().emptyPrinter(expr)

# The hack currently in cirq:
fixed_tokens = [
    'Symbol',
    'pi',
    'Mul',
    'Pow',
    'Add',
    'Mod',
    'Integer',
    'Float',
    'Rational',
    'GreaterThan',
    'StrictGreaterThan',
    'LessThan',
    'StrictLessThan',
    'Equality',
    'Unequality',
    'And',
    'Or',
    'Not',
    'Xor',
    'Indexed',
    'IndexedBase',
]
