#LAB 04

'''
The conversions are:
Nautical Mile to Inches = 72,913.4
Mile to Inches = 63,360
Yards to Inches = 36
Feet to Inches = 12
'''

num = float(input("Enter a number of Nautical Miles \nand I will give its break down"))

inches = num * 72913.4
# floor division // gives the whole number
# 5//2 = 2 whereas 5/2 = 2.5
miles = inches // 63360
miles_remainder = inches % 63360
yards = miles_remainder // 36
yards_remainder = yards % 36
feet = yards_remainder // 12
final_inches = yards_remainder % 12

print( str(miles) + " miles")
print( str(yards) + " yards")
print( str(feet) + " feet")
print(str(final_inches) + " inches")
