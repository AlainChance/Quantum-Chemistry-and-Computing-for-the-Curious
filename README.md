# Quantum-Chemistry-and-Computing-for-the-Curious
Quantum Chemistry and Computing for the Curious: Illustrated with Python and Qiskit® code" Packt (2022), https://a.co/d/hIVmgQl

This repository contains companion Jupyter notebooks of the book that have been successfully run with the following Qiskit versions:
- Qiskit v1.3
- Qiskit v2.0

We provide a work-in-progress version (V4) of the companion Jupyter notebooks for the following chapters: 
- Chapter 4: `Chapter_04_Molecular_Hamiltonians_V4.ipynb`
- Chapter 5: `Chapter_05_Variational_Quantum_Eigensolver_(VQE)_algorithm_V4.ipynb`.

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

The TAR archive file contains a set of customized files that are needed/used in the Jupyter notebooks for Chapter 4 and Chapter 5. Under your own risk, you can adapt the following list of commands to your specific installation and execute them:

```bash
cp -r $HOME/qiskit_algorithms/*.* $HOME/miniconda3/lib/python3.12/site-packages/qiskit_algorithms/

cp -r $HOME/primitives/*.* $HOME/miniconda3/lib/python3.12/site-packages/qiskit/primitives
cp -r $HOME/primitives_V1/*.* $HOME/miniconda3/lib/python3.12/site-packages/qiskit/primitives

cp $HOME/providers/backend.py $HOME/miniconda3/lib/python3.12/site-packages/qiskit/providers/

cp - r $HOME/qiskit_nature/*.* $HOME/miniconda3/lib/python3.12/site-packages/qiskit_nature/
```

A boolean `qv1` is set to `True` if the version of Qiskit is less than 2.0:
```
import qiskit
qv = qiskit.__version__
print(f"Qiskit version: {qv}")
qv1 = int(qv[0]) < 2
```

The shared variable `primitive_v2` is set in the file `primitive_version.py` as follows (customize according to your specific installation path):
```python
# Open the file in write mode
with open("primitive_version.py", "w") as file:
    # Write a single line to the file
    if qv1:
        file.write("primitive_v2 = False")
    else:
        file.write("primitive_v2 = True")

!cp primitive_version.py $HOME/miniconda3/lib/python3.12/site-packages/qiskit_algorithms/
```
It then imports it in the code cell that follows `Import various algorithms with the following commands`:
```
from qiskit_algorithms.primitive_version import primitive_v2
```
The shared variable `primitive_v2` is imported in a number of Python files, see below example: 

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
