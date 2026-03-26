# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import networkx as nx
import pytest

import cirq
import cirq.contrib.acquaintance as cca


@pytest.mark.parametrize(
    'circuit_dag,sorted_nodes',
    [
        (dag, tuple(cca.random_topological_sort(dag)))
        for dag in [
            cirq.contrib.CircuitDag.from_circuit(cirq.testing.random_circuit(10, 10, 0.5))
            for _ in range(5)
        ]
        for _ in range(5)
    ],
)
def test_topological_sort(circuit_dag, sorted_nodes) -> None:
    sorted_nodes = list(sorted_nodes)
    assert cca.is_topologically_sorted(circuit_dag, (node.val for node in sorted_nodes))

    assert not cca.is_topologically_sorted(circuit_dag, (node.val for node in sorted_nodes[:-1]))

    assert not cca.is_topologically_sorted(
        circuit_dag, (node.val for node in sorted_nodes + sorted_nodes[:2])
    )

    v, w = next(iter(circuit_dag.edges))
    i = sorted_nodes.index(v)
    j = sorted_nodes.index(w, i + 1)
    sorted_nodes[i], sorted_nodes[j] = sorted_nodes[j], sorted_nodes[j]

    assert cca.is_topologically_sorted(circuit_dag, (node.val for node in sorted_nodes)) == (
        v.val == w.val
    )


def test_random_topological_sort_properties():
    # Empty graph
    dag = nx.DiGraph()
    assert list(cca.random_topological_sort(dag)) == []

    # Single node
    dag = nx.DiGraph()
    dag.add_node(1)
    assert list(cca.random_topological_sort(dag)) == [1]

    # Disconnected components
    dag = nx.DiGraph()
    dag.add_edge(1, 2)
    dag.add_edge(3, 4)
    for _ in range(10):
        result = list(cca.random_topological_sort(dag))
        assert set(result) == {1, 2, 3, 4}
        assert result.index(1) < result.index(2)
        assert result.index(3) < result.index(4)

    # Randomness: two independent nodes should appear in either order
    dag = nx.DiGraph()
    dag.add_node(1)
    dag.add_node(2)
    results = set()
    for _ in range(100):
        results.add(tuple(cca.random_topological_sort(dag)))
    assert results == {(1, 2), (2, 1)}

    # Larger DAG
    dag = nx.DiGraph([(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)])
    for _ in range(10):
        result = list(cca.random_topological_sort(dag))
        assert len(result) == 5
        assert set(result) == set(range(5))
        for u, v in dag.edges:
            assert result.index(u) < result.index(v)
