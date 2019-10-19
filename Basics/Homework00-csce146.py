import random
import os

class Prize:
    name = "none"
    price = 0.00

    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def getName(self):
        return self.name

    def getPrice(self):
        return float(self.price)

    def setName(self, aNname):
        self.name = aName

    def setPrice(self, aPrice):
        self.price = aPrice

class Showcase:
    rawList = []
    showcase = []
    splitline = []
    print("erik's a bitch")
    
    def __init__(self, filename):
        file = open(filename, "r")
        print("erik's a bitch")
        for x in file:
            self.splitline = x.split('\t')
            if len(self.splitline) < 2:
                continue
            prize = Prize(self.splitline[0], self.splitline[1])
            self.rawList.append(prize)
            

        for x in range(5):
            y = random.randint(0,len(self.rawList)-1)
            z = self.rawList[y]
            self.showcase.append(z)

        print("Shaun's a bitch too")

    def getRawList(self):
        return self.rawList

    def getShowCase(self):
        return self.showcase


        '''
        exists = os.path.isfile("/Users/eriki/Desktop/prizeList.txt")
        print(exists)

        __init__("/Users/eriki/Desktop/prizeList.txt")
        print(rawList)
        print(showcase)
        print("Erik is a bitch")
        '''
        
'''
Test if split works like how i think it does
mary = "Hey Erik"
splitline = []
splitline = mary.split('r')
print(splitline[0])
'''


exists = os.path.isfile("/Users/eriki/Desktop/prizeList.txt")
print(exists)
#Showcase("/Users/eriki/Desktop/prizeList.txt")
move = Showcase("/Users/eriki/Desktop/prizeList.txt")

answer = "yes"

while answer == "yes":
    cost = 0
    run = move.getShowCase()

    print("Welcome to the showcase showdown")
    print("Your prizes are: ")

    for x in range(0, len(run)):
        print(run[x].getName())

    for x in range(0, len(run)):
        cost += run[x].getPrice()

    print("You must guess the total cost of all without going over")
    guess = float(input("Enter your guess"))
    cost2 = cost-2000

    if guess < cost and guess >= cost2:
        print("You guessed " + str(guess) + ". The actual price is " +
              str(cost) + ".\nYour guess was under! You win! :)")
    else:
        print("You guessed " + str(guess) + ". The actual price is " +
              str(cost) + ".\nY5our guess was bad. You lose for being bad :(")

    ques = input("Would you like to play again? Enter \"no\" to quit")
    if ques != "yes":
        answer = "No"
    
    

