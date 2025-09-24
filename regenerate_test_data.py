import importlib
import pathlib
import sys

import cirq
import numpy as np
import pandas as pd
import sympy

def main():
    """Regenerates test data for a given file."""
    filepath = sys.argv[1]

    # Read the content of the file
    content = pathlib.Path(filepath).read_text()

    # Create a dictionary of imports for eval
    imports = {
        'cirq': cirq,
        'cirq_aqt': importlib.import_module('cirq_aqt'),
        'cirq_google': importlib.import_module('cirq_google'),
        'cirq_ionq': importlib.import_module('cirq_ionq'),
        'cirq_pasqal': importlib.import_module('cirq_pasqal'),
        'datetime': importlib.import_module('datetime'),
        'nx': importlib.import_module('networkx'),
        'np': np,
        'pd': pd,
        'sympy': sympy,
    }

    # Evaluate the content of the file
    obj = eval(content, imports)

    # Print the new repr and json
    print("New repr:")
    print(repr(obj))
    print("\nNew json:")
    print(cirq.to_json(obj))

if __name__ == '__main__':
    main()
