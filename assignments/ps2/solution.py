'''
Name : sorting.py
Author  : Chao Ling
Version : 1.0
Description : Apply Sorting Algorithms to the csv data set
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
def loadBids(csvPath: str) -> List:
    '''
    Load a CSV file containing bids into a container
    @param csvPath the path to the CSV file
    @return a container holding all the bids read
    '''
    # opening csv file
    print(f"now loading csv file {csvPath}...")
    bids = []
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
                bid = Bid(entry.get('auctionid',""),entry.get('auctiontitle',None),entry.get('fund',""),str2float(entry.get('winningbid','0.0'),['$',',']))
                bids.append(bid)
    except Exception as ex:
        print(f"excetion occurred, {ex}")
        
    return bids

# FIXME (1a): Impement the selection sort logic over bid.bidId
def selectionSort(bids: List) -> None:
    '''
    Perform a selection sort on bid title
    Average performance: O(n^2))
    Worst case performance O(n^2))
    @param bid list instance to
    '''
    n = len(bids)
    for i in range(n):
        min_pos = i
        #pick smallest bid's index position and exchange it with ith pos
        for j in range(i+1,n):
            if bids[j].title < bids[min_pos].title:
                min_pos = j
        if min_pos != i:
            bids[min_pos],bids[i] = bids[i],bids[min_pos] #exchange value

#FIXME (2a): Implement the quick sort logic over bid.title
def quickSort(bids: List) -> None:
    '''
    Perform a quick sort on bid title
    Average performance: O(n log(n))
    Worst case performance O(n^2))
    @param bids ref to the bids List to be sorted
    '''
    def partition(bids: List, begin: int, end: int) -> int:
        '''
        Partition the vector of bids into two parts, low and high
        @param bids ref to the bids List to be partitioned
        @param begin Beginning index to partition
        @param end Ending index to partition
        '''
        #set low and high equal to begin and end
        low, hi = begin+1, end

        #pick the middle element as pivot point
        pivot = begin + (end-begin)//2
        pivot_val = bids[pivot]
        #exchange pivot with low
        bids[pivot],bids[begin] = bids[begin],bids[pivot]
        #print(f'{pivot=}')
        done = False
        # while not done
        while not done:
            #keep incrementing low index while bids[low] < bids[pivot]
            while low <= hi and bids[low].title <= pivot_val.title:
                low += 1

            #keep decrementing high index while bids[pivot] < bids[high]
            while hi >=low and bids[hi].title >= pivot_val.title:
                hi -= 1
            #If there are zero or one elements remaining, all bids are partitioned. Return high
            if hi < low:
                done = True
            else:
                bids[low],bids[hi] = bids[hi],bids[low]
            #else swap the low and high bids ()
            #move low and high closer ++low, --high
        bids[begin],bids[hi] = bids[hi],bids[begin] #don't forget to exchange pivot to right position
        return hi

    def qSort(bids: List, begin: int, end: int) -> None:
        '''
        Helper function, perform a quickSort recursively
        @param bids ref to the bids List to be partitioned
        @param begin Beginning index to partition
        @param end Ending index to partition
        '''
        
        #Base case: If there are 1 or zero bids to sort,
        n = len(bids)
        if n <= 1:
            return
        #partition is already sorted otherwise if begin is greater than or equal to end then return
        if begin >= end:
            return
        #Partition bids into low and high such that midpoint is location of last element in low
        mid = partition(bids, begin, end)
        #recursively sort low partition (begin to mid)1
        qSort(bids, begin, mid-1)
        #recursively sort high partition (mid+1 to end)
        qSort(bids, mid+1, end)

    qSort(bids,0,len(bids)-1)
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process cmd line arguments')
    parser.add_argument('-p','--path', default='eBid_Monthly_Sales_Dec.csv',
                    help='path to the csv file')

    args = parser.parse_args()
    menu = {}
    menu['1']="Load Bids" 
    menu['2']="Display All Bids"
    menu['3']="Selection Sort All Bids"
    menu['4']="Quick Sort All Bids"
    menu['9']="Exit"
    
    while True: 
        options=menu.keys()
        for entry in options: 
            print(entry, menu[entry]) #display the menu item

        selection=input("Enter choices: ") 
        if selection =='1': 
            bids = loadBids(args.path)
        elif selection == '2': 
            print("display bids....")
            for bid in bids:
                print(bid)
        elif selection == '3':
            print("selection sort...")
            selectionSort(bids)
        elif selection == '4': 
            print("quick sort...")
            quickSort(bids)
        elif selection == '9': 
            print("Bye!")
            break
        else: 
            print("Unknown Option Selected!")
    