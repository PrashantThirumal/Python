'''
File I/O
'''

#Prizes class
class Prize:
    name = "default"
    cost = 0.0

    #Constructor
    def __init__(prize, aName, aCost):
        prize.name = aName
        if(float(aCost) >= 0):
            prize.cost = aCost
        else:
            print("INVALID PRIZE COST")

    #Accessors
    def getName(prize):
        return prize.name

    def getCost(prize):
        return prize.cost

    #Mutators
    def setName(prize, aName):
        prize.name = aName

    def setCost(prize, aCost):
        if(aCost >= 0):
            prize.cost = aCost
        else:
            print("INVALID PRIZE COST")

    #To String method
    def toString(self):
        print("Name: " + self.getName() + " Cost: " + str(self.getCost()))


#Showcase Class
import random
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

        

#Front End
#Create an instance of showcase
move = Showcase("prizeList.txt")

answer = "yes"

while answer == "yes":
    cost = 0
    run = move.getShowCase()

    print("Welcome to the showcase showdown")
    print("Your prizes are: ")

    for x in range(0, len(run)):
        print(run[x].getName())

    for x in range(0, len(run)):
        cost += float(run[x].getCost())

    print("You must guess the total cost of all without going over")
    guess = float(input("Enter your guess"))
    cost2 = cost-2000

    if guess <= cost and guess >= cost2:
        print("You guessed " + str(guess) + ". The actual price is " +
              str(cost) + ".\nYour guess was under! You win! :)")
    else:
        print("You guessed " + str(guess) + ". The actual price is " +
              str(cost) + ".\nYour guess was bad. You lose for being bad :(")

    ques = input("Would you like to play again? Enter \"no\" to quit")
    if ques != "yes":
        answer = "No"

    
    
