# Quantum-Chemistry-and-Computing-for-the-Curious
**Updated, work-in-progress code repository** for the book
[*Quantum Chemistry and Computing for the Curious: Illustrated with Python and Qiskit® Code*](https://a.co/d/hIVmgQl) (Packt, 2022), derived from the original Packt Publishing repository:
[PacktPublishing/Quantum-Chemistry-and-Computing-for-the-Curious](https://github.com/PacktPublishing/Quantum-Chemistry-and-Computing-for-the-Curious).

This repository contains companion Jupyter notebooks of the book that have been successfully run with Qiskit v1.3, Qiskit v2.0, Qiskit v2.1 and the Qiskit Runtime V2 primitives:
- Chapter 3: `Chapter_03_Quantum_circuit_model_of_computation_V3.ipynb`
- Chapter 4: `Chapter_04_Molecular_Hamiltonians_V4.ipynb`
- Chapter 5: `Chapter_05_Variational_Quantum_Eigensolver_(VQE)_algorithm_V4.ipynb`.

We provide a work-in-progress version (V4) of the companion Jupyter notebooks for chapters 4 and 5.

Please refer to the following documentation:
- Migrate to the Qiskit Runtime V2 primitives, https://docs.quantum.ibm.com/migration-guides/v2-primitives
- StatevectorSampler, https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.StatevectorSampler
- StatevectorEstimator, https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.StatevectorEstimator

V2 primitives do not perform layout, routing, and translation operations. See the transpilation documentation for instructions to transform circuits.

**Qiskit Algorithms** is no longer officially supported by IBM. Work is in progress to adapt the whole code base to support V2 primitives and ISA circuits:

- Added V2 and ISA support #197, 🔗https://github.com/qiskit-community/qiskit-algorithms/pull/197
- HamiltonianPhaseEstimation class — Issue #204, 🔗https://github.com/qiskit-community/qiskit-algorithms/issues/204

**Warning**

Like any other Apache 2 licensed code, you are free to use `qiskit_algorithms`, `qiskit_nature`, `qiskit/primitives`, and `qiskit/providers` libraries or/and extend them, but please be aware that it is under your own risk. 

See disclaimer in readme, 🔗 https://github.com/qiskit-community/qiskit-algorithms?tab=readme-ov-file#qiskit-algorithms

**Temporary fix**

In this GitHub repository you will find three TAR archive files containing a set of customized files that are needed/used in the Jupyter notebooks for Chapter 4 and Chapter 5. 

* qiskit.tar
* qiskit_algorithms.tar
* qiskit_nature.tar

Under your own risk, you can adapt and then run the `Copy_V4.ipynb` notebook which executes the `Copy_V4.py` script.

```bash
%run Copy_V4
```

The `Copy_V4.py` Python script sets a boolean `qv1` to `True` if the version of Qiskit is less than 2.0:
```
import qiskit
qv = qiskit.__version__
print(f"Qiskit version: {qv}")
qv1 = int(qv[0]) < 2
```

The shared variable `primitive_v2` is set in the file `primitive_version.py` as follows (customize according to your specific installation path):
```python
#------------------------
# Get site_packages path
#------------------------
import site
sitepackages = site.getsitepackages()

#---------------------------------------------------
# Write primitive_version.py into qiskit_algorithms
#---------------------------------------------------
with open(sitepackages[0] + '/qiskit_algorithms/primitive_version.py', "w") as file:
    # Write a single line to the file
    if qv1:
        file.write("primitive_v2 = False")
    else:
        file.write("primitive_v2 = True")

```
It then imports it in the code cell that follows `Import various algorithms with the following commands`:
```
from qiskit_algorithms.primitive_version import primitive_v2
```
The shared variable `primitive_v2` is imported in a number of Python files, see below examples. 

`qiskit_algorithms/minimum_eigensolvers/vqe.py`
```
from qiskit_algorithms.primitive_version import primitive_v2

# If version 2 of the Qiskit Runtime primitives
if primitive_v2:
    from qiskit.primitives import BaseEstimatorV2 as BaseEstimator, StatevectorEstimator
    print("\nvqe - Using Qiskit Runtime V2 primitives")
else:
    from qiskit.primitives import BaseEstimatorV1 as BaseEstimator, EstimatorResult
    from qiskit.primitives.estimator import Estimator
    print("\nvqe - Using Qiskit Runtime V1 primitives")
```
