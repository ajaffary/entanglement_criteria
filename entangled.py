"""
Definitions:
- Basis Kets are any bitstrings with a single '1' only
- A Basis Ket with a '1' at index 'i' is referred to as 'e_i'
- Non-Basis Kets are bitstrings with '1' occuring in at least two places

Logic:
- Given a Statevector Dictionary, separate all kets into 'basis kets' and 
'non-basis kets'
- For each 'non-basis ket', decompose it into its corresponding 'basis kets'
    and apply the Entanglement Criteria
- Output the result:  whether or not the Statevector is Entangled

Implementation:
- Basis Kets are bitstrings representations of powers of 2.  Non-Basis Kets 
are bitstrings representations of all other integers.  A 'decomposition' of a
'Non-Basis Ket' into 'Basis Kets' means separating any integer that is not a
power of two into a sum of integers that are powers of two, e.g. the integer:
    13 = 8 + 4 + 1
corresponds to:
    1101 = 1000 + 0100 + 0001
in binary.
- Given the number of qubits `n`, generate a list of powers of two from 2**0 
    to 2**(n-1)
- This list is a decimal index representation of Basis Kets
- Alternatively, for bitstrings of length `n`, generate a list of bitstrings 
    of zeros and a single '1' at index 'i', for each index
- Given a Statevector, generate a list of Non-Basis Kets present in the 
    Statevector by comparing its kets with the list of Basis Kets
- For each Non-Basis Ket, generate a list of its corresponding Basis Kets
    -- This is implemented two ways, one for decimal, one for binary
- For each Non-Basis Ket, compare its amplitude with the product of its 
    corresponding Basis Ket amplitudes
- Record the equality as a boolean value (appended to the Non-Basis Ket
    dictionary)
- The Entanglement Criteria says that is if any boolean check is false, then
    the state is Entangled.  If all boolean checks are true, the state is 
    Not Entangled.

Notes:
- I have only tested this with statevectors where the amplitude of the zero 
    ket |000...> is manually set to 1 by my user input, or set to 1 from the
    normalized_random_state() function in the create_statevector module.
- Currently, this will return incorrect results for any statevector with a 
    zero ket that has any other amplitude.  This needs to be corrected by 
    'normalizing' any Statevector so that the zero ket has amplitude 1.
- In instances where there is no zero ket, e.g., a statevector such as:
    |psi> = |1000> + |0100> + |0001> + |1101>
    we need to perform a 'basis change' before applying the criteria, as
    outlined in Kauffman's paper.  This has not yet been implemented.
"""

# Get list of Powers of Two in Binary or Decimal up to 2**(n-1)
# input: 
#   n = number of qubits
#   base = 2 or 10 (optional)
# output: 
#   list of powers of two up to 2**(number_qubits-1)
def powers_of_two(n, kets=None, base=None):
    if base == 10:
        return [2**(n-1-i) for i in range(n)]
    elif kets:
        return [kets[2**(n-1-i)] for i in range(n)]
    else:
        return [format(1 << (n - 1 - i) | 0, '0'+str(n)+'b') for i in range(n)]


# Get list of Non-Basis Kets in Binary or Decimal
# input:
#   n = number of qubits, 
#   powers = list of powers of 2
#   kets = list of all kets
#   base = 2 or 10 (optional)
# output: 
#   list of non-basis kets
def non_basis_kets(n, powers, kets=None, base=None):
    # decimal
    if base == 10:
        non_basis_kets = [i for i in range(1,2**n) if i not in powers]
    # statevector keys() as input
    elif kets:
        non_basis_kets = [ket for ket in kets[1:] if ket not in powers]
    # construct binary kets
    else:
        # can this be condensed to exclude 'powers'?
        non_basis_kets = [format(i, '0'+str(n)+'b') for i in range(1,2**n)]
        for p in powers:
            non_basis_kets.remove(p)        
    return non_basis_kets


# Determine Basis Kets (binary)
# input:    
#   ket = non-basis ket
#   powers = list of all basis kets
# output:
#   list of basis kets
def get_basis_kets(ket, powers):
    basis_kets = [powers[index] for index, bit in enumerate(ket) if bit == "1"]
    return basis_kets


