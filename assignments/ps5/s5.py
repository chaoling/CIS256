# -*- coding: utf-8 -*-
'''
Name : trees.py
Author  : Benjamin Lang
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
            if node is not None:
                inOrder(node.left)#recursively call inOrder() on left subtree
                print(node.bid)#print current node's bid info
                inOrder(node.right)#recursively call inOrder() on right subtree
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
            if node is not None:
                print(node.bid)#print current node's bid info
                preOrder(node.left)#recursively call inOrder() on left and right subtrees
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
            if node is not None:
                postOrder(node.left)#recursively call inOrder() on left and right subtrees
                postOrder(node.right)
                print(node.bid)#print current node's bid info

        #call postOrder function and pass root
        postOrder(self.root)


    def insert(self, bid: Bid)->None:
        '''
        FIXME(5) implement logic to insert a bid
        @param: bid: the data to be inserted to the BST
        '''

        def addNode(node: Node, bid: Bid)->None:
            '''
            FIXME(6) implement inserting a bid into the tree recursively
            '''
            if node.bid.bidId > bid.bidId: #if current node is bigger than bid, insert it to the left subtree
                if not node.left:
                    node.left = Node(bid)#if no left node, this bid became the left node
                else:#else recurse down the left subtree
                    addNode(node.left, bid)
            else:
                if not node.right:
                    node.right = Node(bid) #if no right node, this bid became the right node
                else:#else recurse down the right subtree
                    addNode(node.right, bid)

        if self.root is None:
            self.root = Node(bid)# self.root is assigned to new node bid
        else:#call recursive function addNode
            addNode(self.root, bid)


    def search(self, bidId: str)->Bid:
        '''
        FIXME(7) Implement searching bst for a bid
        @param bidId id of the bid to be searched
        @return bid object or None if not found
        '''
        def searchNode(node, bidId):
            if not node:
                return None
            elif bidId == node.bid.bidId:#if match found, return current bid
                return node.bid
            elif bidId < node.bid.bidId:#if bid is smaller than current node then search left subtree
                return searchNode(node.left, bidId)
            else:
                return searchNode(node.right, bidId)#else seach right subtree

        return searchNode(self.root, bidId)

    def remove(self, bidId: str)->None:
        '''
        FIXME(8) search and remove the node from the bst
        @param bidId the id of the bid to be removed from the bst
        '''
        def findMinNode(node):
            minNode = node.right
            while minNode.left:
                minNode = minNode.left
            return minNode
        def removeNode(node: Node, bidId: int)->None:
            '''
            FIXME(9) Implement node removal recursively
            '''
            if node is None:
                return None#handle base case: return None if node is None
            elif bidId < node.bid.bidId:#elif bidId less than current node's bidId
                node.left = removeNode(node.left, bidId)#call itself recursively to the left subtree
            elif bidId > node.bid.bidId:#elif bidId bigger than current node's bidId
                node.right = removeNode(node.right, bidId)#call itself recursively to the right subtree
            else:#(matched node found)
                if node.left is None and node.right is None:#if node is leaf node (no left and right child)
                    node = None#delete node
                elif node.right is None: #elif node has no right child:
                    temp = node
                    node = node.left#take the left child and make it current node, then delete the old node
                    temp = None
                elif node.left is None: #elif node has no left node
                    temp = node
                    node = node.right#take the right child and make it current node, then delete the old node
                    temp = None
                else:#node has both left and right subtree
                    minNode = findMinNode(node)#find the minimum of the right subtree nodes for bst and replace the old node with it
                    node.bid = minNode.bid#replace old node with min
                    node.right = removeNode(node.right, minNode.bid.bidId)#call removeNode recursively
            return node

        removeNode(self.root, bidId)#call removeNode() with root and bidId

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