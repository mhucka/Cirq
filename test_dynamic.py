import sympy

class Printer(sympy.printing.repr.ReprPrinter):
    def _print(self, expr, **kwargs):
        s = super()._print(expr, **kwargs)
        # Instead of fixed tokens, just check if the expression's module starts with 'sympy.'
        # and if `s` doesn't already start with a quote (e.g. for strings) or a number (e.g. if it's evaluated to a primitive some day? actually sympy objects are all objects).

        # In `cirq`, they use `fixed_tokens` to whitelist things that get `sympy.` prepended.
        # Why not just whitelist everything whose module is `sympy`?

        mod = getattr(expr.__class__, "__module__", "")
        if mod.startswith("sympy") or mod == "sympy":
            # Just to be safe, don't prefix if it already has 'sympy.'
            # Wait, what does `s` look like? For a Symbol, it's `Symbol('t')`.
            # For pi, it's `pi`.
            # We want to prepend `sympy.` so it evaluates using `import sympy`.

            # The only caveat is if `s` is something that shouldn't be prefixed?
            return "sympy." + s

        return s

v = sympy.Symbol('t') * 3
print("With dynamic lookup:", Printer().doprint(v))
