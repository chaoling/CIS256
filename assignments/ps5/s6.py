'''
Name : trees.py
Author  : Dylan McCoy
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

class Node(object): #define bst node class to hold bids
    def __init__(self,bid,left=None,right=None): #every node contains a bid and pointers to left/right child nodes
        self.bid = bid
        self.left = left
        self.right = right

class BinarySearchTree(object):
    def __init__(self, root=None):
        self.root = root #bst root is initialized to None

    def InOrderTraversal(self): #performs 'in order' traversal (left>node>right)
        def inOrder(node: Node)->None: #helper function for recursive calls
            if node is not None:
                inOrder(node.left) #traverses the left subtree first
                print(f'{node.bid}->') #prints the bid at the current node
                inOrder(node.right) #traverses the right subtree
        inOrder(self.root) #call inOrder function and pass root

    def PreOrderTraversal(self): #performs 'pre order' traversal (node>left>right)
        def preOrder(node: Node)->None: #helper function for recursive calls
            if node is not None:
                print(f'{node.bid}->') #prints the bid at the current node
                preOrder(node.left) #traverses the left subtree
                preOrder(node.right) #traverses the right subtree
        preOrder(self.root) #call preOrder function and pass root

    def PostOrderTraversal(self): #performs 'post order' traversal (left>right>node)
        def postOrder(node: Node)->None: #helper function for recursive calls
            if node is not None:
                postOrder(node.left) #traverses the left subtree
                postOrder(node.right) #traverses the right subtree
                print(f'{node.bid}->') #prints the bid at the current node
        postOrder(self.root) #call postOrder and pass root

    def insert(self, bid: Bid)->None: #insert bid into the bst with the following properties
        def addNode(node: Node, bid: Bid)->None:
            if node.bid.bidId > bid.bidId: #if bid ID is smaller then go left
                if not node.left:
                    node.left = Node(bid) #insert bid as left child
                else:
                    addNode(node.left, bid) #go left to find correct position for this bid
            else: #if bid ID is larger then go right
                if not node.right:
                    node.right = Node(bid) #insert bid as right child
                else:
                    addNode(node.right, bid) #go right to find correct position for this bid

        if self.root is None:
            self.root = Node(bid) #if the tree is empty then set bid as root
        else:
            addNode(self.root, bid) #otherwise insert recursively

    def search(self, bidId: str)->Bid: #search for bid in the bst by its ID
        def searchNode(node, bidId):
            if not node:
                return None #bid not found
            elif bidId == node.bid.bidId:
                return node.bid #return matching bid
            elif bidId < node.bid.bidId:
                return searchNode(node.left, bidId) #search in the left subtree
            else:
                return searchNode(node.right, bidId) #search in the right subtree
        return searchNode(self.root, bidId)

    def remove(self, bidId: str)->None: #remove a bid from the bst via ID
        def findMinNode(node):
            tmp = node.right #start at the right subtree
            while tmp.left:
                tmp = tmp.left #find leftmost/smallest value node
            return tmp

        def removeNode(node: Node, bidId: int)->Node:
            if node is None:
                return None #base case - node not found
            elif bidId < node.bid.bidId:
                node.left = removeNode(node.left, bidId) #search the left subtree
            elif bidId > node.bid.bidId:
                node.right = removeNode(node.right, bidId) #search the right subtree
            else: #node to be deleted found
                if node.left is None and node.right is None:
                    node = None #no children - remove node
                elif node.right is None:
                    node = node.left #single child (left)
                elif node.left is None:
                    node = node.right #single child (right)
                else:
                    minNode = findMinNode(node) #find minimum node in the right subtree
                    node.bid = minNode.bid #replace node's bid with min. node
                    node.right = removeNode(node.right, minNode.bid.bidId) #remove min. node
            return node

        removeNode(self.root, bidId)

def str2float(origin: str, ch: List) ->float:
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
def loadBids(csvPath: str, bst: BinarySearchTree)->None:
    # opening csv file
    print(f"now loading csv file {csvPath}...")
    try:
        with open(csvPath,'r') as file:
            #reader = DictReader(file)
            reader = csv.reader(file)
            header = next(reader)
            # clean up the header as keys
            keys = [key.replace(" ", "").lower() for key in header]
            # print(keys)
            # printing each row of table
            for row in reader:
                entry = dict(zip(keys, row))
                bid = Bid(id=entry.get('auctionid', ""), title=entry.get('auctiontitle', None), fund=entry.get('fund', ""), amt=str2float(entry.get('winningbid', '0.0'), ['$', ',']))
                bst.insert(bid)
    except Exception as ex:
        print(f"exception occurred, {ex}")

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