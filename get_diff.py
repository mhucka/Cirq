with open('cirq-core/cirq/_compat.py', 'r') as f:
    print(f.read().find('class Printer(sympy.printing.repr.ReprPrinter):'))
