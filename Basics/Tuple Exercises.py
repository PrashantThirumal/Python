from copy import deepcopy

#Create a tuple
tuple1 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(tuple1)

#Add element to a tuple
tuple2 = ("a", "b", "c")
tuple_combined = tuple1 + tuple2
print(tuple_combined)

#Add element to specific index of a tuple
tuple_specific = tuple1[:5] + ("new", "new1" ,"new2") + tuple1[5:]
print("\n", tuple_specific)

#convert tuple to list
list_converted = list(tuple1)
print("\nConverted to a list", list_converted)

#convert tuple to string
string_converted = str(tuple1)
print(string_converted)

#get the 4th element and 4th element from last of a tuple
fourth = tuple1[3]
back_fourth = tuple1[len(tuple1) - 4]
print('\nFourth Element: ', fourth)
print('Fourth from last: ', back_fourth)

#create the colon of a tuple
tuple3 = ("HELLO" , 5, [], True)
tuple_deep = deepcopy(tuple3)
print('\nOriginal: ', tuple3)
print('Deep Copy: ', tuple_deep)
tuple_deep[2].append(50)
print('Deep Copy with appending: ', tuple_deep)

#find the repeated items of a tuple
tuple4 = (0, 1, 1, 2, 3, 5, 8, 13, 21, 21, 34, 34, 34, 55, 89, 144, 233, 377, 610, 987,987,987,987)
counter = []
counting = []


for i in range(0, len(tuple4)-1):
    if(tuple4.count(tuple4[i]) > 0):
      counting.append(tuple4.count(i))
      counter.append(tuple4[i])

for i in range(0, len(counter) -1):
  print("Repeated number: " + str(counter[i]) + " No.of Times: " + str(counting[i]))
            
