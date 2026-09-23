import subprocess

with open('cirq-core/cirq/_compat.py', 'r') as f:
    content = f.read()

# Replace the HACK part
new_content = content.replace(
"""    if isinstance(value, sympy.Basic):
        # HACK: work around https://github.com/sympy/sympy/issues/16074
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

        class Printer(sympy.printing.repr.ReprPrinter):
            def _print(self, expr, **kwargs):
                s = super()._print(expr, **kwargs)
                if any(s.startswith(t) for t in fixed_tokens):
                    return 'sympy.' + s
                return s

        return Printer().doprint(value)""",
"""    if isinstance(value, sympy.Basic):

        class Printer(sympy.printing.repr.ReprPrinter):
            def _print(self, expr, **kwargs):
                s = super()._print(expr, **kwargs)
                if getattr(getattr(expr, '__class__', None), '__module__', '').startswith('sympy'):
                    return 'sympy.' + s
                return s

        return Printer().doprint(value)"""
)

with open('cirq-core/cirq/_compat.py', 'w') as f:
    f.write(new_content)
