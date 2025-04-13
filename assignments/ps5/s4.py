'''
Name : trees.py
Author  : AJ Hunt
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

        #bst root is initialized to None or user defined
        self.root = root


    def InOrderTraversal(self):

        def inOrder(node: Node)->None: # we want a helper funtion because the main function is called on a BST, while the helper is called on a single node and can then be called recursively.
            '''
            helper function in recursive calls
            '''
            #if node is not None:
            if node is not None:
                #recursively call inOrder() on left subtree
                inOrder(node.left)
                #print current node's bid info
                print(f'{node.bid}-->')
                #recursively call inOrder() on right subtree
                inOrder(node.right)

        #call inorder function and pass root
        inOrder(self.root)


    def PreOrderTraversal(self):

        def preOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''
            #if node is not None:
            if node is not None:
                #print current node's bid info
                print(f'{node.bid}-->')
                #recursively call preOrder() on left subtree
                preOrder(node.left)
                #recursively call preOrder() on right subtree
                preOrder(node.right)

        #call preOrder function and pass root
        preOrder(self.root)


    def PostOrderTraversal(self):

        def postOrder(node: Node)->None:
            '''
            helper function in recursive calls
            '''
            #if node is not None:
            if node is not None:
                #recursively call postOrder() on left subtree
                postOrder(node.left)
                #recursively call postOrder() on right subtree
                postOrder(node.right)
                #print current node's bid info
                print(f'{node.bid}-->')

        #call postOrder function and pass root
        postOrder(self.root)


    def insert(self, bid: Bid)->None:
        '''
        @param: bid: the data to be inserted to the BST
        '''
        def addNode(node: Node, bid: Bid)->None:
            #if current node is bigger than bid, insert it to the left subtree
            if node.bid.bidId > bid.bidId:
                #if no left node, this bid became the left node
                if not node.left:
                    node.left = Node(bid)
                #else recurse down the left subtree
                else:
                    addNode(node.left, bid)
            # else if current node not bigger than bid, insert it to the right subtree
            else:
                #if no right node, this bid became the right node
                if not node.right:
                    node.right = Node(bid)
                #else recurse down the right subtree
                else:
                    addNode(node.right, bid)

        # if BST is empty, self.root is assigned to new node bid
        if self.root is None:
            self.root = Node(bid)
        #else, call recursive function addNode(self.root, bid)
        else:
            addNode(self.root, bid)

    def search(self, bidId: str)->Bid:
        '''
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        def searchNode(node, bidId):
            # base case: if we get to the end of the bst, we will search an empty node, so we return None (did not find the node in that branch)
            if not node:
                return None
            #if match found, return current bid
            elif bidId == node.bid.bidId:
                return node.bid
            #if bidId is smaller than current node then search left subtree
            elif bidId < node.bid.bidId:
                return searchNode(node.left, bidId)
            #else seach right subtree
            else:
                return searchNode(node.right, bidId)

        # call helper function on the root of the bst
        return searchNode(self.root, bidId)


    def remove(self, bidId: str)->None:
        '''
        @param bidId the id of the bid to be removed from the bst
        '''
        # helper function to find the minimum node (next largest to node to be removed)
        def findMinNode(node):
            # traverse to the leftmost node of the right subtree (next largest)
            tmp = node.right
            while tmp.left:
                tmp = tmp.left
            return tmp

        def removeNode(node: Node, bidId: int)->Node:
            #handle base case: return None if node is None
            if node is None:
                return None

            #elif: (matched node found)
            elif node.bid.bidId == bidId: #find a match, now remove it
                #if node is leaf node (no left and right child):
                if node.left is None and node.right is None:
                    #delete node
                    node = None
                #elif node has no right child:
                elif node.right is None:
                    #take the left child and make it current node, then delete the old node
                    tmp = node
                    node = node.left
                    tmp = None
                #elif node has no left node:
                elif node.left is None:
                    #take the right child and make it current node, then delete the old node
                    tmp = node
                    node = node.right
                    tmp = None
                #else: node has both left and right subtree:
                else:
                    #find the minimum of the right subtree nodes for bst and replace the old node with it
                    minNode = findMinNode(node)
                    node.bid = minNode.bid
                    # call removeNode recursively with (new_node.right, bidId) to remove the minimum node we just promoted
                    node.right = removeNode(node.right, minNode.bid.bidId)
            # now search the tree for the node to be removed
            #elif bidId less than current node's bidId:
            elif bidId < node.bid.bidId:
                # call itself recursively to the left subtree
                node.left = removeNode(node.left, bidId)
            #elif bidId bigger than current node's bidId:
            else:
                # call itself recursively to the right subtree
                node.right = removeNode(node.right, bidId)

            return node
        #call removeNode() with root and bidId
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

    args = parser.parse_args(args=[])
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