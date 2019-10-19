import random

#Randomly generate numbers 0 to 50
com = random.randint(0,50)
user = 51

while(user != com):
    user = int(input("Enter your guess"))

    if(user > com):
        print("My number is smaller")
    elif(com > user):
        print("My number is bigger")

print("That is my number!!")

