'''
Name : trees.py
Author  : Katie Inman
Version : 1.0
Description : use trees to store the csv data set
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
    #define bst node class to hold bids
    def __init__(self,bid,left=None,right=None):
        self.bid = bid
        self.left = left
        self.right = right

'''
BST class definition
Define a class containing data memebers and methods to
implement a binary search tree
'''

class BinarySearchTree(object):
    def __init__(self, root=None):
        '''
        Initialize the structures used to hold bids
        '''
        self.root = root


    def InOrderTraversal(self):
        '''
        Traverse the BST in order and print the bids
        '''
        def inOrder(node: Node)-> None:
            if node is not None:
                inOrder(node.left) #traverse left subtree
                print(f"{node.bid} -->") #print current node's bid
                inOrder(node.right) #traverse right subtree
        
        inOrder(self.root)


    def PreOrderTraversal(self):
        '''
        Traverse the BST in pre-order and print the bids
        '''
        def preOrder(node: Node)-> None:
            if node is not None:
                print(f"{node.bid} -->") #print current node's bid
                preOrder(node.left) #traverse left subtree
                preOrder(node.right) #traverse right subtree
                
        preOrder(self.root)


    def PostOrderTraversal(self):
        '''
        Traverse the BST in post-order and print the bids
        '''
        def postOrder(node: Node)-> None:
            if node is not None:
                postOrder(node.left) #traverse left subtree
                postOrder(node.right) #traverse right subtree
                print(f"{node.bid} -->") #print current node's bid

        postOrder(self.root)


    def insert(self, bid: Bid)-> None:
        '''
        Insert a bid into the BST
        @param: bid: the data to be inserted to the BST
        '''
        
        def addNode(node: Node, bid: Bid)-> None:
            '''
            Insert a bid into the tree recursively
            '''
            if node.bid.bidId > bid.bidId: #compare bid IDs
                if not node.left:  #if left child is empty, insert bid
                    node.left = Node(bid)
                else:
                    addNode(node.left, bid) #recurse to the left child
            else:
                if not node.right: #if right child is empty, insert bid
                    node.right = Node(bid)
                else:
                    addNode(node.right, bid) #recurse to the right child
     
        if self.root is None: #if BST is empty, set root to new node
            self.root = Node(bid)
        else:
            addNode(self.root, bid) #recurse starting from the root

    def search(self, bidId: str)-> Bid:
        '''
        Search for a bid by its ID in the BST
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        def searchNode(node: Node, bidId: str)->Bid:
            if not node:
                return None #node not found
            elif bidId == node.bid.bidId:
                return node.bid #match found
            elif bidId < node.bid.bidId:
                return searchNode(node.left, bidId) #recurse left
            else:
                return searchNode(node.right, bidId) #recurse right

        return searchNode(self.root, bidId)

    def remove(self, bidId: str)->None:
        '''
        Remove a bid by its ID from the BST
        @param bidId the id of the bid to be removed from the bst
        '''
        def findMinNode(node: Node):
            tmp = node.right
            while tmp.left:
                tmp = tmp.left #find the leftmost node in the right subtree
            return tmp
        
        def removeNode(node: Node, bidId: int)-> Node:
            '''
            Remove a node recursively
            '''
            if node is None:
                return None #base case: node is None 
                
            if bidId < node.bid.bidId: #bid ID is smaller, go left
                node.left = removeNode(node.left, bidId)
            elif bidId > node.bid.bidId: #bid ID is larger, go right
                node.right = removeNode(node.right, bidId)    
            else:
                if node.left is None and node.right is None:
                    node = None #remove leaf node
                elif node.right is None:
                    tmp = node 
                    node = node.left #replace node with its left child
                    tmp = None
                elif node.left is None:
                    tmp = node
                    node = node.right #replace node with its right child
                    tmp = None
                else:
                    minNode = findMinNode(node) #find the smallest node in the right subtree
                    node.bid = minNode.bid #replace current node with the minimum node
                    node.right = removeNode(node.right, minNode.bid.bidId) #recursively remove the minimum node
            return node

        self.root = removeNode(self.root, bidId) #call removeNode with the root    

def str2float(origin: str, ch: List) ->str:
    '''
    Convert string to float, stripping unwanted characters
    '''
    for c in ch:
        origin = origin.replace(c,'')

    return float(origin.strip())

def logtime(func):
    '''
    Decorator to log the execution time of functions
    '''
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
def loadBids(csvPath: str, bst: BinarySearchTree)->None:
    '''
    Load a CSV file containing bids into a BST
    @param csvPath the path to the CSV file
    @return a hashTable holding all the bids read
    '''
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
                bst.insert(bid)
    except Exception as ex:
        print(f"excetion occurred, {ex}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('-p','--path', default='eBid_Monthly_Sales_Dec.csv',
                    help='path to the csv file')
    parser.add_argument('-i','--id',
                    help='Bid ID for the bid')

    args = parser.parse_args()
    menu = {}
    menu['1']="Load Bids"
    menu['2']="Display All Bids"
    menu['3']="Find Bid"
    menu['4']="Remove Bid"
    menu['9']="Exit"

    bst = BinarySearchTree()

    while True:
        options=menu.keys()
        for entry in options:
            print(entry, menu[entry]) #display the menu item

        selection=input("Enter choices: ")
        if selection =='1':
            loadBids(args.path, bst)
        elif selection == '2':
            print("display bids....")
            bst.InOrderTraversal()

        elif selection == '3':
            print("search")
            id = args.id
            if not id:
                id = input("please enter a bid ID: ")
            bid = bst.search(id)
            print(bid)

        elif selection == '4':
            print("remove bid")
            id = args.id
            if not id:
                id = input("please enter a bid ID: ")
            bst.remove(id)
        elif selection == '9':
            print("Bye!")
            break
        else:
            print("Unknown Option Selected!")