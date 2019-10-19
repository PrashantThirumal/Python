'''
Created on May 31, 2019

@author: Prashant
'''
#Note for this homework we are using a doubly linked list
#That is we need head, current and previous

class Node:
    #Default Constructor
    def __init__(self, data = None, prev_node = None, next_node = None):
        self.data = data
        self.next_node = next_node
        self.prev_node = prev_node
    
    def get_data(self):
        return self.data
    
    def get_next(self):
        return self.next_node
    
    def get_prev(self):
        return self.prev_node
    
    def set_next(self, new_next):
        self.next_node = new_next
    
    def set_prev(self, new_prev):
        self.prev_node = new_prev
    
    def set_data(self, d):
        self.data = d

class GenLinkedList:
    
    #Default
    def __init__(self, head = None):
        self.head = self.prev = self.curr = self.next = None
        self.size = 0
    
    #Insert Method
    def insert(self, data):
        #Create the Node
        newNode = Node(data, None)
        
        #Check if list is empty
        if(self.head == None):
            self.head = newNode
            self.curr = self.head
        #If list is not empty
        temp = self.head
        #Traverse to the end of the list and then add Data
        while (temp.next_node != None):
            temp = temp.next_node
            
        temp.next_node = newNode #Adds new node at the end of the list
    
    #Print method. Done to check linked list
    def LLprint(self):
        temp = self.head
        
        while(temp.next_node != None):
            print(temp.data)
            temp = temp.next_node
    
    def get_current(self):
        if(self.curr != None):
            return self.curr.data
        else:
            return None
    
    def set_current(self, aData):
        if(self.curr != None):
            self.curr.data = aData  
    
    def move_current_forward(self):
        if(self.curr != None):
            self.prev = self.curr
            self.curr = self.curr.next
            
    def insert_after_curr(self, aData):
        newNode = Node(aData, None)
        if(self.curr != None):
            newNode.next_node = self.curr.next
            self.curr.next = newNode
    
    def delete_curr(self):
        if(self.curr != None and self.prev != None):
            self.prev.next = self.curr.next
            self.curr = self.curr.next
        
        elif(self.curr != None and self.prev == None):
            self.head = self.curr.next
            self.curr = self.head
        
        else:
            print("Current was null...for some reason")
    
 
class Movie:
    
    # A constructor
    def __init__(self, aName, aYear, aRating, aDirector, aGross):
        self.name = aName
        self.year = aYear
        self.rating = aRating
        self.director = aDirector
        self.gross = aGross
         
    # Accessors and Mutators
    def get_name(self):
        return self.name
     
    def get_year(self):
        return self.year
     
    def get_rating(self):
        return self.rating 
     
    def get_director(self):
        return self.director 
     
    def get_gross(self):
        return self.gross
     
    def set_name(self, aName):
        self.name = aName
    
    def set_year(self, aYear):
        self.year = aYear
            
    def set_rating(self, aRating):
        if(aRating >= 1 and aRating <= 5):
            self.rating = aRating
        else:
            print("Invalid Rating")
    
    def set_director(self, aDirector):
        self.director = aDirector 
    
    def set_gross(self, aGross):
        if(aGross > 0):
            self.gross = aGross
        else:
            print("Invalid Box Office Gross")
    
    # Other Methods
    def equals(self, other):
        return (self.name == other.name
            and self.year == other.year 
            and self.rating == other.rating  
            and self.director == other.director
            and self.gross == other.gross)
    
    def to_string(self):
        print("==================================")
        print("Name: " + self.name)
        print("Year: " + str(self.year))
        print("Rating: " + str(self.rating))
        print("Director: " + self.director)
        print("Gross: " + str(self.gross))

'''
class MovieDatabase:
    movie_list = GenLinkedList()
    aMovie = Movie()
    
    def add_movie(self, aMovie):
        movie_list.insert(aMovie)
    
    def remove_title(self, aName):
        movie_list.remove(aName)
        
    def search_title(self, aName):
        movie_list.
            
'''
        
movie_list = GenLinkedList()

choice = int(input("Enter 1: To Add a movie" 
                   + "\nEnter 2: To Add a movie"))       
    
    
        
    
