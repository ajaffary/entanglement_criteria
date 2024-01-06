# entanglement_criteria
Please see the comments in `entangled.py` and `create_statevector.py` for a summary of this project.

`entanglement_criteria_third_draft.ipynb` is a Jupyter Notebook with test runs of the functions from `entangled.py`, and also contains a detailed description of the project.  It may contain slightly older code.

Next steps:
- rewrite the `entangled.py` module as a class
  - we should store a list of basis kets (for a few different string lengths 'n') that can be referenced when we run the algorithm, instead of generating them every time
- rewrite `create_statevector.py` as a class?
   - I don't know that this is necessary since we are not storing any data
   - I will add a 'normalization' function that scales all amplitudes of a given statevector so that the zero ket has amplitude '1'
   - we need to implement the basis change transformation in this module
 
All of the above utilizes the [IBM Qiskit Statevector class](https://docs.quantum.ibm.com/api/qiskit/qiskit.quantum_info.Statevector)
