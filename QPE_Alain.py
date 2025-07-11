#-------------------------------------------------------------------------------------------
## MIT License

# Copyright (c) 2025 Alain Chancé

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#--------------------------------------------------------------------------------

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
import qiskit_aer
from qiskit_aer import AerSimulator

#------------------------------------------
# Define function qft_dagger (inverse QFT)
#------------------------------------------
def qft_dagger(circuit, n):
    """Apply inverse QFT on the first n qubits."""
    for j in range(n//2):
        circuit.swap(j, n - j - 1)
    for j in range(n):
        for k in range(j):
            circuit.cp(-np.pi / float(2**(j - k)), k, j)
        circuit.h(j)
    return circuit

#---------------------------------------
# Define function construct_qpe_circuit
#---------------------------------------
def construct_qpe_circuit(unitary: QuantumCircuit, n_count: int) -> QuantumCircuit:
    """Build QPE circuit for a given unitary and number of counting qubits.
    
    Args:
        unitary: QuantumCircuit acting on 1 or more qubits.
        n_count: Number of counting qubits (precision bits).
    
    Returns:
        QuantumCircuit: full QPE circuit.
    """
    n_unitary = unitary.num_qubits
    qc = QuantumCircuit(n_count + n_unitary, n_count)

    # Step 1: Apply Hadamard to counting qubits
    qc.h(range(n_count))

    # Step 2: Prepare the eigenstate (here assumed to be |1...0⟩ for example)
    qc.x(n_count + n_unitary - 1)  # Apply X to last target qubit

    # Step 3: Apply controlled-U^{2^j} operations
    for i in range(n_count):
        # Repeat unitary 2^i times (power of 2)
        repetitions = 2 ** i
        controlled_u = unitary.copy()
        for _ in range(repetitions - 1):
            controlled_u = controlled_u.compose(unitary)

        controlled_u = controlled_u.control()  # Make it controlled

        # Apply controlled-U^{2^i} from counting qubit i
        qc.append(controlled_u, [i] + list(range(n_count, n_count + n_unitary)))

    # Step 4: Apply inverse QFT to counting qubits
    qft_dagger(qc, n_count)

    # Step 5: Measure counting qubits
    qc.measure(range(n_count), range(n_count))

    return qc

#----------------------------------------------------------------------------------------------------
# Define function binary_fraction_to_decimal
# To convert a **binary string representing a fractional number** 
# (e.g., using bits like `'111'` for $\frac{1}{2} + \frac{1}{4} + \frac{1}{8}$) into a decimal value, 
# we use the formula:
# $$
# \text{value} = \sum_{i=1}^{n} \frac{b_i}{2^i}
# $$
# Where $b_i$ is the $i$th bit from the binary string.
#----------------------------------------------------------------------------------------------------
def binary_fraction_to_decimal(bitstring):
    return sum(int(bit) / 2**(i + 1) for i, bit in enumerate(bitstring))

#----------------------------------------------------------------------------------------------------
# Define function do_qpe - Qiskit v2.1 compatible
# The class qiskit.circuit.library.phase_estimation.PhaseEstimation is deprecated as of Qiskit 2.1. 
# It will be removed in Qiskit 3.0. Use qiskit.circuit.library.phase_estimation instead.
# https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.PhaseEstimation
#----------------------------------------------------------------------------------------------------
aer_sim = AerSimulator(method='statevector')

def do_qpe(unitary, nqubits=3, show=False):
    # Construct the QPE circuit
    qpe_circuit = construct_qpe_circuit(unitary, n_count= nqubits)
        
    # Transpile for the Aer simulator
    new_circuit = transpile(qpe_circuit, aer_sim)

    # Execute the circuit
    job = aer_sim.run(new_circuit, shots=1000)
    result = job.result()

    # Get measurement counts
    counts = result.get_counts(qpe_circuit)

    # Extract the most likely output
    max_key = max(counts, key=counts.get)

    # Convert binary output to decimal phase
    phase_out = binary_fraction_to_decimal(max_key)
        
    if show:
        print("Number of qubits: {}, QPE phase estimate: {}".format(nqubits, phase_out))
        
    return phase_out

#-------------------------------------------------------------------
# Compute the ground state energy of the hydrogen molecule from QPE
#-------------------------------------------------------------------
from qiskit.circuit.library import UnitaryGate
from scipy.linalg import expm

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.circuit.library import HartreeFock

def run_qpe(problem, n_ancillae, show=True):
    hamiltonian = problem.hamiltonian.second_q_op()
    mapper = ParityMapper(num_particles=problem.num_particles)
    tapered_mapper = problem.get_tapered_mapper(mapper)
    qubit_op = tapered_mapper.map(hamiltonian)
    
    unitary = HartreeFock(problem.num_spatial_orbitals,problem.num_particles,mapper)
    U = UnitaryGate(expm(1j*qubit_op.to_matrix()))
    unitary.compose(U, inplace=True)
    
    phase = do_qpe(unitary, nqubits=n_ancillae)
    result = (phase-1.0) * 2*np.pi

    if show:
        print(f'Ground state energy from QPE: {result} Ha')
  
    return result