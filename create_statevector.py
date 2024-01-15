"""
This module contains two functions to generate IBM Qiskit Statevector 
Dictionaries specifically of length 2**n, for `n` qubits.

Qiskit Statevectors Dictionaries are indexed by bitstrings that represent kets 
in a Statevector.  The bitstrings are required for the Entanglement Criteria 
algorithm.

The function get_amplitudes() generates statevectors via user input.

The function normalized_random_statevector() generates random statevectors and
normalizes the zero ket amplitiude to 1.

See (Qiskit Statevector documentation)
See (Entanglement Criteria module)
"""

import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import random_statevector

# Initialize a nonzero Qiskit Statevector Dictionary
# use np.ones() because Statevector(np.zeros()) returns an empty list    
def init_statevector(number_qubits: int) -> dict:
    return Statevector(np.ones(2**number_qubits)).to_dict()

# Get amplitude of single ket via user input
def get_amplitude(key: str, recursive=False):
    """ get a complex number from user input
    """
    # checks if user input is a number
    if recursive:
        message = f"Error: amplitude for {key} must be a number: "
    else:
        message = f"Enter an amplitude for {key}: "
    
    # get user input
    amplitude = input(message)
    
    # empty user input defaults to '0' amplitude
    if amplitude == "":
        amplitude = 0

    # convert user input to complex number type
    try:
        amplitude = complex(amplitude)
    except ValueError:
        return get_amplitude(key, True)
    
    return amplitude

# Get amplitudes for each ket in Qiskit Statevector Dictionary
def get_amplitudes(number_qubits: int):
    """ Populate a Qiskit Statevector dictionary values with amplitudes via
    user input
    """
    # initalize new statevector dictionary
    statevector = init_statevector(number_qubits)

    # Update ket amplitudes
    for key in statevector.keys():
        statevector[key] = get_amplitude(key)

    return statevector


# Random Statevector Dictionary with normalized zero ket
# TODO: implement the normalization step in the general
#       algorithm per the Entanglement Criteria
def normalize_random_statevector(n):
    # generate Qiskit random statevector of dim 2**n
    random_state = random_statevector(2**n, None)

    # Normalize zero ket to have amplitude = 1
    normalized_random_state = random_state/random_state[0]

    # Convert normalized Statevector to dictionary:
    statevector = normalized_random_state.to_dict()

    return statevector

# Test statevector of length 16 with zero ket amplitude = 0 to test 
# basis change methods
def test_statevector():
    amplitudes = [0, 2, 3, 5, 0, 7, 8, 9, 0, 11, 0, 13, 17, 19, 0, 1]
    x = init_statevector(4)

    for index in range(len(amplitudes)):
        x[list(x.keys())[index]] = amplitudes[index]
    return x
