"""
Definitions:
- 'basis kets' are any bitstrings with a single '1' only
- A basis ket with a '1' at index 'i' is referred to as 'e_i'
- 'non-basis kets' are bitstrings with '1' occuring in at least two places

Logic:
- Given a Statevector Dictionary, separate all kets into basis kets and 
non-basis kets
- For each non-basis ket, decompose it into its corresponding basis kets
    and apply the Entanglement Criteria
- Output the result:  whether or not the Statevector is Entangled

Implementation:
- basis kets are bitstring representations of powers of 2.  non-basis kets 
are bitstring representations of all other integers.  A 'decomposition' of a
non-basis ket into basis kets means expressing any integer that is not a
power of two into a sum of integers that are powers of two, e.g. the integer:
    13 = 8 + 4 + 1
corresponds to:
    1101 = 1000 + 0100 + 0001
in binary.
- the input to the algorithm must be a Qiskit Statevector of length 2**n,
    corresponding to a linear combination of all possible n-qubit states
- the algorithm can be implemented two ways:
    1. use Qiskit Statevector Dictionary.  this is my preferred method.
        Statevector Dictionary uses bitstrings as keys to denote kets, and
        stores the amplitudes as values.
        - Given a number of qubits `n`, generate a list of bitstrings of
            length `n` of all zeros and a single '1' at index 'i', for 
            every index 0 <= i < n
        - This list contains the binary representation of all basis kets in a 
            Statevector Dictionary
    
    2. use Qiskit Statevector.  this stores amplitudes in a list where each ket
        is referenced by its index. the decimal value of the index
        corresponds to the binary representation of the ket.
        - Given a number of qubits `n`, generate a list of powers of two 
            from 2**0 to 2**(n-1)
        - This list contains the decimal indices of basis kets in a Statevector

With either representation:
- Generate a list of non-basis kets in the Statevector by removing all 
    basis kets from the entire list of kets
- For each non-basis ket:
    - generate a list of its corresponding basis kets
    - compute the product of the basis ket amplitudes
    - check whether its amplitude is equal to the product of its 
      corresponding basis ket amplitudes and record the boolean result
- The Entanglement Criteria says that if any boolean check is False, then
    the state is Entangled.  If all boolean checks are True, the state is 
    Not Entangled.

Notes:
- I have only tested this with statevectors where the amplitude of the zero 
    ket |000...> is manually set to 1 by my user input, or set to 1 from the
    normalized_random_state() function in the create_statevector module.
- Currently, the algorithm will return incorrect results for any statevector 
    with a zero ket that has any other amplitude.  This needs to be corrected 
    by 'normalizing' any Statevector so that the zero ket has amplitude 1.
- In instances where the zero ket has amplitude 0, e.g., a statevector such as:
        |psi> = |1000> + |0100> + |0001> + |1101>
    we need to perform a 'basis change' before applying the criteria, as
    outlined in Kauffman's paper.  This has not yet been implemented.
"""

# Get list of powers of two in binary (default) or decimal
# We refer to these values as 'basis-kets'
# inputs: 
#   - n = number of qubits
#   - (optional) kets = list of all bitstrings of length n
#   - (optional) base = 10
# output: 
#   - list of powers of two from 2**0 to 2**(n-1)
def powers_of_two(n, kets=None, base=None):
    if base == 10:
        # compute and store powers of two in base 10
        return [2**(n-1-i) for i in range(n)]
    elif kets:
        # statevector keys() as input, choose only powers of two
        return [kets[2**(n-1-i)] for i in range(n)]
    else:
        # construct binary strings directly
        return [format(1 << (n - 1 - i) | 0, '0'+str(n)+'b') for i in range(n)]


# Get list of non powers of two in binary (default) or decimal
# We refer to these values as 'non-basis kets'
# inputs:
#   - n = number of qubits, 
#   - powers = list of powers of 2
#   - (optional) kets = list of all bitstrings of length n
#   - (optional) base = 10
# output: 
#   - list of non-powers of two less than 2**(n-1)
def non_basis_kets(n, powers, kets=None, base=None):
    if base == 10:
        # generate a list of decimal integers without powers of two
        non_basis_kets = [i for i in range(1,2**n) if i not in powers]
    elif kets:
        # statevector keys() as input, remove powers of two
        non_basis_kets = [ket for ket in kets[1:] if ket not in powers]
    else:
        # construct binary strings directly
        non_basis_kets = [format(i, '0'+str(n)+'b') for i in range(1,2**n)]
        for p in powers:
            non_basis_kets.remove(p)        
    return non_basis_kets


# Determine basis kets corresponding to a non-basis ket
# Use this to reference basis kets in a Qiskit Statevector Dictionary
# Kets are all represented by binary strings
# inputs:    
#   - ket = a non-basis ket of length 'n'
#   - powers = list of all basis kets of length 'n'
# output:
#   - list of basis kets whose binary sum equals the non-basis ket
def get_basis_kets(ket, powers):
    basis_kets = [powers[index] for index, bit in enumerate(ket) if bit == "1"]
    return basis_kets


