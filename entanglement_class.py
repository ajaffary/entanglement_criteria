"""
First version Entangled, the entanglement criteria as a class.

An object of class Entangled initializes with the following attributes:
1. 'number_qubits', given by user input upon instantiation
2. 'statevector', a Qiskit Statevector Dictionary of size 2**number_qubits, 
    populated with np.ones() (np.zeros() will give an empty vector of length 0)
3. 'kets', a list of all bitstrings of length 'number_qubits', derived from
    statevector.keys(); list() is necessary because statevector.keys() is not
    indexable per the error:
        'TypeError: 'dict_keys' object is not subscriptable'
4. 'basis_kets', a list of all basis kets of length 'number_qubits'
5. 'non_basis_kets', a list of all non-basis kets of length 'number_qubits'
6. 'decomp_dict', a dictionary of all non-basis kets as keys and their basis ket
    decompositions as values
        - this attribute name will likely change

Example:
>>> import entanglement_class as entang
>>> x = entang.Entangled(4)
>>> x
<entanglement_class.Entangled object at 0x102a9f190>
>>> x.kets
['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001',
'1010', '1011', '1100', '1101', '1110', '1111']
>>> x.statevector
{'0000': (1+0j), '0001': (1+0j), '0010': (1+0j), '0011': (1+0j), '0100': (1+0j),
 '0101': (1+0j), '0110': (1+0j), '0111': (1+0j), '1000': (1+0j), '1001': (1+0j),
 '1010': (1+0j), '1011': (1+0j), '1100': (1+0j), '1101': (1+0j), '1110': (1+0j),
 '1111': (1+0j)}
>>> x.basis_kets
['1000', '0100', '0010', '0001']
>>> x.non_basis_kets
['0011', '0101', '0110', '0111', '1001', '1010', '1011', '1100', '1101', '1110',
 '1111']
>>> x.decomp_dict
{'0011': {'basis_kets': ['0010', '0001']}, 
 '0101': {'basis_kets': ['0100', '0001']}, 
 '0110': {'basis_kets': ['0100', '0010']}, 
 '0111': {'basis_kets': ['0100', '0010', '0001']}, 
 '1001': {'basis_kets': ['1000', '0001']}, 
 '1010': {'basis_kets': ['1000', '0010']}, 
 '1011': {'basis_kets': ['1000', '0010', '0001']}, 
 '1100': {'basis_kets': ['1000', '0100']}, 
 '1101': {'basis_kets': ['1000', '0100', '0001']}, 
 '1110': {'basis_kets': ['1000', '0100', '0010']}, 
 '1111': {'basis_kets': ['1000', '0100', '0010', '0001']}}
>>>

TODO next:
- implement methods from create_statevector.py
- create separate method to normalize statevector with zero ket amplitude = 1
"""

import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import random_statevector

