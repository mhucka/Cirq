import json

with open('docs/tutorials/google/spin_echoes.ipynb', 'r') as f:
    notebook = json.load(f)

for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        for i, line in enumerate(cell['source']):
            if 'cirq.MergeInteractionsToSqrtIswap().optimize_circuit(circuit)' in line:
                cell['source'][i] = line.replace('cirq.MergeInteractionsToSqrtIswap().optimize_circuit(circuit)', 'circuit = cirq.optimize_for_target_gateset(circuit, gateset=cirq.SqrtIswapTargetGateset())')
    elif cell['cell_type'] == 'markdown':
        for i, line in enumerate(cell['source']):
            if '`cirq.MergeInteractionsToSqrtIswap` optimizer' in line:
                cell['source'][i] = line.replace('`cirq.MergeInteractionsToSqrtIswap` optimizer', '`cirq.optimize_for_target_gateset` transformer with `cirq.SqrtIswapTargetGateset()`').replace('This optimizer merges', 'This transformer merges')

with open('docs/tutorials/google/spin_echoes.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
