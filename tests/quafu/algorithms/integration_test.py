# (C) Copyright 2023 Beijing Academy of Quantum Information Sciences
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from quafu.algorithms import Hamiltonian, QAOACircuit, Estimator
from quafu import simulate
from scipy.optimize import minimize


class TestQAOA:
    """Example of a QAOA algorithm to solve maxcut problem"""

    def test_run(self):
        """
        A simple graph with 5 nodes and connected as below
            a -> b -> c
            d ---^
            e ---^
        """
        num_layers = 2
        hamlitonian = Hamiltonian.from_pauli_list(
            [("IIIZZ", 1), ("IIZIZ", 1), ("IZIIZ", 1), ("ZIIIZ", 1)]
        )
        ref_mat = np.load("tests/quafu/algorithms/test_hamiltonian.npy")
        assert np.array_equal(ref_mat, hamlitonian.get_matrix())
        ansatz = QAOACircuit(hamlitonian, num_layers=num_layers)
        ansatz.draw_circuit()

        def cost_func(params, ham, estimator: Estimator):
            beta = params[:num_layers]
            gamma = params[num_layers:]
            cost = estimator.run(ham, beta, gamma)
            return cost

        est = Estimator(ansatz)
        params = 2 * np.pi * np.random.rand(num_layers * 2)
        res = minimize(cost_func, params, args=(hamlitonian, est), method="COBYLA")
        print(res)
        ansatz.measure(list(range(5)))
        ansatz.draw_circuit()
        probs = simulate(ansatz).probabilities
        print(probs)
