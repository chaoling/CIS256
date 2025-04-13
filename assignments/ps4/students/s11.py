'''
Name : hashtable.py
Author  : Alex Vogt
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
        self.tableSize = size
        #this is to initialize the list related to None
        self.data = [None] * size

    def hash(self, id: int)->int:
      #this line is used to calculate the index
        return int(id) % self.tableSize

    def insert(self, bid: Bid)->None:
      #I had do to a little extra leg work to get this command working, I couldn't figure out
      #how to get this command to not error out but basically this gets multiple bids to be
      #stored at the same index location in the table
        key = self.hash(int(bid.bidId))
        node = self.data[key]
        if node is None:
            self.data[key] = Node(bid,key)
        else:
            while node.next is not None:
                node = node.next
            node.next = Node(bid,key)

    def printAll(self)->None:
      #this one errored on me a couple times, I forgot to tab the if portion correctly
      #but this was to display all bids that are stored in the table
        for node in self.data:
          while node is not None:
            if node.key is not None:
              print(node.val)
            node = node.next

    def remove(self, bidId: str)->None:
      #removes the bidId from the table to calculate the key and searches the
      #indexfor the matching node
        key = self.hash(int(bidId))
        node = self.data[key]
        prev = None

        while node is not None and node.val.bidId != bidId:
            prev = node
            node = node.next

        if node is not None:
          if prev is None:
            self.data[key] = node.next
          else:
            prev.next = node.next

    def search(self, bidId: str)->Bid:
      #this basically receives a specific bid in the bidId
        key = self.hash(int(bidId))
        node = self.data[key]

        while node is not None:
          if node.val.bidId == bidId:
            return node.val
          node = node.next

        return None

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
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='eBid_Monthly_Sales_Dec.csv',
                    help='path to the csv file')
    parser.add_argument('-i','--id',
                    help='bidId for the bid')

    # Pass an empty list to parse_args() to avoid parsing system arguments
    args = parser.parse_args([]) # This is the change

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