'''
Name : hashtable.py
Author  : Katie Inman
Version : 1.0
Description : use hashtable to store the csv data set
'''

# importing DictReader class from csv module
import csv
from typing import List
import argparse
import time

# class to hold bid information
class Bid(object):
    def __init__(self,id=None,title=None,fund=None,amt=0.0):
        self.bidId = id
        self.title = title
        self.fund = fund
        self.amount = amt

    def __str__(self):
        return f"ID: {self.bidId}, Title: {self.title}, Fund: {self.fund}, Amount: {self.amount}"

class Node(object):
    #define node class to hold bids in case of collisions
    def __init__(self,bid,key=None):
        self.key = key
        self.bid = bid
        self.next = None

'''
Hash Table class definition
This class implements a hash table with chaining to handle collissions
'''
DEFAULT_SIZE = 179
class HashTable(object):
    def __init__(self, size=DEFAULT_SIZE):
        #Initialize the hash table with a specific size
        self.tableSize = size
        self.data = [None for _ in range(size)]

    def hash(self, id: int)->int:
        '''
        Calculate a hash value for a given bid ID
        @param: id: bidId to be hashed
        @return: hashed value
        '''
        return id % self.tableSize
    
    def insert(self, bid: Bid)-> None:
        '''
        Insert a bid into the hash table
        @param: bid: the data to be inserted to the hash table
        '''
        key = self.hash(int(bid.bidId)) #Calculate hash key for the bid
        keynode = self.data[key] #Retrieve the node at the key location
        #If no entry found, create a new node
        if not keynode:
            self.data[key] = Node(bid, key=key)
        else:
            #If there's a collision, find the next available position
            while keynode.next:
                keynode = keynode.next    
            keynode.next = Node(bid, key=key)

    def printAll(self)->None:
        '''
        Print all bids from the hash table
        '''
        for node in self.data:
            while node:
                print(f"-->{node.bid} ")
                node = node.next

    def remove(self, bidId: str)->None:
        '''
        Remove a bid from the hash table by its bid ID
        @param bidId: the id of the bid to be removed
        '''
        key = self.hash(int(bidId)) #calculate the hash key
        keynode = self.data[key] #retrieve the node at the key location
       
        if keynode is None:
            print(f'Bid {bidId} not found')
            return
            
        #If the first node in the chain matches the bidId, remove it
        if keynode.bid.bidId == bidId:
            self.data[key] = keynode.next
            return

        #If the id is somewhere in the chain, find and remove it
        curr_node = keynode.next
        prev_node = keynode
        while curr_node:
            if curr_node.bid.bidId == bidId:
                prev_node.next = curr_node.next #remove the node
                return
                
            prev_node = curr_node
            curr_node = curr_node.next
                
        else:
            print(f"bid {bidId} not found")

    def search(self, bidId: str)->Bid:
        '''
        Search for a bid in the hash table by its bid ID
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        key = self.hash(int(bidId)) #Caulate the hash key
        keynode = self.data[key] #Retrieve the node at the key location
        while keynode:
            if keynode.bid.bidId == bidId:
                return keynode.bid #Return bid if found
            keynode = keynode.next #Continue to the next node in the chain
        return None #Return None if not found

def str2float(origin: str, ch: List) ->str:
    '''
    Convert string to float, stripping unwanted characters
    @param origin: string to be converted
    @param ch: list of characters to be stripped
    @return: converted float value
    ''' 
    for c in ch:
        origin = origin.replace(c,'') #Remove unwanted characters

    return float(origin.strip()) #Convert to float and return

def logtime(func):
    #Decorate to log the time taken by the function
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        with open('timelog.txt','a') as outfile:
            #timestamp, func name, time spent
            record = f'at {time.time()}:\t{func.__name__}\t time spent: {total_time}(sec)\n'
            print(record)
            outfile.write(record)
        return result
    return wrapper


@logtime
def loadBids(csvPath: str, bidTable: HashTable)->None:
    '''
    Load a CSV file containing bids into a hashTable
    @param csvPath the path to the CSV file
    @param bidTable the hash table to store the bids
    @return a hashTable holding all the bids read
    '''
    # opening csv file
    print(f"now loading csv file {csvPath}...")

    try:
        with open(csvPath,'r') as file:
            reader = csv.reader(file) #Read CSV file
            header = next(reader) #Read the header
            keys = [key.replace(" ","").lower() for key in header] #Clean header
            for row in reader:
                entry = dict(zip(keys,row)) #Create a dictionary from the row from row and header
                bid = Bid(id=entry.get('auctionid',""),title=entry.get('auctiontitle',None),fund=entry.get('fund',""),amt=str2float(entry.get('winningbid','0.0'),['$',',']))
                bidTable.insert(bid) #Insert bid into the hash table
    except Exception as ex:
        print(f"excetion occurred, {ex}")


if __name__ == "__main__":
    #Command-line interface setup
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='eBid_Monthly_Sales_Dec.csv', help='path to the csv file')
    parser.add_argument('-i','--id', help='bidId for the bid')

    args = parser.parse_args()
    menu = {}
    menu['1']="Load Bids"
    menu['2']="Display All Bids"
    menu['3']="Find Bid"
    menu['4']="Remove Bid"
    menu['9']="Exit"

    bidTable = HashTable()

    #Main loop for user interaction
    while True:
        options=menu.keys()
        for entry in options:
            print(entry, menu[entry]) #display the menu items

        selection=input("Enter choices: ")
        
        if selection =='1':
            loadBids(args.path, bidTable)
        elif selection == '2':
            print("display bids....")
            bidTable.printAll()

        elif selection == '3':
            print("search")
            id = args.id
            if not id:
                id = input("please enter a bid ID: ")
            bid = bidTable.search(id)
            print(bid)

        elif selection == '4':
            print("remove bid")
            id = args.id
            if not id:
                id = input("please enter a bid ID: ")
            bidTable.remove(id)
        elif selection == '9':
            print("Bye!")
            break
        else:
            print("Unknown Option Selected!")