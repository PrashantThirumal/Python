'''
Created on May 31, 2019
Linked Lists
@author: Prashant
'''


class Node:
    
    #Default Constructor
    def __init__(self, data = None, next_node = None):
        self.data = data
        self.next_node = next_node
    
    def get_data(self):
        return self.data
    
    def get_next(self):
        return self.next_node
    
    def set_next(self, new_next):
        self.next_node = new_next
    
    def set_data(self, d):
        self.data = d
        
class LinkedList:
    
    #Default Constructor
    def __init__(self, head = None):
        self.head = head
        self.size = 0
    
    def get_size(self):
        return self.size
    
    #Insert Method
    def insert(self, d):
        #Create the node
        new_node = Node(d, None)
        
        #If list is empty
        if(self.head == None):
            self.head = new_node
        
        #List is not empty, traverse to the end of the list and then add data
        else:
            temp = self.head
            while(temp.next_node != None):
                temp = temp.next_node
            temp.next_node = new_node
        
        self.size += 1
    
    #Remove method
    def remove(self, d):
        this_node = self.head
        prev_node = None
        
        while this_node:
            if(this_node.get_data() == d):
                if prev_node:
                    prev_node.set_next(this_node.get_next())
                    
                else: 
                    self.head = this_node.get_next()
                self.size -= 1
                return True #data removed
            else:
                prev_node = this_node
                this_node = this_node.get_next()
        
        return False #Data not found
    
    def find(self, d):
        this_node = self.head
        while this_node:
            if this_node.get_data() == d:
                return d
            else:
                this_node = this_node.get_next()
        return None        
        
    
myList = LinkedList()
myList.insert(5)
myList.insert("hello")
myList.insert(8)
print("size=" + str(myList.get_size()))
myList.remove(8)
print("size=" + str(myList.get_size()))
myList.remove(12)
print("size=" + str(myList.get_size()))
print(myList.find("hello"))
