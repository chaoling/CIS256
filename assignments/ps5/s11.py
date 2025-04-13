'''
Name : trees.py
Author  : Alex Vogt
Version : 1.0
Description : use trees to store the csv data set
'''

# importing DictReader class from csv module
import csv
#i was having a hard time getting past this error again and implimented the import sys and sys.argv
import sys
sys.argv = [sys.argv[0]]
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
        if root is not None and not isinstance(root, Node):
            raise TypeError("root must be of type Node")
        #bst root is initialized to None or user defined
        self.root = root


    def InOrderTraversal(self):
        '''
        Implement logic to traverse a BST in order
        '''
        def inOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''

            if node is not None:
            #recursively call inOrder() on left subtree
              inOrder(node.left)
            #print current node's bid info
              print(node.bid)
            #recursively call inOrder() on right subtree
              inOrder(node.right)

        #call inorder function and pass root
        inOrder(self.root)


    def PreOrderTraversal(self):
        '''
        Implement logic to traverse a BST pre-order
        '''
        def preOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''

            if node is not None:
            #print current node's bid info
              print(node.bid)
            #recursively call inOrder() on left subtree
              preOrder(node.left)
            #recursively call inOrder() on right subtree
              preOrder(node.right)

        #call preOrder function and pass root
        preOrder(self.root)


    def PostOrderTraversal(self):
        '''
        Implement logic to traverse a BST post-order
        '''
        def postOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''
            if node is not None:
            #recursively call inOrder() on left subtree
              postOrder(node.left)
            #recursively call inOrder() on right subtree
              postOrder(node.right)
            #print current node's bid info
              print(node.bid)


        #call postOrder function and pass root
        postOrder(self.root)


    def insert(self, bid: Bid)->None:
        '''
        implement logic to insert a bid
        @param: bid: the data to be inserted to the BST
        '''
        pass
        def addNode(node: Node, bid: Bid)->None:
            '''
            inserting a bid into the tree recursively
            '''
            if node is None:
              return Node(bid)
            
            #compares bidID to help determine the position
            if bid.bidId < node.bid.bidId:
              node.left = addNode(node.left, bid)
            elif bid.bidId > node.bid.bidId:
              node.right = addNode(node.right, bid)

            return node

          #if None, create the root with bid
            if self.root is None:
              self.root = Node(bid)
            else: 
              addNode(self.root, bid)



    def search(self, bidId: str)->Bid:
        '''
        Implement searching bst for a bid
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        current = self.root
        while current is not None:
          if bidId == current.bid.bidId:
            return current.bid
          elif bidId < current.bid.bidId:
            current = current.left #moves to left
          else:
            current = current.right #moves to right
        return None


    def remove(self, bidId: str)->None:
        '''
        search and remove the node from the bst
        @param bidId the id of the bid to be removed from the bst
        '''
        def removeNode(node: Node, bidId: int)->None:
            '''
            FIXME(9) Implement node removal recursively
            '''
            if node is None:
              return node
            if bidId < node.bid.bidId:
              node.left = removeNode(node.left, bidId)
            elif bidId > node.bid.bidId:
              node.right = removeNode(node.right, bidId)
            else:
              if node.left is None:
                return node.right
              elif node.right is None:
                return node.left
         
              minLargerNode = node.right
              while minLargerNode.left is not None:
                minLargerNode = minLargerNode.left
              node.bid = minLargerNode.bid
              node.right = removeNode(node.right, minLargerNode.bid.bidId)
            return node
        self.root = removeNode(self.root, bidId)


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