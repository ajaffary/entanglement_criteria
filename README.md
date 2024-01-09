# entanglement_criteria
This project utilizes the [IBM Qiskit Statevector class](https://docs.quantum.ibm.com/api/qiskit/qiskit.quantum_info.Statevector)

Please see the comments in `entangled.py` and `create_statevector.py` for a summary of this project.

`entanglement_criteria_third_draft.ipynb` is a Jupyter Notebook with test runs of the functions from `entangled.py`, and also contains a detailed description of the project.  It contains slightly older code.

`entanglement_class.py` is a new module with a class `Entangled`.  This incorporates and updates code from the above two modules.
I have elected to only work with binary string representations of kets, so I've abandoned the decimal index versions of any functions, and removed references to an optional `base=10` parameter and the associated 'if/else' statements.  This means the algorithm only works with Qiskit Statevector Dictionaries.  I have not built in an exception to check for this before running the `entangled()` method.

Documentation inside `entanglement_class.py` describes the current structure, and provides examples of its methods.