# Determine the integer powers of two that sum to a non-power of two
# Use this to reference basis kets by their indices in a Qiskit Statevector
# inputs:
#   - powers = list of powers of two
#   - k = non-basis ket index
# output:
#   - list of basis ket indices
def get_basis_indices(k, powers):
    k_list = []
    for p in powers:
        if k < p:
            pass
        else:
            k = k - p
            k_list.append(p)
    return k_list


# Create a dictionary of non-basis kets and their corresponding basis kets
# inputs:
#   - list = list of non-basis kets (binary) or non-basis ket indices
#   - powers = list of all basis kets of length n (binary) or their ket indices
#   - (optional) base = 10 (when using indices)
# output:
#   - dictionary containing:
#       - keys: the non-basis kets provided above
#       - values: dictionaries initialized with a list of their corresponding 
#                 basis kets
def non_basis_kets_dict(list, powers, base=None):
    dict = {}

    if base == 10:
        # use decimal function
        get_kets = get_basis_indices
    else:
        # use binary function
        get_kets = get_basis_kets

    for ket in list:
        m = ket
        basis_kets = get_kets(ket, powers)
        dict[m] = { 'basis_kets': basis_kets }

    return dict


# Compute the product of basis ket amplitudes
# This function works with either decimal or binary representations of kets
# inputs:
#   - statevector or statevector dictionary
#   - list of basis kets as decimal indices or as binary strings
# output: 
#   - product of the amplitudes of the given basis kets
def basis_amplitude_product(statevector, index_list):
    product = 1    
    for index in index_list:
        product = product*statevector[index]
    return product


# Equality check
# input: two values
# output: True or False
# Make lambda function?
def is_equal(a, b):
    return a == b


# Check equality of a non-basis ket amplitude with the product of its 
# corresponding basis ket amplitudes, and store the results in a dictionary.
# This is a self-contained method to check the criteria on a specific ket 
# without having to run the algorithm for all kets.
# inputs:
#   - a statevector dictionary
#   - a non-basis ket (binary)
#   - (optional) list of corresponding basis kets
# output: 
#   - dictionary with computed amplitude and boolean check value
def check_single_ket(statevector, ket, basis_kets=None):
    dict = {}

    if basis_kets == None:
    #   if basis kets not provided, generate them
        basis_kets = generate_basis_kets(ket)
        dict['basis_kets'] = basis_kets

    # get product of basis ket amplitudes
    # append result to dictionary
    dict['target_amplitude'] = basis_amplitude_product(statevector, basis_kets)

    # check if ket amplitude = product of basis ket amplitudes
    # append boolean result to dictionary
    dict['equality'] = is_equal(statevector[ket], dict['target_amplitude'])

    # Print Statements
    def print_statements():
        product_string = basis_product_string(basis_kets)
        print_entanglement_equation(ket, product_string, dict['equality'])
        if dict['equality'] == False:
            print_basis_amplitudes(product_string, dict['target_amplitude'])
    
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
def generate_basis_kets(ketstring):
    length = len(ketstring)
    basis_kets = [format(1 << (length - 1 - index) | 0, '0'+str(length)+'b')
               for index, bit in enumerate(ketstring) if bit == "1"]    
    return basis_kets

# Generate basis indices corresponding to a specific non-basis ket index
# Method 2 (decimal)
# Use with Qiskit Statevector and function check_single_ket when a list of 
#   basis kets is not provided
# input:
#   - bitstring representing a non-basis ket
# output:
#   - decimal indices representing the corresponding basis kets
def generate_basis_indices(ket):
    indices = [2**(len(ket) - 1 - index) for index, bit in enumerate(ket) 
    if bit == "1"]
    return indices


# Print Product of basis kets Expression
# input:
#   - list of basis kets for a non-basis ket
def basis_product_string(list):
    product = "Psi['"+list[0]+"']"
    for index in list[1:]:
        product = product + "*Psi['"+index+"']"
    return product

# Print Product of basis kets Amplitude
# input:
#   - kets = text string reference to product of a list of basis ket amplitudes
#   - amplitude = the numerical value of the product of the amplitudes
def print_basis_amplitudes(kets, amplitude):
    print(kets + " = " + str(amplitude))

# Print non-basis ket amplitude
# inputs:
#   - ket = text string reference to a non-basis ket amplitude
#   - amplitude = numerical value of amplitude
def print_ket_amplitude(ket, amplitude):
    print("Psi['"+ket+"'] = " + str(amplitude))


# Print True/False check statement
# inputs: 
#   - non-basis ket
#   - product of basis ket string
#   - boolean check value
def print_entanglement_equation(ket, basis_elements, bool):
    print("Psi['"+ket+"']" + " == " + basis_elements + " is " + str(bool))


# Entanglement Function
# At this time, this function only uses binary ket represenations
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
def entangled(statevector):
    # get number of qubits
    number_qubits = len(list(statevector.keys())[0])

    # generate list of all basis kets
    powers = powers_of_two(number_qubits)

    # generate list of all non-basis kets
    non_basis_kets_list = non_basis_kets(number_qubits, powers)

    # store all non-basis kets in dictionary
    dict = non_basis_kets_dict(non_basis_kets_list, powers)

    # initalize booleans
    booleans = set()

    # apply entanglement criteria for each ket
    for ket in dict:
        # get results from check single ket
        ket_results = check_single_ket(
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

