'''
Name : hashtable.py
Author  : Dylan McCoy
Version : 1.0
Description : use hashtable to store the csv data set
'''

#import dictReader class from csv module
import csv
from typing import List
import argparse
import time

#class for holding information of the bids
class Bid(object):
    def __init__(self,id=None,title=None,fund=None,amt=0.0):
        self.bidId = id
        self.title = title
        self.fund = fund
        self.amount = amt

    def __str__(self):
        return f"ID: {self.bidId}, Title: {self.title}, Fund: {self.fund}, Amount: {self.amount}"

class Node(object):
    #defines a node class to hold the bids
    def __init__(self,bid,key=None):
        self.key = key
        self.bid = bid
        self.next = None

DEFAULT_SIZE = 179
class HashTable(object):
    def __init__(self, size=DEFAULT_SIZE):
        #initialize hash table with fixed size list and each spot starts with None
        self.tableSize = size
        self.data = [None for _ in range(DEFAULT_SIZE)]

    def hash(self, id: int)->int:
        #compute hash value for given bid id using mod operator to make sure...
        #that the index stays within the size of the table limit
        return id % self.tableSize

    def insert(self, bid: Bid)->None:
        #insert new bid into hash table at appropriate index
        key = self.hash(int(bid.bidId))  #compute hash key from bid id
        keynode = self.data[key] #get the existing node at this index

        if not keynode:
            #if no existing node at this index then create new node and store it
            keynode = Node(bid, key=key)
            self.data[key] = keynode
        elif not keynode.key:
            #if a node does exist but unassigned yet then use it to store new bid
            keynode.key = key
            keynode.bid = bid
            keynode.next = None
            self.data[key] = keynode
        else:
            #if collision occurs then go through linked list until finding an empty spot
            while keynode.next:
                keynode = keynode.next
            keynode.next = Node(bid, key=key) #add new node at end of chain

    def printAll(self)->None:
        #prints all of the bids that are currently stored in the table
        for node in self.data:
            if node:
                print(node.bid)  #print first bid in this index
                if node.next:
                    #if multiple bids due to collisions then print them
                    tmp = node.next
                    while tmp:
                        print(f"-->{tmp.bid} ")
                        tmp = tmp.next

    def remove(self, bidId: str)->None:
        #remove bid from hash table after locating in the list and then adjust links
        key = self.hash(int(bidId)) #compute hash key for given bid id
        keynode = self.data[key] #get the node in this index

        if keynode and keynode.key:
            if keynode.bid.bidId == bidId:
                if keynode.next is None:
                    #if this is the only node in this index then remove it
                    self.data[key] = None
                else:
                    #if there are multiple nodes here then shift the next one up
                    self.data[key] = keynode.next
            else:
                #if bid is not in first node then search through chain
                cur = keynode.next
                pre = keynode
                while cur:
                    if cur.bid.bidId == bidId:
                        pre.next = cur.next  #update link to remove node
                        cur = None
                        return
                    pre = cur
                    cur = cur.next
        else:
            print(f"No such node exists in the hash table.")

    def search(self, bidId: str)->Bid:
        #search for bid using the id then return its bid object if it is found
        key = self.hash(int(bidId)) #computes hash key
        keynode = self.data[key] #gets the node in this index

        while keynode:
            if keynode.bid.bidId == bidId:
                return keynode.bid  #return bid if its found
            keynode = keynode.next #move to next node in chain if you have to
        return None  #returns None if bid wasnt found

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
    #opening csv file
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

    args = parser.parse_args()
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