class Entangled:
    def __init__(self, number_qubits) -> None:
        self.number_qubits = number_qubits
        # Initialize a nonzero Qiskit Statevector Dictionary of length 2^n
        # Use np.ones() because Statevector(np.zeros()) returns an empty list    
        self.statevector = Statevector(np.ones(2**number_qubits)).to_dict()
        self.kets = list(self.statevector.keys())
        self.basis_kets = self.powers_of_two(self.number_qubits, self.kets)
        self.non_basis_kets = self.non_basis_kets(self.basis_kets, self.kets)
        self.decomp_dict = self.non_basis_kets_dict(self.non_basis_kets, self.basis_kets)

    # https://stackoverflow.com/questions/12646326/calling-a-class-function-inside-of-init
    # define methods as method_name(self, parameters)
    # call methods inside __init__ as self.method_name(parameters)


    # Get list of powers of two in binary
    # We refer to these values as 'basis-kets'
    # inputs: 
    #   - n = length of bitstrings
    #   - kets_list = statevector.keys()
    # output: 
    #   - list of basis kets of length n powers of two from 2**0 to 2**(n-1)
    def powers_of_two(self, n, kets_list):
        return [kets_list[2**(n-1-i)] for i in range(n)]

    # Get list of non powers of two in binary (default) or decimal
    # We refer to these values as 'non-basis kets'
    # inputs:
    #   - n = number of qubits, 
    #   - powers = list of basis kets
    #   - kets = statevector.keys()
    # output: 
    #   - list of non-powers of two less than 2**(n-1)
    def non_basis_kets(self, powers, kets):
        # use statevector keys() as input and remove powers of two
        return [ket for ket in kets[1:] if ket not in powers]

    # Determine basis kets corresponding to a non-basis ket
    # Use this to reference basis kets in a Qiskit Statevector Dictionary
    # Kets are all represented by binary strings
    # inputs:    
    #   - ket = a non-basis ket of length 'n'
    #   - powers = list of all basis kets of length 'n'
    # output:
    #   - list of basis kets whose binary sum equals the non-basis ket
    def get_basis_kets(self, ket, powers):
        basis_kets = [powers[index] for index, bit in enumerate(ket) if bit == "1"]
        return basis_kets

    # Create a dictionary of non-basis kets and their corresponding basis kets
    # inputs:
    #   - list = list of non-basis kets
    #   - powers = list of all basis kets of length n
    # output:
    #   - dictionary containing:
    #       - keys: the non-basis kets from the above list
    #       - values: dictionaries initialized with a list of their corresponding 
    #                 basis kets
    def non_basis_kets_dict(self, list, powers):
        dict = {}

        for ket in list:
            basis_kets = self.get_basis_kets(ket, powers)
            dict[ket] = { 'basis_kets': basis_kets }

        return dict

        """
        can also use dictionary comprehension?
        dict = {
            ket: { 'basis_kets': self.get_basis_kets(ket, powers)}
            for ket in list }
        """

    """ above functions all go inside __init__ """

    # Compute the product of ket amplitudes
    # inputs:
    #   - statevector dictionary
    #   - list of basis kets
    # output: 
    #   - product of the amplitudes of the given basis kets
    def basis_amplitude_product(self, statevector, index_list):
        product = 1    
        for index in index_list:
            product = product*statevector[index]
        return product

    # Check equality of a non-basis ket amplitude with the product of its 
    # corresponding basis ket amplitudes, and store the results in a dictionary.
    # This can be used as a self-contained method to check the criteria on a 
    # specific ket without having to run the algorithm for all kets.
    # inputs:
    #   - a statevector dictionary
    #   - a non-basis ket
    #   - (optional) list of corresponding basis kets
    # output: 
    #   - dictionary with computed target amplitude and boolean check value
    def check_single_ket(self, statevector, ket, basis_kets=None):
        dict = {}

        if basis_kets == None:
        #   if basis kets not provided, generate them
            basis_kets = self.generate_basis_kets(ket)
            dict['basis_kets'] = basis_kets

        # get product of basis ket amplitudes
        # append result to dictionary
        dict['target_amplitude'] = self.basis_amplitude_product(statevector, basis_kets)

        # check if ket amplitude = product of basis ket amplitudes
        # append boolean result to dictionary
        dict['equality'] = statevector[ket] == dict['target_amplitude']

        # Print Statements
        def print_statements():
            product_string = self.basis_product_string(basis_kets)
            self.print_entanglement_equation(ket, product_string, dict['equality'])
            if dict['equality'] == False:
                self.print_basis_amplitudes(product_string, dict['target_amplitude'])
        
        # print_statements()
        
        return dict


    # Generate basis kets corresponding to a specific non-basis ket
    # Method 1 (binary)
    # Use with Qiskit Statevector Dictionary and function check_single_ket when a 
    #   list of basis kets is not provided
    # input:
    #   - bitstring representing a non-basis ket
    # output:
    #   - a list of bitstrings representing the corresponding basis kets
    def generate_basis_kets(self, ketstring):
        length = len(ketstring)
        basis_kets = [format(1 << (length - 1 - index) | 0, '0'+str(length)+'b')
                for index, bit in enumerate(ketstring) if bit == "1"]    
        return basis_kets


    # Print Product of basis kets Expression
    # input:
    #   - list of basis kets for a non-basis ket
    def basis_product_string(self, list):
        product = "Psi['"+list[0]+"']"
        for index in list[1:]:
            product = product + "*Psi['"+index+"']"
        return product

    # Print Product of basis kets Amplitude
    # input:
    #   - kets = text string reference to product of a list of basis ket amplitudes
    #   - amplitude = the numerical value of the product of the amplitudes
    def print_basis_amplitudes(self, kets, amplitude):
        print(kets + " = " + str(amplitude))

    # Print non-basis ket amplitude
    # inputs:
    #   - ket = text string reference to a non-basis ket amplitude
    #   - amplitude = numerical value of amplitude
    def print_ket_amplitude(self, ket, amplitude):
        print("Psi['"+ket+"'] = " + str(amplitude))


    # Print True/False check statement
    # inputs: 
    #   - non-basis ket
    #   - product of basis ket string
    #   - boolean check value
    def print_entanglement_equation(self, ket, basis_elements, bool):
        print("Psi['"+ket+"']" + " == " + basis_elements + " is " + str(bool))


    # Entanglement Function
    # input:
    #   - statevector = Qiskit Statevector Dictionary
    # output:
    #   - dict = dictionary, where:
    #       - keys: all non-basis kets in the statevector
    #       - values: dictionaries containing:
    #           - corresponding basis kets
    #           - target amplitude (product of basis ket amplitudes) 
    #           - boolean equality check
    #   - print statement indicating whether or not the state is Entangled
    def entangled(self, statevector):
        # create fresh copy of decomp_dict for given statevector
        dict = self.decomp_dict

        # initalize set of booleans
        booleans = set()

        # apply entanglement criteria for each ket
        for ket in dict:
            # get results from check single ket
            ket_results = self.check_single_ket(
                statevector, 
                ket, 
                dict[ket]['basis_kets']
                )
            # update dictionary with results
            # faster way to do this?  items()?
            dict[ket]['target_amplitude'] = ket_results['target_amplitude']
            dict[ket]['equality'] = ket_results['equality']

            booleans.add(dict[ket]['equality'])

        # conclusion
        if False in booleans:
            print("|Psi> is Entangled")
        else:
            print("|Psi> is not Entangled")

        return dict