# Determine Basis Kets (decimal)
# creates a list of basis kets indices corresponding to non-basis ket
# input:
#   powers = list of powers of two
#   k = non-basis ket index
# output:
#   list of basis ket indices
def get_basis_indices(k, powers):
    k_list = []
    for p in powers:
        if k < p:
            pass
        else:
            k = k - p
            k_list.append(p)
    return k_list


# Create a dictionary of non-basis kets as keys
# Each value is a dictionary consisting of a list of corresponding basis kets
# and will be appended later with target amplitude and boolean check
# input:
#   list of non-basis kets (binary) or non-basis ket indices (decimal)
#   list of all basis kets (binary) or ket indices (decimal)
# output:
#   dictionary
def non_basis_kets_dict(list, powers, base=None):
    # list = list of non-basis kets or indices
    # powers = list of basis kets or powers of 2
    # base = 10 for indices output
    dict = {}
    if base == 10:
        # decimal function
        get_kets = get_basis_indices
    else:
        # binary function
        get_kets = get_basis_kets

    for ket in list:
        m = ket
        basis_kets = get_kets(ket, powers)
        dict[m] = { 'basis_kets': basis_kets }

    return dict


# Multiply Basis Ket Amplitudes
# input: statevector = list (decimal) or dictionary (binary)
#        list of basis kets (binary or decimal)
# output: product of amplitudes, indexed by
#         basis kets in Statevector dictionary (binary)
#         or basis ket indices in Statevector (decimal)
def basis_amplitude_product(statevector, index_list):
    """ Works with decimal and binary indices """
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


# single ket check function (using binary keys)
# input: statevector, ket, list of basis kets (optional)
#   if basis kets not provided, it will generate them
# output: dictionary with amplitude and boolean check value
def check_single_ket(statevector, ket, basis_kets=None):
    dict = {}
        
    if basis_kets == None:
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


# Generate basis kets
# Method 1 (binary)
# Use with check_single_ket and Statevector Dictionary 
#   when basis_kets not provided
# input: (binary) non-basis ket string
# output: (binary) keys for basis kets in Statevector Dictionary
def generate_basis_kets(ketstring):
    length = len(ketstring)
    basis_kets = [format(1 << (length - 1 - index) | 0, '0'+str(length)+'b')
               for index, bit in enumerate(ketstring) if bit == "1"]    
    return basis_kets

# Generate basis indices
# Method 2 (decimal)
# Use with check_single_ket and Statevector when basis_kets not provided
# input: (binary) non-basis ket string
# ouput: (decima) indices for basis kets in Statevector

def generate_basis_indices(ket):
    indices = [2**(len(ket) - 1 - index) for index, bit in enumerate(ket) 
    if bit == "1"]
    return indices


# Print Product of Basis Kets Expression
# input: list of basis kets for a non-basis ket
# output: string of product of Psi[basis_ket]

def basis_product_string(list):
    product = "Psi['"+list[0]+"']"
    for index in list[1:]:
        product = product + "*Psi['"+index+"']"
    return product


# Print Non-basis ket amplitude
# input: non-basis ket, amplitude

def print_ket_amplitude(ket, amplitude):
    print("Psi['"+ket+"'] = " + str(amplitude))


# Print Product of Basis Kets Amplitude
# input: product of basis ket string, amplitude

def print_basis_amplitudes(kets, amplitude):
    print(kets + " = " + str(amplitude))


# Print True/False check statement
# input: non-basis ket, product of basis ket string, boolean check value

def print_entanglement_equation(ket, basis_elements, bool):
    print("Psi['"+ket+"']" + " == " + basis_elements + " is " + str(bool))


# Entanglement Function (binary kets)
# input: Statevector Dictionary
# output: dictionary 
#   keys: all non-basis kets
#   values: dictionaries of corresponding basis kets, target amplitude, 
#           boolean check

def entangled(statevector):
    # get number of qubits
    number_qubits = len(list(statevector.keys())[0])

    # generate list of all basis kets:
    powers = powers_of_two(number_qubits)

    # generate list of all non-basis kets:        
    non_basis_kets_list = non_basis_kets(number_qubits, powers)

    # store all non-basis kets in dictionary:
    dict = non_basis_kets_dict(non_basis_kets_list, powers)

    # initalize booleans
    booleans = set()

    for ket in dict:
        # get results fron check single ket:
        ket_results = check_single_ket(
            statevector, 
            ket, 
            dict[ket]['basis_kets']
            )
        # update dictionary with results:
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

