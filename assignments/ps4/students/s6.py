'''
Name : hashtable.py
Author  : Michael Moschetta
Version : 1.0
Description : use hashtable to store the csv data set
'''

# importing DictReader class from csv module
import csv
from typing import List
#import argparse
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
    #define node class to hold bids
    def __init__(self,bid,key=None):
        self.key = key
        self.val = bid
        self.next = None

'''
Hash Table class definition
Define a class containing data memebers and methods to
implement a hash table with chaining
'''
DEFAULT_SIZE = 179
class HashTable(object):
    def __init__(self, size=DEFAULT_SIZE):
        #FIXME(1): Initialize the structures used to hold bids
        #set tableSize and use list to hold the node

        #Initializes the hash table with the given default size
        self.tableSize = size
        #Creates a list to hold nodes
        self.data = [None] * size

    def hash(self, id: int)->int:

      #Hash function to calculate index for the bidID
      return int(id) % self.tableSize
      '''
        FIXME(2): Implement logic to calculate a hash value
        @param: id: an interger reperesting the bidId to be hashed
        @return: hashed value according to your hash function
        '''



    #Inserts a bid into the hash table
    def insert(self, bid: Bid)->None:

      #Gets the hash key for the given BidID
      key = self.hash(bid.bidId)
      #Retrieves the node at the hash key
      node = self.data[key]

      #If no node exists at the key it creates a new node
      if node is None:
        self.data[key] = Node(bid, key)
      else:
        #If there's already a node it will traverse the chain and add the new node at the end
        while node.next:
          node = node.next
        node.next = Node(bid, key)
        '''
        FIXME(3) implement logic to insert a bid
        @param: bid: the data to be inserted to the hash table
        '''

        #create the hashed key for the given bid using hash function

        #retrieve the node using the key

        #if no entry found for the key location
        # assign this node to the key position

        #else if node is not used
        # assign old node key to None, set to key, set old node to bid and old node next to None

        #else ind the nxt open node, add new node to the end of the chain

    #Prints all bids in the hash table
    def printAll(self)->None:

      for i in range(self.tableSize):
        node = self.data[i]
        while node:
            #Prints each bid and moves it to the next node
            print(node.val)
            node = node.next
        '''
        FIXME(4): Implement logic to print all bids from the hash table
        '''

        # interate over the list of the hashtabel, print all nodes that has non-empty
        # keys, if there is chaining on that slot, print all nodes chained as well

    #Removes a bid from the hash table using its bidId
    def remove(self, bidId: str)-> None:

      #Calculates the key for the given bidId
      key = self.hash(bidId)
      #Retrieves the node at the hashed key
      node = self.data[key]
      #Initializes previous node as none
      prev = None

      while node:
        if node.val.bidId == bidId:
          #If the bid is found, it removes it from the chain
          if prev:
            #Bypasses the node
            prev.next = node.next
          else:
            #Updates the head of the chain
            self.data[key] = node.next
          return
        #updates the previous node
        prev = node
        #Move to the next node in the chain
        node = node.next

        '''
        @param bidId the id of the bid to be removed from the hash tabel
        '''

        #FIXME(5) search and remove the node from the hash table

    #Searches for a bid in the hash table by its bidId
    def search(self, bidId: str)->Bid:

      #Calculates the key for the given bidId
      key = self.hash(bidId)
      #Retrieves the node at the hashed key
      node = self.data[key]

      while node:
        #If the bid is found it returns it
        if node.val.bidId == bidId:
          return node.val
        #moves to the next node in the chain
        node = node.next

      #returns none if the bid was not found
      return None

      '''
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''

        #FIXME(6) Implement logic to searf for and return a bid

        #calculate the key for the given bid
        #if entry found for the hashed key, return the bid
        #elif entry found in the chained list, return the bid
        #else return None


def str2float(origin: str, ch: List) ->str:
    #Convert string to float, stripping ch. e.g: '$6,000.00 ' -> 6000.00
    for c in ch:
        origin = origin.replace(c,'')

    return float(origin.strip())

def logtime(func):
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
    @return a hashTable holding all the bids read
    '''
    # opening csv file
    print(f"now loading csv file {csvPath}...")

    try:
        with open(csvPath,'r') as file:
            #reader = DictReader(file)
            reader = csv.reader(file)
            header = next(reader)
            # clean up the header as keys
            keys = [key.replace(" ","").lower() for key in header]
            # print(keys)
            # printing each row of table
            for row in reader:
                entry = dict(zip(keys,row))
                bid = Bid(id=entry.get('auctionid',""),title=entry.get('auctiontitle',None),fund=entry.get('fund',""),amt=str2float(entry.get('winningbid','0.0'),['$',',']))
                bidTable.insert(bid)
    except Exception as ex:
        print(f"excetion occurred, {ex}")


if __name__ == "__main__":

  #parser = argparse.ArgumentParser(description='Process cmd line arguments')
  #parser.add_argument('-p','--path', default='sample_data/eBid_Monthly_Sales_Dec.csv',
                    #help='path to the csv file')
  #parser.add_argument('-i','--id',
                   # help='bidId for the bid')

  #args = parser.parse_args()
  menu = {}
  menu['1']="Load Bids"
  menu['2']="Display All Bids"
  menu['3']="Find Bid"
  menu['4']="Remove Bid"
  menu['9']="Exit"

  bidTable = HashTable()

  while True:
        options=menu.keys()
        for entry in options:
            print(entry, menu[entry]) #display the menu item

        selection=input("Enter choices: ")
        if selection =='1':
            loadBids('sample_data/eBid_Monthly_Sales_Dec.csv', bidTable)
        elif selection == '2':
            print("display bids....")
            bidTable.printAll()

        elif selection == '3':
            print("search")
            #id = args.id
            #if not id:
            id = input("please enter a bid ID: ")
            bid = bidTable.search(id)
            print(bid)

        elif selection == '4':
            print("remove bid")
            #id = args.id
            #if not id:
            id = input("please enter a bid ID: ")
            bidTable.remove(id)
        elif selection == '9':
            print("Bye!")
            break
        else:
            print("Unknown Option Selected!")
