import sympy
class Printer(sympy.printing.repr.ReprPrinter):
    def _print(self, expr, **kwargs):
        s = super()._print(expr, **kwargs)
        # s is a string like "Mul(Integer(3), Symbol('t'))"
        # Since it's recursively generated, `s` might be just "Integer(3)"
        # How do we prefix the module dynamically instead of using `fixed_tokens`?

        # In fact, we want to know if the string returned by `super()._print(expr, **kwargs)`
        # begins with the expression's class name, and if that class name is part of the `sympy` module.
        # But wait, what if it's `pi`? `pi` is a singleton. `type(sympy.pi).__name__` is `Pi`.
        # But it prints as `pi`.

        # `fixed_tokens` is a hack because it hardcodes names.
        # Instead of `any(s.startswith(t) for t in fixed_tokens): return 'sympy.' + s`
        # We can just check if the class is defined in `sympy` module. But `pi` prints as `pi`,
        # not `Pi(...)`.

        # What if we just parse the module from `expr.__class__.__module__`?
        if getattr(expr.__class__, "__module__", "").startswith("sympy"):
            # We want to prepend 'sympy.' to `s` only if `s` is the "bare" name, not if it's already qualified.
            # But wait, `s` is already recursively formatted, so its arguments might have `sympy.` but the top level doesn't.
            # Actually, `sympy.srepr` output doesn't have `sympy.` anywhere.

            # The hack prepends 'sympy.' to anything that *starts* with one of the fixed_tokens.
            # E.g. if s="Mul(Integer(3), Symbol('t'))", it starts with "Mul", so it prepends "sympy." -> "sympy.Mul(Integer(3), Symbol('t'))"
            # But wait! If it does this recursively, then it returns "sympy.Mul(sympy.Integer(3), sympy.Symbol('t'))"!
            pass

    def emptyPrinter(self, expr):
        if getattr(expr.__class__, "__module__", "").startswith("sympy"):
            return "sympy." + super().emptyPrinter(expr)
        return super().emptyPrinter(expr)

# Let's inspect what `getattr(expr.__class__, "__module__", "")` returns.
