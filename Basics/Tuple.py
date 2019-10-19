'''
Tuples
'''

import sys
import timeit

#Creating a Tuple. NOTE: Tuples are NOT Mutable

#Single Element Tuple

single = ("a" ,) #comma is important to denote it is a single elemnt tuple
multiple = ("a" , "b", "c",);

#Test if it is a tuple
print(single)
print(multiple)

#Tuples are smaller than lists
list_eg = [1, 2, 3, 'a', 'b', 'c', True, 3.14159]
tuple_eg = (1, 2, 3, 'a', 'b', 'c', True, 3.14159)

print("\nList size = " , sys.getsizeof(list_eg))
print("Tuple size = " , sys.getsizeof(tuple_eg))

#Tuples are created faster than lists
list_test = timeit.timeit(stmt = "[1,2,3,4,5]", number = 1000000)
tuple_test = timeit.timeit(stmt = "(1,2,3,4,5)", number = 1000000)

print('\nList time: ', list_test)
print('Tuple time: ', tuple_test)

#Tuple assignment
survey = (27, "Vietnam", True)
age, country, knows_python = survey #assign variables in one line
print("\nAge: ", age)
print("Country: ", country)
print("Knows Python? ", knows_python)
