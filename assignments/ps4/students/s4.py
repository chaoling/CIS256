# -*- coding: utf-8 -*-
'''
Name : hashtable.py
Author  : Benjamin Lang
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
        #set tableSize and use list to hold the node
        self.tableSize = size
        self.data = [None for i in range(DEFAULT_SIZE)]

    def hash(self, id: int)->int:
        '''
        @param: id: an interger reperesting the bidId to be hashed
        @return: hashed value according to your hash function
        '''
        return id % self.tableSize

    def insert(self, bid: Bid)->None: 
        #create the hashed key for the given bid using hash function
        key = self.hash(int(bid.bidId))
        #retrieve the node using the key
        node = self.data[key]
        #if no entry found for the key location
        # assign this node to the key position
        if node is None:
            node = Node(bid, key=key)
            self.data[key] = node
        #else if node is not used
        # assign old node key to None, set to key, set old node to bid and old node next to None
        elif node.key is not None:
            node.key = key
            node.bid = bid
            node.next = None
            self.data[key] = node
        #else ind the nxt open node, add new node to the end of the chain
        else:
            while node.next:
                node = node.next#if there is a collision move to next empty position
            node.next = Node(bid, key=key)
    def printAll(self)->None:
        # interate over the list of the hashtabel, print all nodes that has non-empty
        # keys, if there is chaining on that slot, print all nodes chained as well
        for node in self.data:
            if node:#if only value, print
                print(node.val)
                if node.next:#if more than one value, keep printing
                    temp_node = node.next
                    while temp_node:
                        print(f'--{temp_node.val}--')
                        temp_node = temp_node.next


    def remove(self, bidId: str)->None:
        '''
        @param bidId the id of the bid to be removed from the hash tabel
        '''
        key = self.hash(int(bidId))
        node = self.data[key]
        if node and node.key:
            if node.val.bidId == bidId:#search for node to remove
                if node.next is None:#removes if there are no connected values
                    node.key = None
                    return
                else:
                    self.data[key] = node.next#replaces value to be removed with next value
                    return
            else:
                current_val = node.next#stores next value
                previous_val = node#stores previous value
                while current_val:#moves over values until node is empty
                    if current_val.val.bidId == bidId:
                        previous_val.next = current_val.next
                        current_val = None
                        return
        else:
            print('Node does not exist in this table')
            
    def search(self, bidId: str)->Bid:
        '''
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        key = self.hash(int(bidId))
        node = self.data[key]
        if node and node.key:
            if node.val.bidId == bidId:#search for node
                if node.next is None:#returns if there are no linked values
                    return node.val#if entry found for the hashed key, return the bid
                else:#elif entry found in the chained list, return the bid
                    self.data[key] = node.next#replaces value to be searched with next value
                    return node.val
            else:
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