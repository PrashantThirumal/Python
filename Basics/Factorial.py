#Given a number get its factorial
result = 1
num = int(input('Enter a number and I will give its factorial'))

if( num == 1):
    result = 1
    
# this approach is in ascending order so 1x2x3x4x5x...
else:
    for i in range(1,num+1):
        result = result * i

print(str(result))
