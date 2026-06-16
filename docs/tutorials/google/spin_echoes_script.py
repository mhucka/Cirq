##### Copyright 2021 The Cirq Developers

# @title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import cirq
except ImportError:
    print("installing cirq...")
    !pip install --quiet cirq
    print("installed cirq.")

import matplotlib.pyplot as plt
import numpy as np

import cirq
import cirq_google as cg

import os

# The Google Cloud Project id to use.
project_id = ''  # @param {type:"string"}
processor_id = ""  # @param {type:"string"}

from cirq_google.engine.qcs_notebook import get_qcs_objects_for_notebook

device_sampler = get_qcs_objects_for_notebook(project_id, processor_id)

# @markdown Helper functions.
from typing import Sequence
from cirq.experiments import random_rotations_between_grid_interaction_layers_circuit

# Gates for spin echoes.
pi_pulses = [cirq.PhasedXPowGate(phase_exponent=p, exponent=1.0) for p in (-0.5, 0.0, 0.5, 1.0)]


def create_benchmark_circuit(
    qubits: Sequence[cirq.GridQubit],
    cycles: int,
    twoq_gate: cirq.Gate = cirq.SQRT_ISWAP,
    seed: int | None = None,
    with_optimization: bool = False,
    with_alignment: bool = False,
    with_spin_echoes: bool = False,
) -> cirq.Circuit:
    """Returns an "OTOC-like" circuit [1] used to benchmark optimization and/or
    alignment and/or spin echoes.

    Args:
        qubits: Qubits to use.
        cycles: Depth of random rotations in the forward & reverse unitary.
        twoq_gate: Two-qubit gate to use.
        seed: Seed for circuit generation.
        with_optimization: Run a series of optimizations on the circuit.
        with_alignment: Align moments and synchronize terminal measurements.
        with_spin_echoes: Insert spin echoes on ancilla qubit.

    References:
        [1] Fig. S10 of https://arxiv.org/abs/2101.08870.
    """
    ancilla, qubits = qubits[0], qubits[1:]

    # Put ancilla into the |1⟩ state and couple it to the rest of the qubits.
    excite_ancilla = [cirq.X(ancilla), twoq_gate(ancilla, qubits[0])]

    # Forward operations.
    forward = random_rotations_between_grid_interaction_layers_circuit(
        qubits,
        depth=cycles,
        two_qubit_op_factory=lambda a, b, _: twoq_gate.on(a, b),
        pattern=cirq.experiments.GRID_STAGGERED_PATTERN,
        single_qubit_gates=[
            cirq.PhasedXPowGate(phase_exponent=p, exponent=0.5) for p in np.arange(-1.0, 1.0, 0.25)
        ],
        seed=seed,
    )

    # Full circuit. Note: We are intentionally creating a bad circuit structure
    # by putting each operation in a new moment (via `cirq.InsertStrategy.New`)
    # to show the advantages of optimization & alignment.
    circuit = cirq.Circuit(excite_ancilla)
    circuit.append(forward.all_operations(), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.inverse(forward).all_operations(), strategy=cirq.InsertStrategy.NEW)
    circuit.append(cirq.inverse(excite_ancilla[1:]))
    circuit.append(cirq.measure(ancilla, key="z"), strategy=cirq.InsertStrategy.NEW)

    # Run optimization.
    if with_optimization:
        circuit = cirq.optimize_for_target_gateset(circuit, gateset=cirq.SqrtIswapTargetGateset())
        circuit = cirq.eject_phased_paulis(circuit)
        circuit = cirq.eject_z(circuit)
        circuit = cirq.drop_negligible_operations(circuit)
        circuit = cirq.drop_empty_moments(circuit)

    # Insert spin echoes. Note: It's important to do this after optimization, as
    # optimization will remove spin echoes.
    if with_spin_echoes:
        random_state = np.random.RandomState(seed)

        spin_echo = []
        for _ in range(cycles * 2):
            op = random_state.choice(pi_pulses).on(ancilla)
            spin_echo += [op, cirq.inverse(op)]

        circuit.insert(2, spin_echo)

    # Alignment.
    if with_alignment:
        circuit = cirq.align_right(circuit)
        circuit = synchronize_terminal_measurements(circuit)

    return circuit


def to_survival_prob(result: cirq.Result) -> float:
    return np.mean(np.sum(result.measurements["z"], axis=1) == 1)

"""Create an example circuit."""

qubits = cirq.GridQubit.rect(
    2, 3
)  # [cirq.GridQubit(x, y) for (x, y) in [(3, 2), (4, 2), (4, 1), (5, 1), (6, 1), (6, 2), (5, 2)]]
circuit = create_benchmark_circuit(qubits, twoq_gate=cirq.ISWAP, cycles=3, seed=1)

print("Example benchmark circuit:\n")
circuit

"""Without noise, only the 1 state is measured."""

