#Weight conversions program

print('Welocme to the weight and height converter 9000!')

#Get user input for pounds and height

pounds = float(input('Enter a weight in pounds'))
height = float(input('Enter a height in feet'))

#Convert pounds to different weights
kilograms = pounds * 0.456
stones = pounds * 0.071
slug = pounds * 0.031
penny_weight = pounds * 291.667
grain = pounds * 7000

#Convert height to different heights
meter = height * 0.305
hand =  height * 3
furlong = height * 0.002
cubit = height * 0.667
rack = height * 6.857

#print converted measurements
print(pounds,'lbs is ',kilograms,' kilograms')
print(pounds,'lbs is ',stones,' stones')
print(pounds,'lbs is ',slug,' slugs')
print(pounds,'lbs is ',penny_weight,' pennyweights')
print(pounds,'lbs is ',grain,' grains')
print(height,'feet is ',meter,' meters')
print(height,'feet is ',hand,' hands')
print(height,'feet is ',furlong,' furlongs')
print(height,'feet is ',cubit, 'cubits')
print(height,'feet is ',rack,' racks')
