# Numbers Squared

#Get user input for the number
num = input('Enter a 4 digit number')

print(num)
print(num[1] + "  " + num[2])
print(num[2] + "  " + num[1])

#Reverse the string using extended slice syntax
print(num[::-1])

'''
How the extended slice works:
string[start:stop:step]

Slicing a string gives you a new string from one point in the string,
backwards or forwards, to another point, by given increments.
They take slice notation or a slice object in a subscript:

'''
