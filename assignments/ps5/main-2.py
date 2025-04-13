'''
Name : trees.py
Author  : Kristi Ogden
Version : 1.0
Description : use trees to store the csv data set

----reflection----
The purpose of this code is to explore the data structure of a binary search tree.
The approach was to implement all basic functionality, like adding and removing and searching
and then test with a small sample set to make sure that the functionality worked.
The approach I took was to take the todos literally and implement them as close to the
pseudocode as possible.
One problem I ran into is that initially I did not cast integers from the bid ids. They
are stored as strings, so depending on the dataset the comparison may or may not work.
I approached fixing this by standardizing all data points as integers in comparisons
Another issue I ran into is that the remove function only sometimes works
so far debugging has been less than helpful in finding the source of this issue
another issue I ran into was how to print a bid. I did not intially see that a string
formatter was already set up for a bid object and wasted significant time trying to make what
looked "right"
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
        FIXME(1): Initialize the structures used to hold bids
        '''
        #bst root is initialized to None or user defined
        self.root = root


    def InOrderTraversal(self):
        '''
        FIXME(2): Implement logic to traverse a BST in order
        '''
        def inOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''
            if node:
            #if node is not None:
            #recursively call inOrder() on left subtree
                if node.left:
                    inOrder(node.left)
            #print current node's bid info
                print(node.bid)
            #recursively call inOrder() on right subtree
                if node.right:
                    inOrder(node.right)

        #call inorder function and pass root
        inOrder(self.root)


    def PreOrderTraversal(self):
        '''
        FIXME(3): Implement logic to traverse a BST pre-order
        '''
        def preOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''
            #if node is not None:
            if node:
            #print current node's bid info
                print(node.bid)
            #recursively call inOrder() on left subtree\
                if node.left:
                    preOrder(node.left)
            #recursively call inOrder() on right subtree
                if node.right:
                    preOrder(node.right)

        #call preOrder function and pass root
        preOrder(self.root)


    def PostOrderTraversal(self):
        '''
        FIXME(4): Implement logic to traverse a BST post-order
        '''
        def postOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''
            #if node is not None:
            if node:
            #recursively call inOrder() on left subtree
                if node.left:
                    postOrder(node.left)
            #recursively call inOrder() on right subtree
                if node.right:
                    postOrder(node.right)
            #print current node's bid info
                print(node.bid)


        #call postOrder function and pass root
        postOrder(self.root)


    def insert(self, bid: Bid)->None:
        '''
        FIXME(5) implement logic to insert a bid
        @param: bid: the data to be inserted to the BST
        '''
        pass
        def addNode(node: Node, bid: Bid)->None:
            '''
            FIXME(6) implement inserting a bid into the tree recursively
            '''
            #if current node is bigger than bid, insert it to the left subtree
            if int(node.bid.bidId) > int(bid.bidId):
              #if no left node, this bid became the left node
                if not node.left:
                    node.left = Node(bid)
              #else recurse down the left subtree
                else:
                    addNode(node.left, bid)
            #else:
            else:
              #if no right node, this bid became the right node
                if not node.right:
                    node.right = Node(bid)
              #else recurse down the right subtree
                else:
                    addNode(node.right, bid)

        #if self.root is None:
        if not self.root:
        # self.root is assigned to new node bid
            self.root = Node(bid)
        #else, call recursive function addNode(self.root, bid)
        else:
            addNode(self.root, bid)



    def search(self, bidId: str)->Bid:
        '''
        FIXME(7) Implement searching bst for a bid
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''

        #set current node to self.root
        current = self.root
        #keep looping down the tree until leaf node reached or matching bidId found
        while current:
        #if match found, return current bid
            if int(current.bid.bidId) == int(bidId):
                return current.bid
        #if bid is smaller than current node then search left subtree
            elif int(bidId) < int(current.bid.bidId):
                current = current.left
        #else seach right subtree
            else:
                current = current.right


    def remove(self, bidId: str)->None:
        '''
        FIXME(8) search and remove the node from the bst
        @param bidId the id of the bid to be removed from the bst
        '''
        def removeNode(node: Node, bidId: int)->None:
            '''
            FIXME(9) Implement node removal recursively
            '''
            #handle base case: return None if node is None
            if not node:
                return None
            #elif bidId less than current node's bidId:
            if int(bidId) < int(node.bid.bidId):
            # call itself recursively to the left subtree
                removeNode(node.left, bidId)
            #elif bidId bigger than current node's bidId:
            elif int(bidId) > int(node.bid.bidId):
            # call itself recursively to the right subtree
                removeNode(node.right, bidId)
            #else: (matched node found)
            else:
                #if node is leaf node (no left and right child):
                if not (node.left or node.right):
                   #delete node
                    node = None
                #elif node has no right child:
                elif not node.left:
                   #take the left child and make it current node, then delete the old node
                    node = node.right
                #elif node has no left node:
                elif not node.right:
                    node = node.left
                   #do the opposite
                #else: node has both left and right subtree:
                else:
                    parent = node.right
                    child = parent.left
                    while child:
                        parent = child
                        child = parent.left
                    parent.left = node
                    removeNode(parent.left, nodeId)
                    #find the minimum of the right subtree nodes for bst and replace the old node with it
                    #hint: the minium of the subtree is the left most leaf node, find it , replace it
                    #with the current old node, then call removeNode recursively with (new_node.right, bidId)



        #call removeNode() with root and bidId
        if self.root:
            removeNode(self.root, bidId)



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
def loadBids(csvPath: str, bst: BinarySearchTree)->None:
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
                bst.insert(bid)
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
