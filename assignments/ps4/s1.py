'''
Name : hashtable.py
Author  : FirstName LastName
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
        self.bid = bid
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
        self.tableSize = size
        self.data = [None for _ in range(DEFAULT_SIZE)]
    
    def hash(self, id: int)->int:
        '''
        FIXME(2): Implement logic to calculate a hash value
        @param: id: an interger reperesting the bidId to be hashed
        @return: hashed value according to your hash function
        '''
        return id % self.tableSize
        

    def insert(self, bid: Bid)->None:
        '''
        FIXME(3) implement logic to insert a bid
        @param: bid: the data to be inserted to the hash table
        '''
        
        #create the hashed key for the given bid using hash function
        key = self.hash(int(bid.bidId))

        #retrieve the node using the key
        keynode = self.data[key]

        #if no entry found for the key location
        # assign this node to the key position
        if not keynode:
            keynode = Node(bid, key=key)
            self.data[key] = keynode
        elif not keynode.key:
            keynode.key = key
            keynode.bid = bid
            keynode.next = None
            self.data[key] = keynode
        else:
            #collision: find the next empty postion in the key location
            while keynode.next:
                keynode = keynode.next
            keynode.next = Node(bid, key=key)
        
            
        

        #else if node is not used
        # assign old node key to None, set to key, set old node to bid and old node next to None

        #else find the nxt open node, add new node to the end of the chain
        
    def printAll(self)->None:
        '''
        FIXME(4): Implement logic to print all bids from the hash table
        '''
        
        # interate over the list of the hashtabel, print all nodes that has non-empty
        # keys, if there is chaining on that slot, print all nodes chained as well
        for node in self.data:
            if node:
                if node.next:
                    print(node.bid)
                    tmp = node.next
                    while tmp:
                        print(f"-->{tmp.bid} ")
                        tmp = tmp.next
                    
        

    def remove(self, bidId: str)->None:
        '''
        @param bidId the id of the bid to be removed from the hash tabel
        '''
        
        #FIXME(5) search and remove the node from the hash table  
        key = self.hash(int(bidId))
        keynode = self.data[key]

        if keynode and keynode.key:
            if keynode.bid.bidId == bidId:
                #found the node to be removed
                if keynode.next is None:
                    keynode.key = None
                    return 
                else:
                    self.data[key] = keynode.next
                    return
            else:
                cur = keynode.next
                pre = keynode
                while cur:
                    if cur.bid.bidId == bidId:
                        pre.next = cur.next
                        cur = None
                        return
                    pre = cur
                    cur = cur.next
        else:
            print(f"sorry, no such node exists in the hash table")

    def search(self, bidId: str)->Bid:
        '''
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        pass
        #FIXME(6) Implement logic to search for and return a bid

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
                print(bid)
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