'''
Created on May 30, 2019

@author: Prashant
'''

'''
1. Create a set of 8 people
2. Iterate over the set
3. Add 3 people to the set
4. Remove 1 person from the set
5. Remove an item from a set if it is present in the set.
6. Create an intersection of sets
7. Create a union of sets
8. Create set difference
9. Create a symmetric difference
10. Use issubset and issuperset
11. Create a shallow copy of sets
12. Clear a set
13. Create a frozen set
14. Create a set of random numbers and find the max and minimum value
15. Find the length of a set

'''
import random

#1. 
people = {"Adam", "Sophia", "Jackson", "Olivia", "Liam", "Emma", "Noah", "Ava" }
print("Printing Orginal Set:")
print(people)

#2.
print("\nIterating over set")
for n in people:
    print(n)
    
#3. 
print("\nAdding 3 people to the set")
people.update(["Jack", "John", "Jake"]) #Use update to add multiple people to the set
print(people)

#4.
print("\nRemoving a person from the list")
people.pop()
print(people)

#5.
print("\nRemoving John from the set")
people.discard("John")
print(people)

#6.
print("\nCreating a list of 3 people")
people_new = {"Olivia", "Noah", "Erik"}
print(people_new)
print("Printing the intersection")
print(people.intersection(people_new))

#7.
print("\nCreating a Union of people and people_new")
people_union = people|people_new
print(people_union) #Note for elements that are in both sets only one copy is included

#8.
print("\nFinding the difference of two sets")
people_difference = people_union - people
print(people_difference)

#9.
print("\nFinding the symmetric difference between two sets")
setx = set(["apple", "mango"])
sety = set(["mango", "orange"])
#Symmetric difference
setc = setx ^ sety
print(setc)

#10.
print("\nUsing the issubset and issuper set")
setx = set(["apple", "mango"])
sety = set(["mango", "orange"])
setz = set(["mango"])
issubset = setx <= sety
print(issubset)
issuperset = setx >= sety
print(issuperset)
issubset = setz <= sety
print(issubset)
issuperset = sety >= setz
print(issuperset)

#11.
print("\nCreating a shallow copy")
setp = set(["Red", "Green"])
setr = setp.copy()
print(setr)

#12.
print("\nClearing setp")
setp.clear()
print(setp)

#13.
print("\nCreating a frozen set")
frozen_set = frozenset(["e", "f", "g"])
print(frozen_set)

#14.
print("\nCreating a set of random integers")
num = set()

for n in range(4):
    com = random.randint(0,50)
    num.add(com)
    
print(num)
print("Max Number: ")
print(max(num))
print("Min Number: ")
print(min(num))

#15.
print("\nPrinting the length of num set")
print(len(num))
    
