#Python lists
'''
Lists are just like arrays decalred in other language.
Lists need not be homogenous. A single list may contain DataTypes like Integers, Strings and Objects.
Useful in implementing stacks and queues.
Mutable and hence can be altered even after their creation.
'''

#List Question
'''
Randomly generate a list (a) of 30 numbers from 0 to 10(inclusive)
Print out the elements of the list that are less than 5
Make a new list(b) that has all the elemnts less than 5 from the previous list(a)
Ask the user for a number and return a list(c) that contains only elements
from the original list(a) that are smaller than that number given by the user.
Sort the original list into a new list(d) and print it out
'''

import random

#Declare variables
count = 0
a = []
b = []
c = []
user = 0

#insert random numbers into list
while(count != 29):
  com = random.randint(0,10)
  a.append(com)
  count += 1

print(a)

#insert values that are less than 5 from a to b
for x in a:
    if(x < 5):
        b.append(x)

print(b)

#ask user for number
user = int(input("Enter a number"))

for x in a:
    if(x < user):
        c.append(x)

print(c)

#Make a sorted list of a
for i in range(len(a)):
    for j in range(0, len(a)-i-1):
        if a[j] > a[j+1]:
            a[j], a[j+1] = a[j+1], a[j]

print(a)