result = cirq.Simulator().run(circuit, repetitions=1000)
result.histogram(key="z")

# Create an Engine object to use.
spec = cg.Engine(project_id).get_processor(processor_id).get_device_specification()

# Iterate through each gate set valid on the device.
for gateset in spec.valid_gate_sets:
    print(gateset.name)
    print('-------')
    # Prints each gate valid in the set with its duration
    for gate in gateset.valid_gates:
        print('%s %d' % (gate.id, gate.gate_duration_picos))
    print()

circuit = cirq.optimize_for_target_gateset(circuit, gateset=cirq.SqrtIswapTargetGateset())
circuit

"""Compile an arbitrary two-qubit operation to the sqrt_iswap gateset."""

ops = cirq.two_qubit_matrix_to_sqrt_iswap_operations(
    q0=qubits[0], q1=qubits[1], mat=cirq.testing.random_unitary(dim=4, random_state=1)
)
cirq.Circuit(ops)

circuit = cirq.eject_phased_paulis(circuit)
circuit

circuit = cirq.eject_z(circuit)
circuit

left_aligned_circuit = cirq.align_left(circuit)
left_aligned_circuit

print(f"Original circuit has {len(circuit)} moments.")
print(f"Aligned circuit has {len(left_aligned_circuit)} moments.")

right_aligned_circuit = cirq.align_right(circuit)
right_aligned_circuit

circuit = cirq.stratified_circuit(
    circuit, categories=[lambda op: len(op.qubits) == 1, lambda op: len(op.qubits) == 2]
)
circuit

circuit = cirq.drop_negligible_operations(circuit)
circuit = cirq.drop_empty_moments(circuit)
circuit

circuit = cirq.synchronize_terminal_measurements(circuit)
circuit

# Gates for spin echoes. Note that these gates are self-inverse.
pi_pulses = [cirq.PhasedXPowGate(phase_exponent=p, exponent=1.0) for p in (-0.5, 0.0, 0.5, 1.0)]

# Generate spin echoes on ancilla.
num_echoes = 3
random_state = np.random.RandomState(1)

spin_echo = []
for _ in range(num_echoes):
    op = random_state.choice(pi_pulses).on(qubits[0])
    spin_echo += [op, cirq.inverse(op)]

# Insert spin echo operations to circuit.
optimized_circuit_with_spin_echoes = circuit.copy()
optimized_circuit_with_spin_echoes.insert(5, spin_echo)

# Align single-qubit spin echo gates into other moments of single-qubit gates.
optimized_circuit_with_spin_echoes = cirq.stratified_circuit(
    optimized_circuit_with_spin_echoes,
    categories=[lambda op: len(op.qubits) == 1, lambda op: len(op.qubits) == 2],
)
optimized_circuit_with_spin_echoes

"""Set experiment parameters."""

qubits = cg.line_on_device(device_sampler.device, length=7)
cycle_values = range(0, 100 + 1, 4)
nreps = 20_000
seed = 1

circuit = create_benchmark_circuit(qubits, cycles=2, seed=1)
print(f"Unoptimized circuit ({len(circuit)} moments):\n")
circuit

optimized_circuit = create_benchmark_circuit(
    qubits, cycles=2, seed=1, with_optimization=True, with_alignment=True
)
print(f"Circuit with optimization + alignment ({len(optimized_circuit)} moments):\n")
optimized_circuit

optimized_circuit_with_spin_echoes = create_benchmark_circuit(
    qubits, cycles=2, seed=1, with_optimization=True, with_alignment=True, with_spin_echoes=True
)
print(
    f"Circuit with optimization + alignment + spin echoes ({len(optimized_circuit_with_spin_echoes)} moments):\n"
)
optimized_circuit_with_spin_echoes

"""Create all circuits."""

batch = [create_benchmark_circuit(qubits, cycles=c, seed=seed) for c in cycle_values]
batch_with_optimization = [
    create_benchmark_circuit(
        qubits, cycles=c, seed=seed, with_optimization=True, with_alignment=True
    )
    for c in cycle_values
]
batch_with_optimization_and_spin_echoes = [
    create_benchmark_circuit(
        qubits,
        cycles=c,
        seed=seed,
        with_optimization=True,
        with_alignment=True,
        with_spin_echoes=True,
    )
    for c in cycle_values
]

"""Run all circuits."""

all_probs = []
for b in (batch, batch_with_optimization, batch_with_optimization_and_spin_echoes):
    results = device_sampler.sampler.run_batch(b, repetitions=nreps)
    all_probs.append([to_survival_prob(*res) for res in results])

"""Plot results."""

labels = ["Unoptimized", "Optimization + Alignment", "Optimization + Alignment + Spin echoes"]

for probs, label in zip(all_probs, labels):
    plt.plot(cycle_values, probs, "-o", label=label)

plt.xlabel("Cycles")
plt.ylabel("Survival probability")
plt.legend();
