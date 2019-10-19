'''
Created on May 30, 2019

@author: Prashant
'''
from builtins import set

#A set is an unordered collection data type that is iterable, mutable and has no duplicate elements

#Frozen sets are immutable objects that only support methods and operators that produce a result without affecting the frozen sets or sets to which they are applied

'''
Python program to demonstrate differences
between normal and frozen sets 
'''

normal_set = set(["a", "b", "c"])

#Adding an element to normal set is fine
normal_set.add("d")

print("Normal Set")
print(normal_set)

#A frozen set
frozen_set = frozenset(["e", "f", "g"])
print("\nFrozen Set")
print(frozen_set)
# this will yield an error :frozen_set.add("h")

'''
Methods for Sets
.add() - adds item if not already present in set
.union() - returns a union of two sets
.intersection() - returns an intersection of two sets
.difference() - returns a set containing all the elements of invoking set but not of second set
.clear
'''
print()

#Add method
people = {"Jay", "Idrish", "Archil"}
print("Original people set: " + str(people))
print("Adding Dax")
people.add("Dax")
print("New people set: " + str(people))

#Union method
vampires = {"Karan", "Arjun"}
population = people|vampires # = population = people.union(vampires)
print("\nPrinting union set population")
print(population)

#Difference method
safe = people - vampires #= safe = people.difference(vampires)
print("\nPrinting the difference between vampire and people")
print(safe)

#Clear Method
print("\nClearing the safe set")
safe.clear()
print(safe)









