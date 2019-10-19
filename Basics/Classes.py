'''
Creating a class and its methods
'''

class Coffee:    
    name = "default"
    caffeineContent = 0.1

    #Constructor
    def __init__(coffee, aName, aContent):
        coffee.name = aName
        if(aContent >= 50 and aContent <= 300):
            coffee.caffeineContent = aContent
        else:
            coffee.caffeineContent = -1
            print("INVALID CAFFEINE CONTENT")
        
    #Accessors
    def getName(coffee):
        return coffee.name

    def getContent(coffee):
        return coffee.caffeineContent

    #Mutators
    def setName(coffee, aName):
        coffee.name = aName

    def setContent(coffee, aContent):
        #Ensure content is between 50 and 300mg
        if(aContent >= 50 and aContent <= 300):
            coffee.caffeineContent = aContent
        else:
            print("INVALID CAFFEINE CONTENT")

    #Method to determine risky amount
    def riskyAmount(coffee):
        if(coffee.caffeineContent == -1):
            print("")
        else:
            cups = 180.0/((coffee.caffeineContent/100.0)*6.0)
            print("It would take " + str(cups) + " cups " + "of " + coffee.name + " before you are at a health risk!")
    
    

print("Lets Coffee!!!1!11!!ONE!!!1!")

aName = input("What is the name of the first coffee?")
aContent = float(input("What is " + aName + " caffeine content?"))

bName = input("What is the name of the second coffee?")
bContent = float(input("What is " + bName + " caffeine content?"))

coffee1 = Coffee(aName, aContent)
coffee2 = Coffee(bName, bContent)

coffee1.riskyAmount()

coffee2.riskyAmount()
