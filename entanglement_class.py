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

Attributres 1 - 5 are meant to be static and global to the class.  Attribute 6
is meant to be local to a user statevector.
		
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

>>> x.entangled(x.statevector)
|Psi> is not Entangled
{'0011': {
	'basis_kets': ['0010', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '0101': {
	'basis_kets': ['0100', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '0110': {
	'basis_kets': ['0100', '0010'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '0111': {
	'basis_kets': ['0100', '0010', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '1001': {
	'basis_kets': ['1000', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '1010': {
	'basis_kets': ['1000', '0010'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '1011': {
	'basis_kets': ['1000', '0010', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '1100': {
	'basis_kets': ['1000', '0100'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '1101': {
	'basis_kets': ['1000', '0100', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}, 
 '1110': {
	'basis_kets': ['1000', '0100', '0010'], 
	'target_amplitude': (1+0j), 
	'equality': True
	},
 '1111': {
	'basis_kets': ['1000', '0100', '0010', '0001'], 
	'target_amplitude': (1+0j), 
	'equality': True
	}
}

>>> my_statevector = x.get_amplitudes()
Enter an amplitude for 0000: 4
Enter an amplitude for 0001: 3
Enter an amplitude for 0010: 2
Enter an amplitude for 0011: 1
Enter an amplitude for 0100: 6
Enter an amplitude for 0101: 3
Enter an amplitude for 0110: 2
Enter an amplitude for 0111: 7
Enter an amplitude for 1000: 10
Enter an amplitude for 1001: 5
Enter an amplitude for 1010: 3
Enter an amplitude for 1011: 7
Enter an amplitude for 1100: 1
Enter an amplitude for 1101: 3
Enter an amplitude for 1110: 9
Enter an amplitude for 1111: 8

>>> my_statevector
{'0000': (4+0j), '0001': (3+0j), '0010': (2+0j), '0011': (1+0j), '0100': (6+0j),
 '0101': (3+0j), '0110': (2+0j), '0111': (7+0j), '1000': (10+0j), '1001': (5+0j),
 '1010': (3+0j), '1011': (7+0j), '1100': (1+0j), '1101': (3+0j), '1110': (9+0j),
 '1111': (8+0j)}

>>> x.entangled(my_statevector)
|Psi> is Entangled
{'0011': {
	'basis_kets': ['0010', '0001'], 
	'target_amplitude': (0.375+0j), 
	'equality': False
	}, 
 '0101': {
	'basis_kets': ['0100', '0001'], 
	'target_amplitude': (1.125+0j), 
	'equality': False
	}, 
 '0110': {
	'basis_kets': ['0100', '0010'], 
	'target_amplitude': (0.75+0j), 
	'equality': False
	}, 
 '0111': {
	'basis_kets': ['0100', '0010', '0001'], 
	'target_amplitude': (0.5625+0j), 
	'equality': False
	}, 
 '1001': {
	'basis_kets': ['1000', '0001'], 
	'target_amplitude': (1.875+0j), 
	'equality': False
	}, 
 '1010': {
	'basis_kets': ['1000', '0010'], 
	'target_amplitude': (1.25+0j), 
	'equality': False
	}, 
 '1011': {
	'basis_kets': ['1000', '0010', '0001'], 
	'target_amplitude': (0.9375+0j), 
	'equality': False
	}, 
 '1100': {
	'basis_kets': ['1000', '0100'], 
	'target_amplitude': (3.75+0j), 
	'equality': False
	}, 
 '1101': {
	'basis_kets': ['1000', '0100', '0001'], 
	'target_amplitude': (2.8125+0j), 
	'equality': False
	}, 
 '1110': {
	'basis_kets': ['1000', '0100', '0010'], 
	'target_amplitude': (1.875+0j), 
	'equality': False
	}, 
 '1111': {
	'basis_kets': ['1000', '0100', '0010', '0001'], 
	'target_amplitude': (1.40625+0j), 
	'equality': False
	}
}

- basis change methods added and tested
- see `basis_change.ipynb` for examples

TODO next:
- replace recursive function calls with while loops
- review which methods should be private vs public
- convert kets, basis_kets, and non_basis_kets to tuples so they are immutable
- rewrite docstrings as restructured text
- try to output final result as JSON (see python json encoding tutorial)
"""

import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import random_statevector
import inspect

class Entangled:
	def __init__(self, number_qubits) -> None:
		self.number_qubits = number_qubits

		# initialize new statevector dictionary
		self.statevector = self.init_statevector()

		# create list of all kets of length 'number_qubits'
		self.kets = list(self.statevector.keys())

		# create list of basis kets of length 'number_qubits'
		self.basis_kets = self.__powers_of_two(self.number_qubits, self.kets)

		# create list of non-basis kets of length 'number_qubits'
		self.non_basis_kets = self.__non_basis_kets_list(
			self.basis_kets, self.kets
			)

		# create dictionary of non-basis kets and their basis ket decompositions
		self.decomp_dict = self.__non_basis_kets_dict(
				self.non_basis_kets, self.basis_kets
			)

	# Initialize a nonzero Qiskit Statevector Dictionary
	# use np.ones() because Statevector(np.zeros()) returns an empty list    
	def init_statevector(self) -> dict:
		return Statevector(np.ones(2**self.number_qubits)).to_dict()
	
	# Get list of powers of two as binary strings
	# We refer to these values as 'basis-kets'
	# inputs: 
	#   - n = length of bitstrings
	#   - kets_list = a list of statevector.keys()
	# output: 
	#   - list of basis kets of length n powers of two from 2**0 to 2**(n-1)
	def __powers_of_two(self, n, kets_list) -> list:
		return [kets_list[2**(n-1-i)] for i in range(n)]

	# Get list of non powers of two as binary strings
	# We refer to these values as 'non-basis kets'
	# inputs:
	#   - n = number of qubits, 
	#   - powers = list of basis kets
	#   - kets = a list of statevector.keys()
	# output: 
	#   - list of non-powers of two less than 2**(n-1)
	def __non_basis_kets_list(self, powers, kets) -> list:
		return [ket for ket in kets[1:] if ket not in powers]

	# Determine basis ket decomposition of a non-basis ket
	# inputs:    
	#   - ket = a non-basis ket of length 'n'
	#   - powers = list of all basis kets of length 'n'
	# output:
	#   - list of basis kets whose binary sum equals the non-basis ket
	def __get_basis_kets(self, ket, powers) -> list:
		basis_kets = [
			powers[index] for index, bit in enumerate(ket) if bit == "1"
			]
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
	def __non_basis_kets_dict(self, list, powers) -> dict:
		dict = {}

		for ket in list:
			basis_kets = self.__get_basis_kets(ket, powers)
			dict[ket] = { 'basis_kets': basis_kets }

		return dict

		"""
		can also use dictionary comprehension?
		dict = {
			ket: { 'basis_kets': self.get_basis_kets(ket, powers)}
			for ket in list }
		"""

	# Compute the product of ket amplitudes
	# inputs:
	#   - statevector dictionary
	#   - list of basis kets
	# output: 
	#   - product of the amplitudes of the given basis kets
	def __basis_amplitude_product(self, statevector, index_list) -> complex:
		product = 1    
		for index in index_list:
			product = product*statevector[index]
		return product

	# Generate basis kets corresponding to a specific non-basis ket
	# Use with method check_single_ket when a list of basis kets is not provided
	# input:
	#   - ket = bitstring representing a non-basis ket
	# output:
	#   a list of bitstrings representing the corresponding basis kets
	def __generate_basis_kets(self, ket) -> list:
		length = len(ket)
		basis_kets = [format(1 << (length - 1 - index) | 0, '0'+str(length)+'b')
				for index, bit in enumerate(ket) if bit == "1"]
		return basis_kets

	# Check equality of a non-basis ket amplitude with the product of its 
	# corresponding basis ket amplitudes and store the results in a dictionary.
	# This can be used separately to check the criteria on a specific ket 
	# without running the algorithm over all kets.  Basis kets can be generated
	# 'on the fly' when a preset list is not provided.
	# inputs:
	#   - a statevector dictionary
	#   - a non-basis ket
	#   - (optional) list of corresponding basis kets
	# output: 
	#   - dictionary with computed target amplitude and boolean check value
	def check_single_ket(self, statevector, ket, basis_kets=None) -> dict:
		dict = {}

		if basis_kets == None:
		# if basis kets not provided, generate them
			basis_kets = self.__generate_basis_kets(ket)
			dict['basis_kets'] = basis_kets

		# get product of basis ket amplitudes
		# append result to dictionary
		dict['target_amplitude'] = self.__basis_amplitude_product(
			statevector, basis_kets
			)

		# check if ket amplitude = product of basis ket amplitudes
		# append boolean result to dictionary
		dict['equality'] = statevector[ket] == dict['target_amplitude']

		# Print Statements
		def print_statements():
			product_string = self.basis_product_string(basis_kets)
			self.print_entanglement_equation(
				ket, product_string, dict['equality']
				)
			if dict['equality'] == False:
				self.print_basis_amplitudes(
					product_string, dict['target_amplitude']
					)
		
		# print_statements()
		
		return dict

	# Print Product of basis kets Expression
	# input:
	#   - list of basis kets for a non-basis ket
	def basis_product_string(self, list) -> str:
		product = "Psi['"+list[0]+"']"
		for index in list[1:]:
			product = product + "*Psi['"+index+"']"
		return product

	# Print Product of basis kets Amplitude
	# input:
	#   - kets = text string reference to product of a list of basis ket amplitudes
	#   - amplitude = the numerical value of the product of the amplitudes
	def print_basis_amplitudes(self, kets, amplitude) -> None:
		print(kets + " = " + str(amplitude))

	# Print non-basis ket amplitude
	# inputs:
	#   - ket = text string reference to a non-basis ket amplitude
	#   - amplitude = numerical value of amplitude
	def print_ket_amplitude(self, ket, amplitude) -> None:
		print("Psi['"+ket+"'] = " + str(amplitude))


	# Print True/False check statement
	# inputs: 
	#   - non-basis ket
	#   - product of basis ket string
	#   - boolean check value
	def print_entanglement_equation(self, ket, basis_elements, bool) -> None:
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
		# initialize new decomposition dictionary for input statevector
		dict = self.__non_basis_kets_dict(self.non_basis_kets, self.basis_kets)

		# check if zero ket exists and perform change of basis if not
		if statevector['0'*self.number_qubits] == 0:
			valid_kets = self.get_valid_kets(statevector)
			source_ket = self.get_source_ket(valid_kets)
			statevector = self.basis_change_method_two(statevector, source_ket)
			# get source ket
			# basis change method
			pass

		# check zero ket amplitude and normalize if not equal to 1        
		if statevector['0'*self.number_qubits] != 1:
			statevector = self.normalize_statevector(statevector)

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


	# Get amplitude of single ket from user input
	# Input is converted to complex number and type checked
	# Non-numerical value will prompt user to input again
	def __get_amplitude(self, key) -> complex:
		""" get a complex number from user input
		"""
		
		# checks if user input is a number
		while True:
			amplitude = input(f"Enter an amplitude for {key}: ")
			
			# empty user input defaults to '0' amplitude
			if amplitude == "":
				amplitude = 0
			try:
				# convert user input to complex number type
				amplitude = complex(amplitude)
			except ValueError:
				print(f"Error: amplitude for {key} must be a number.")
				continue
			else:
				break
		
		return amplitude


	# Create statevector dictionary by prompting user to input amplitudes
	# for each ket.  User may supply their own statevector as a parameter.
	# If no parameter is provided, a new statevector is initalized.
	# input:
	#	- (optional) user statevector dictionary
	# output:
	#	- statevector dictionary with updated amplitudes
	def get_amplitudes(self, statevector=None) -> dict:
		""" Populate a new Qiskit Statevector Dictionary with amplitudes 
		via user input
		"""
		
		if statevector:
			# assign variable to user supplied statevector
			new_statevector = statevector
		else:
			# initialize new statevector of length 2**number_qubits
			new_statevector = self.init_statevector()
			
		# update ket amplitudes
		for key in new_statevector.keys():
			new_statevector[key] = self.__get_amplitude(key)

		return new_statevector


	# Perform basis change on a single ket using XOR operator
	# input:
	#	- target_ket to be transformed
	#	- source_ket that maps to zero ket
	# output:
	#	- transformed target ket
	def basis_change_ket(self, target_ket, source_ket):
		target_ket = format(
			(int(target_ket,2))^(int(source_ket,2)), 
			'0'+str(len(source_ket))+'b'
			)
		return target_ket 

	# Basis Change Method 1: Transform Statevector keys directly
	# This will change the order of kets in the Statevector, though
	# this should not make a difference when using the entangled() method 
	# since kets are only used reference amplitudes, and the final output 
	# decomp_dictionary is ordered
	# inputs:
	# 	- statevector to be transformed
	#	- source_ket that maps to zero ket
	# output:
	#	- transformed statevector
	def basis_change_method_one(self, statevector, source_ket: str):
		new_statevector = {
			self.basis_change_ket(key, source_ket): value
			for (key, value) in statevector.items()
		}
		return new_statevector

	# Basis Change Method 2: Map Amplitudes to New Statevector
	# This will preserve ket order for convenience
	# inputs:
	#	- statevector to be transformed
	#	- source_ket that maps to zero ket
	# output:
	def basis_change_method_two(self, statevector, source_ket: str):
		# create basis mapping dictionary
		basis_change_dictionary = self.basis_change_dict(
			statevector, 
			source_ket
			)

		# map amplitudes into new statevector
		new_statevector = self.map_amplitudes(
			statevector, 
			basis_change_dictionary
			)
		return new_statevector

	# Create dictionary of basis change mapping
	# note: can this be done with Python map() method?
	# inputs:
	#	- statevector to be transformed
	#	- source_ket that maps to zero ket
	# output:
	#	- dictionary {new_ket: old_ket} of basis change mapping 
	def basis_change_dict(self, statevector, source_ket: str) -> dict:
		dict = {
			key: self.basis_change_ket(key, source_ket)
			for key in statevector.keys()
		}
		return dict

	# Map amplitudes from original statevector to their locations in the 
	# transformed statevector
	# inputs:
	#	- old_statevector = original Statevector dictionary
	#	- dict: basis change mapping dictionary
	# output:
	#	- new_statevector = Transformed Statevector dictionary
	def map_amplitudes(self, old_statevector, dict: dict) -> dict:
		new_statevector = self.init_statevector()
		for key in new_statevector.keys():
			new_statevector[key] = old_statevector[dict[key]]
		return new_statevector

	# Generate a list of kets for user to choose for basis transformation
	# input:
	#	- statevector = Statevector dictionary with zero ket amp equal to '0'
	# output:
	#	- tuple of non-zero kets
	def get_valid_kets(self, statevector) -> tuple:
		# generate a list of valid kets with non-zero amplitudes
		valid_kets = [
			key for (key, value) in statevector.items() if value != 0
			]

		return tuple(valid_kets)

	# Get source_ket for basis change via user input
	# input:
	#	- valid_kets = tuple of non-zero kets
	#	- recursive = boolean check for invalid input
	# output:
	#	- source_ket = ket to use for basis change transformation
	def get_source_ket(self, valid_kets: tuple, recursive=False):
		""" get a ket string from user input
		"""

		while True:
			# display list of valid kets
			print(valid_kets)

			try:
				# get user input and convert to string
				source_ket = str(
					input(inspect.cleandoc(
					"""Please choose a ket to map to the zero ket:
					(or press Enter to choose a random ket)"""
					))
				)    
				# empty user input chooses random ket from valid_kets
				if source_ket == "":
					source_ket = np.random.choice(valid_kets)
					print("Random Choice: " + source_ket)
				# check if user input is in valid_kets
				elif source_ket not in valid_kets:
					raise ValueError
			except ValueError:
				print(
					inspect.cleandoc(
					"""Error, please choose a ket from the following list:
					(or Press Enter to choose a random ket)"""
					)
				)
				continue
			else:
				break

		return source_ket
	

	# Normalize zero ket to have amplitude = 1
	# input:
	#   - user qiskit statevector dictionary
	# output:
	#   - qiskit statevector dictionary with amplitudes scaled so that zero ket
	#       has amplitude '1'
	def normalize_statevector(self, statevector):
		# get initial zero ket amplitude
		zero_ket_amplitude = statevector['0'*self.number_qubits]

		# divide all amplitudes by zero ket amplitude
		normalized_statevector = { 
			key: value/zero_ket_amplitude for key, value in statevector.items()
			}
	   
		return normalized_statevector


	# Random Statevector Dictionary with normalized zero ket
	def normalize_random_statevector(self):
		# generate Qiskit random statevector of dim 2**number_qubits
		random_state = random_statevector(2**self.number_qubits, None)

		# Normalize zero ket to have amplitude = 1
		normalized_random_state = random_state/random_state[0]

		# Convert normalized Statevector to dictionary:
		statevector = normalized_random_state.to_dict()

		return statevector