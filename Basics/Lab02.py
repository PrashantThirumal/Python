# declare variable
g = float(-9.81)

#Get user input
print('We are going to throw something!')
thing = input('What is the name of the thing we are going to throw?')
x = float(input('What is ' + thing + "'s initial velocity (m/s) in the x direction?"))
y = float(input('What is '+ thing + "'s initial velocity (m/s) in the y direction?"))
time = float(input('How much time (s) has elapsed'))

# Calculate the x and y distance
x = x * time
y = (y * time) + (0.5 * g * time**2)

print(thing, " is at location (m) ", x ,"," , y)
