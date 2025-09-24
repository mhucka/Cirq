import cirq
import cirq_ionq

program = cirq_ionq.SerializedProgram(
    input={'gateset': 'qis', 'qubits': 1, 'circuit': []},
    settings={},
    metadata={},
    compilation={},
    error_mitigation={},
    noise={},
    dry_run=False,
)

print("repr:")
print(repr(program))

print("\njson:")
print(cirq.to_json(program))
